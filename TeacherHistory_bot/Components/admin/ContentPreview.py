import React, { useState, useEffect } from 'react';
import { Topic, Assignment } from '@/entities/all';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Eye, Play, BookOpen, Crown, Lock } from 'lucide-react';
import { motion } from 'framer-motion';

export default function ContentPreview() {
    const [topics, setTopics] = useState([]);
    const [assignments, setAssignments] = useState([]);
    const [selectedGrade, setSelectedGrade] = useState('5');
    const [selectedTopic, setSelectedTopic] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [topicsData, assignmentsData] = await Promise.all([
                Topic.list('grade'),
                Assignment.list('-created_date')
            ]);
            setTopics(topicsData);
            setAssignments(assignmentsData);
        } catch (error) {
            console.error("Ошибка загрузки данных:", error);
        }
        setLoading(false);
    };

    const getTopicsByGradeAndSubject = (grade, subject) => {
        return topics.filter(t => 
            t.grade === parseInt(grade) && 
            t.subject === subject
        ).sort((a, b) => (a.order_index || 0) - (b.order_index || 0));
    };

    const getAssignmentsByTopic = (topicId) => {
        return assignments.filter(a => a.topic_id === topicId);
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center p-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Eye className="w-5 h-5" />
                        Предпросмотр учебных материалов
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="mb-6">
                        <Select value={selectedGrade} onValueChange={setSelectedGrade}>
                            <SelectTrigger className="w-48">
                                <SelectValue placeholder="Выберите класс" />
                            </SelectTrigger>
                            <SelectContent>
                                {[5, 6, 7, 8, 9, 10, 11].map(grade => (
                                    <SelectItem key={grade} value={grade.toString()}>
                                        {grade} класс
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>

                    <Tabs defaultValue="history" className="w-full">
                        <TabsList className="grid w-full grid-cols-2">
                            <TabsTrigger value="history">История</TabsTrigger>
                            <TabsTrigger value="social_studies">Обществознание</TabsTrigger>
                        </TabsList>
                        
                        <TabsContent value="history">
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
                                {getTopicsByGradeAndSubject(selectedGrade, 'history').map((topic, index) => (
                                    <motion.div
                                        key={topic.id}
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: index * 0.1 }}
                                        className="cursor-pointer"
                                        onClick={() => setSelectedTopic(topic)}
                                    >
                                        <Card className={`h-full transition-all duration-300 hover:shadow-lg relative overflow-hidden ${
                                            topic.is_premium ? 'border-yellow-200 bg-gradient-to-br from-yellow-50 to-white' : 'border-gray-200 hover:border-gray-300'
                                        }`}>
                                            {topic.is_premium && (
                                                <div className="absolute top-2 right-2 p-1.5 bg-yellow-400 rounded-full text-white shadow-lg">
                                                    <Crown className="w-4 h-4" />
                                                </div>
                                            )}
                                            <CardHeader className="pb-3">
                                                <div className="flex items-start justify-between">
                                                    <div className="flex items-center gap-3">
                                                        <div className="w-10 h-10 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center">
                                                            <BookOpen className="w-5 h-5" />
                                                        </div>
                                                        <div>
                                                            <CardTitle className="text-base leading-tight">{topic.title}</CardTitle>
                                                            <p className="text-sm text-gray-500">История</p>
                                                        </div>
                                                    </div>
                                                </div>
                                            </CardHeader>
                                            
                                            <CardContent>
                                                <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                                                    {topic.content?.substring(0, 120)}...
                                                </p>
                                                
                                                <div className="flex items-center justify-between">
                                                    <Badge variant="outline" className="text-xs">
                                                        +{topic.points_reward} баллов
                                                    </Badge>
                                                    {topic.video_url && (
                                                        <div className="flex items-center gap-1 text-xs text-blue-600">
                                                            <Play className="w-3 h-3" />
                                                            Медиа
                                                        </div>
                                                    )}
                                                </div>
                                            </CardContent>
                                        </Card>
                                    </motion.div>
                                ))}
                            </div>
                        </TabsContent>
                        
                        <TabsContent value="social_studies">
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
                                {getTopicsByGradeAndSubject(selectedGrade, 'social_studies').map((topic, index) => (
                                    <motion.div
                                        key={topic.id}
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: index * 0.1 }}
                                        className="cursor-pointer"
                                        onClick={() => setSelectedTopic(topic)}
                                    >
                                        <Card className={`h-full transition-all duration-300 hover:shadow-lg relative overflow-hidden ${
                                            topic.is_premium ? 'border-yellow-200 bg-gradient-to-br from-yellow-50 to-white' : 'border-gray-200 hover:border-gray-300'
                                        }`}>
                                            {topic.is_premium && (
                                                <div className="absolute top-2 right-2 p-1.5 bg-yellow-400 rounded-full text-white shadow-lg">
                                                    <Crown className="w-4 h-4" />
                                                </div>
                                            )}
                                            <CardHeader className="pb-3">
                                                <div className="flex items-start justify-between">
                                                    <div className="flex items-center gap-3">
                                                        <div className="w-10 h-10 rounded-xl bg-green-100 text-green-600 flex items-center justify-center">
                                                            <BookOpen className="w-5 h-5" />
                                                        </div>
                                                        <div>
                                                            <CardTitle className="text-base leading-tight">{topic.title}</CardTitle>
                                                            <p className="text-sm text-gray-500">Обществознание</p>
                                                        </div>
                                                    </div>
                                                </div>
                                            </CardHeader>
                                            
                                            <CardContent>
                                                <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                                                    {topic.content?.substring(0, 120)}...
                                                </p>
                                                
                                                <div className="flex items-center justify-between">
                                                    <Badge variant="outline" className="text-xs">
                                                        +{topic.points_reward} баллов
                                                    </Badge>
                                                    {topic.video_url && (
                                                        <div className="flex items-center gap-1 text-xs text-blue-600">
                                                            <Play className="w-3 h-3" />
                                                            Медиа
                                                        </div>
                                                    )}
                                                </div>
                                            </CardContent>
                                        </Card>
                                    </motion.div>
                                ))}
                            </div>
                        </TabsContent>
                    </Tabs>
                </CardContent>
            </Card>

            {/* Детальный просмотр темы */}
            {selectedTopic && (
                <Card>
                    <CardHeader>
                        <div className="flex items-center justify-between">
                            <CardTitle className="flex items-center gap-3">
                                <BookOpen className="w-6 h-6 text-blue-600" />
                                {selectedTopic.title}
                                {selectedTopic.is_premium && (
                                    <Crown className="w-5 h-5 text-yellow-500" />
                                )}
                            </CardTitle>
                            <Button variant="outline" onClick={() => setSelectedTopic(null)}>
                                Закрыть
                            </Button>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="grid lg:grid-cols-3 gap-6">
                            <div className="lg:col-span-2">
                                <div className="prose max-w-none">
                                    <p className="whitespace-pre-wrap text-gray-700">{selectedTopic.content}</p>
                                </div>
                                {selectedTopic.video_url && (
                                    <div className="mt-6">
                                        <h4 className="font-medium mb-3">Медиафайл:</h4>
                                        <div className="p-4 bg-gray-50 rounded-lg">
                                            <p className="text-sm text-gray-600 mb-2">Ссылка на медиа:</p>
                                            <a 
                                                href={selectedTopic.video_url} 
                                                target="_blank" 
                                                rel="noopener noreferrer"
                                                className="text-blue-600 hover:underline"
                                            >
                                                {selectedTopic.video_url}
                                            </a>
                                        </div>
                                    </div>
                                )}
                            </div>

                            <div className="space-y-4">
                                <Card>
                                    <CardHeader>
                                        <CardTitle className="text-lg">Задания по теме</CardTitle>
                                    </CardHeader>
                                    <CardContent className="space-y-3">
                                        {getAssignmentsByTopic(selectedTopic.id).map((assignment) => (
                                            <div
                                                key={assignment.id}
                                                className="p-3 rounded-lg border border-gray-200"
                                            >
                                                <h4 className="font-medium text-sm">{assignment.title}</h4>
                                                <div className="flex gap-2 mt-2">
                                                    <Badge variant="outline" className="text-xs">
                                                        {assignment.type}
                                                    </Badge>
                                                    <Badge variant="secondary" className="text-xs">
                                                        {assignment.exam_format}
                                                    </Badge>
                                                    <Badge className="text-xs bg-blue-100 text-blue-800">
                                                        {assignment.points} б.
                                                    </Badge>
                                                </div>
                                            </div>
                                        ))}
                                        
                                        {getAssignmentsByTopic(selectedTopic.id).length === 0 && (
                                            <p className="text-gray-500 text-sm">Заданий пока нет</p>
                                        )}
                                    </CardContent>
                                </Card>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}