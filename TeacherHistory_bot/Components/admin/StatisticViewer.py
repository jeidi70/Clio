import React, { useState, useEffect } from 'react';
import { User, UserProgress, Topic, Assignment } from '@/entities/all';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { BarChart3, Users, BookOpen, Target, TrendingUp, Award } from 'lucide-react';

export default function StatisticsViewer() {
    const [users, setUsers] = useState([]);
    const [userProgress, setUserProgress] = useState([]);
    const [topics, setTopics] = useState([]);
    const [assignments, setAssignments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedGrade, setSelectedGrade] = useState('all');

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [usersData, progressData, topicsData, assignmentsData] = await Promise.all([
                User.list('-total_points'),
                UserProgress.list('-created_date'),
                Topic.list('grade'),
                Assignment.list('-created_date')
            ]);
            setUsers(usersData);
            setUserProgress(progressData);
            setTopics(topicsData);
            setAssignments(assignmentsData);
        } catch (error) {
            console.error("Ошибка загрузки данных:", error);
        }
        setLoading(false);
    };

    const getFilteredUsers = () => {
        return selectedGrade === 'all' 
            ? users 
            : users.filter(u => u.grade?.toString() === selectedGrade);
    };

    const getGradeStats = () => {
        const filteredUsers = getFilteredUsers();
        const gradeProgress = userProgress.filter(p => 
            filteredUsers.some(u => u.email === p.created_by)
        );

        const totalUsers = filteredUsers.length;
        const activeUsers = filteredUsers.filter(u => u.total_points > 0).length;
        const totalAnswers = gradeProgress.length;
        const correctAnswers = gradeProgress.filter(p => p.is_correct).length;
        const accuracy = totalAnswers > 0 ? (correctAnswers / totalAnswers * 100) : 0;
        const avgPoints = totalUsers > 0 ? 
            filteredUsers.reduce((sum, u) => sum + (u.total_points || 0), 0) / totalUsers : 0;

        return {
            totalUsers,
            activeUsers,
            totalAnswers,
            correctAnswers,
            accuracy: Math.round(accuracy),
            avgPoints: Math.round(avgPoints)
        };
    };

    const getTopicStats = () => {
        const filteredUsers = getFilteredUsers();
        const gradeTopics = topics.filter(t => 
            selectedGrade === 'all' || t.grade?.toString() === selectedGrade
        );

        return gradeTopics.map(topic => {
            const topicProgress = userProgress.filter(p => p.topic_id === topic.id);
            const uniqueUsers = new Set(topicProgress.map(p => p.created_by)).size;
            const completions = topicProgress.filter(p => p.is_correct).length;
            
            return {
                ...topic,
                attempts: topicProgress.length,
                uniqueUsers,
                completions,
                completionRate: topicProgress.length > 0 ? 
                    Math.round((completions / topicProgress.length) * 100) : 0
            };
        }).sort((a, b) => b.attempts - a.attempts);
    };

    const getLeaderboard = () => {
        const filteredUsers = getFilteredUsers();
        return filteredUsers
            .filter(u => u.total_points > 0)
            .slice(0, 10)
            .map((user, index) => ({
                ...user,
                rank: index + 1,
                progress: userProgress.filter(p => p.created_by === user.email)
            }));
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center p-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    const gradeStats = getGradeStats();
    const topicStats = getTopicStats();
    const leaderboard = getLeaderboard();

    return (
        <div className="space-y-6">
            {/* Фильтр по классам */}
            <div className="flex items-center gap-4">
                <Select value={selectedGrade} onValueChange={setSelectedGrade}>
                    <SelectTrigger className="w-48">
                        <SelectValue placeholder="Выберите класс" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="all">Все классы</SelectItem>
                        {[5, 6, 7, 8, 9, 10, 11].map(grade => (
                            <SelectItem key={grade} value={grade.toString()}>
                                {grade} класс
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>

            {/* Общая статистика */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3">
                            <Users className="w-8 h-8 text-blue-600" />
                            <div>
                                <h3 className="text-2xl font-bold">{gradeStats.totalUsers}</h3>
                                <p className="text-gray-600">Пользователей</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3">
                            <TrendingUp className="w-8 h-8 text-green-600" />
                            <div>
                                <h3 className="text-2xl font-bold">{gradeStats.activeUsers}</h3>
                                <p className="text-gray-600">Активных</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3">
                            <Target className="w-8 h-8 text-purple-600" />
                            <div>
                                <h3 className="text-2xl font-bold">{gradeStats.accuracy}%</h3>
                                <p className="text-gray-600">Точность</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3">
                            <Award className="w-8 h-8 text-yellow-600" />
                            <div>
                                <h3 className="text-2xl font-bold">{gradeStats.avgPoints}</h3>
                                <p className="text-gray-600">Средний балл</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            <div className="grid lg:grid-cols-2 gap-6">
                {/* Статистика по темам */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <BarChart3 className="w-5 h-5" />
                            Популярные темы
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-3">
                            {topicStats.slice(0, 8).map(topic => (
                                <div key={topic.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                    <div className="flex-1">
                                        <h4 className="font-medium">{topic.title}</h4>
                                        <div className="flex items-center gap-2 mt-1">
                                            <Badge variant="outline">{topic.grade} класс</Badge>
                                            <Badge variant="secondary">
                                                {topic.subject === 'history' ? 'История' : 'Обществознание'}
                                            </Badge>
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <div className="text-lg font-bold text-blue-600">
                                            {topic.attempts}
                                        </div>
                                        <div className="text-sm text-gray-500">
                                            {topic.completionRate}% успех
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                {/* Лидерборд */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Award className="w-5 h-5" />
                            Топ учеников
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-3">
                            {leaderboard.map(user => (
                                <div key={user.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${
                                        user.rank === 1 ? 'bg-yellow-500' :
                                        user.rank === 2 ? 'bg-gray-400' :
                                        user.rank === 3 ? 'bg-amber-600' :
                                        'bg-blue-500'
                                    }`}>
                                        {user.rank}
                                    </div>
                                    <div className="w-10 h-10 rounded-full overflow-hidden bg-gray-200 flex items-center justify-center">
                                        {user.profile_picture_url ? (
                                            <img 
                                                src={user.profile_picture_url} 
                                                alt="Profile" 
                                                className="w-full h-full object-cover" 
                                            />
                                        ) : (
                                            <span className="font-bold text-gray-600">
                                                {user.full_name?.charAt(0) || 'У'}
                                            </span>
                                        )}
                                    </div>
                                    <div className="flex-1">
                                        <h4 className="font-medium">
                                            {user.full_name || 'Ученик'}
                                        </h4>
                                        <p className="text-sm text-gray-500">
                                            {user.grade} класс • Уровень {user.level}
                                        </p>
                                    </div>
                                    <div className="text-right">
                                        <div className="text-lg font-bold text-blue-600">
                                            {user.total_points}
                                        </div>
                                        <div className="text-sm text-gray-500">
                                            {user.progress.length} ответов
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}