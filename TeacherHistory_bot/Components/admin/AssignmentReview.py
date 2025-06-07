import React, { useState, useEffect } from 'react';
import { UserProgress, Assignment, User, Topic } from '@/entities/all';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { CheckCircle2, XCircle, Clock, MessageSquare } from 'lucide-react';
import { InvokeLLM } from '@/integrations/Core';

export default function AssignmentReview() {
    const [submissions, setSubmissions] = useState([]);
    const [assignments, setAssignments] = useState([]);
    const [users, setUsers] = useState([]);
    const [topics, setTopics] = useState([]);
    const [selectedSubmission, setSelectedSubmission] = useState(null);
    const [feedback, setFeedback] = useState('');
    const [points, setPoints] = useState(0);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('pending');

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [submissionsData, assignmentsData, usersData, topicsData] = await Promise.all([
                UserProgress.list('-created_date'),
                Assignment.list('-created_date'),
                User.list('-created_date'),
                Topic.list('grade')
            ]);
            setSubmissions(submissionsData);
            setAssignments(assignmentsData);
            setUsers(usersData);
            setTopics(topicsData);
        } catch (error) {
            console.error("Ошибка загрузки данных:", error);
        }
        setLoading(false);
    };

    const getFilteredSubmissions = () => {
        return submissions.filter(submission => {
            const assignment = assignments.find(a => a.id === submission.assignment_id);
            if (!assignment) return false;
            
            if (filter === 'pending') {
                return assignment.type !== 'test' && submission.ai_feedback === undefined;
            } else if (filter === 'reviewed') {
                return submission.ai_feedback !== undefined;
            } else {
                return assignment.type !== 'test';
            }
        });
    };

    const getAssignmentTitle = (assignmentId) => {
        const assignment = assignments.find(a => a.id === assignmentId);
        return assignment ? assignment.title : 'Неизвестное задание';
    };

    const getTopicTitle = (topicId) => {
        const topic = topics.find(t => t.id === topicId);
        return topic ? topic.title : 'Неизвестная тема';
    };

    const getUserName = (email) => {
        const user = users.find(u => u.email === email);
        return user ? (user.full_name || user.email) : email;
    };

    const handleReview = async (submission, isCorrect, pointsEarned, aiFeedback) => {
        try {
            await UserProgress.update(submission.id, {
                is_correct: isCorrect,
                points_earned: pointsEarned,
                ai_feedback: aiFeedback
            });

            // Обновляем баллы пользователя
            const user = users.find(u => u.email === submission.created_by);
            if (user) {
                const newTotalPoints = (user.total_points || 0) + pointsEarned;
                await User.update(user.id, { 
                    total_points: newTotalPoints,
                    level: Math.floor(newTotalPoints / 100) + 1
                });
            }

            loadData();
            setSelectedSubmission(null);
            setFeedback('');
            setPoints(0);
        } catch (error) {
            console.error("Ошибка сохранения оценки:", error);
        }
    };

    const handleAIReview = async () => {
        if (!selectedSubmission) return;

        const assignment = assignments.find(a => a.id === selectedSubmission.assignment_id);
        if (!assignment) return;

        try {
            const aiResult = await InvokeLLM({
                prompt: `Проверь ответ ученика на задание по истории/обществознанию.
                
                Задание: ${assignment.question}
                Правильный ответ: ${assignment.correct_answer}
                Ответ ученика: ${selectedSubmission.user_answer}
                
                Оцени ответ по критериям:
                1. Правильность фактов
                2. Полнота ответа
                3. Структура изложения
                
                Выстави баллы от 0 до ${assignment.points} и дай подробную обратную связь.`,
                response_json_schema: {
                    type: "object",
                    properties: {
                        is_correct: { type: "boolean" },
                        points_earned: { type: "number" },
                        feedback: { type: "string" }
                    }
                }
            });
            
            setPoints(aiResult.points_earned);
            setFeedback(aiResult.feedback);
        } catch (error) {
            console.error("Ошибка ИИ-проверки:", error);
            alert("Ошибка при получении ИИ-оценки. Попробуйте еще раз.");
        }
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center p-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    const filteredSubmissions = getFilteredSubmissions();

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <CheckCircle2 className="w-5 h-5" />
                        Проверка развернутых ответов
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="mb-6">
                        <Select value={filter} onValueChange={setFilter}>
                            <SelectTrigger className="w-48">
                                <SelectValue placeholder="Фильтр заданий" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="pending">Ожидают проверки</SelectItem>
                                <SelectItem value="reviewed">Проверенные</SelectItem>
                                <SelectItem value="all">Все развернутые</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div className="grid gap-4">
                        {filteredSubmissions.map(submission => {
                            const assignment = assignments.find(a => a.id === submission.assignment_id);
                            if (!assignment) return null;

                            return (
                                <Card 
                                    key={submission.id} 
                                    className={`cursor-pointer transition-all duration-200 ${
                                        submission.ai_feedback ? 'border-green-200 bg-green-50' : 'border-orange-200 bg-orange-50 hover:border-orange-300'
                                    }`}
                                    onClick={() => setSelectedSubmission(submission)}
                                >
                                    <CardContent className="p-4">
                                        <div className="flex items-start justify-between">
                                            <div className="flex-1">
                                                <div className="flex items-center gap-2 mb-2">
                                                    <h3 className="font-medium">{getAssignmentTitle(assignment.id)}</h3>
                                                    <Badge variant="outline">{assignment.type}</Badge>
                                                    <Badge variant="secondary">{assignment.exam_format}</Badge>
                                                    {submission.ai_feedback ? (
                                                        <CheckCircle2 className="w-4 h-4 text-green-600" />
                                                    ) : (
                                                        <Clock className="w-4 h-4 text-orange-600" />
                                                    )}
                                                </div>
                                                <p className="text-sm text-gray-600">
                                                    Тема: {getTopicTitle(submission.topic_id)} • 
                                                    Ученик: {getUserName(submission.created_by)} • 
                                                    {assignment.points} баллов max
                                                </p>
                                                <p className="text-sm text-gray-700 mt-2 line-clamp-2">
                                                    {submission.user_answer.substring(0, 150)}...
                                                </p>
                                            </div>
                                            <div className="text-right">
                                                {submission.ai_feedback ? (
                                                    <div>
                                                        <div className="text-lg font-bold text-green-600">
                                                            {submission.points_earned}/{assignment.points}
                                                        </div>
                                                        <div className="text-sm text-gray-500">Проверено</div>
                                                    </div>
                                                ) : (
                                                    <Badge variant="outline" className="bg-orange-100">
                                                        Требует проверки
                                                    </Badge>
                                                )}
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            );
                        })}

                        {filteredSubmissions.length === 0 && (
                            <div className="text-center py-8 text-gray-500">
                                {filter === 'pending' ? 'Нет заданий, ожидающих проверки' : 'Заданий не найдено'}
                            </div>
                        )}
                    </div>
                </CardContent>
            </Card>

            {/* Детальная проверка */}
            {selectedSubmission && (
                <Card>
                    <CardHeader>
                        <div className="flex items-center justify-between">
                            <CardTitle className="flex items-center gap-2">
                                <MessageSquare className="w-5 h-5" />
                                Проверка ответа
                            </CardTitle>
                            <Button variant="outline" onClick={() => setSelectedSubmission(null)}>
                                Закрыть
                            </Button>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="grid lg:grid-cols-2 gap-6">
                            <div>
                                <h3 className="font-medium mb-3">Задание:</h3>
                                <div className="p-4 bg-gray-50 rounded-lg mb-4">
                                    <p className="text-gray-700">
                                        {assignments.find(a => a.id === selectedSubmission.assignment_id)?.question}
                                    </p>
                                </div>
                                
                                <h3 className="font-medium mb-3">Ответ ученика:</h3>
                                <div className="p-4 bg-blue-50 rounded-lg mb-4">
                                    <p className="text-gray-700 whitespace-pre-wrap">
                                        {selectedSubmission.user_answer}
                                    </p>
                                </div>

                                <h3 className="font-medium mb-3">Эталонный ответ:</h3>
                                <div className="p-4 bg-green-50 rounded-lg">
                                    <p className="text-gray-700">
                                        {assignments.find(a => a.id === selectedSubmission.assignment_id)?.correct_answer}
                                    </p>
                                </div>
                            </div>

                            <div>
                                <div className="mb-4">
                                    <Button onClick={handleAIReview} className="w-full mb-4">
                                        Получить ИИ-оценку
                                    </Button>
                                </div>

                                <div className="mb-4">
                                    <label className="block text-sm font-medium mb-2">Баллы (макс. {assignments.find(a => a.id === selectedSubmission.assignment_id)?.points}):</label>
                                    <input
                                        type="number"
                                        min="0"
                                        max={assignments.find(a => a.id === selectedSubmission.assignment_id)?.points || 0}
                                        value={points}
                                        onChange={(e) => setPoints(parseInt(e.target.value) || 0)}
                                        className="w-full p-2 border rounded-lg"
                                    />
                                </div>

                                <div className="mb-4">
                                    <label className="block text-sm font-medium mb-2">Обратная связь:</label>
                                    <Textarea
                                        value={feedback}
                                        onChange={(e) => setFeedback(e.target.value)}
                                        placeholder="Напишите комментарий для ученика..."
                                        className="min-h-[150px]"
                                    />
                                </div>

                                <div className="flex gap-3">
                                    <Button
                                        onClick={() => handleReview(selectedSubmission, points > 0, points, feedback)}
                                        className="flex-1"
                                        disabled={!feedback.trim()}
                                    >
                                        Сохранить оценку
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}