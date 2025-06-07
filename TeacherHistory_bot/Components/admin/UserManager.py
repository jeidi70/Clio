import React, { useState, useEffect } from 'react';
import { User, UserProgress } from '@/entities/all';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Search, Crown, Users as UsersIcon, TrendingUp, Trash2, AlertTriangle } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
  DialogClose
} from "@/components/ui/dialog";

export default function UserManager() {
    const [users, setUsers] = useState([]);
    const [userProgress, setUserProgress] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [gradeFilter, setGradeFilter] = useState('all');
    const [userToDelete, setUserToDelete] = useState(null);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [usersData, progressData] = await Promise.all([
                User.list('-total_points'),
                UserProgress.list('-created_date')
            ]);
            setUsers(usersData);
            setUserProgress(progressData);
        } catch (error) {
            console.error("Ошибка загрузки данных:", error);
        }
        setLoading(false);
    };

    const getUserProgress = (userId) => {
        return userProgress.filter(p => p.created_by === userId);
    };

    const getUserStats = (user) => {
        const progress = getUserProgress(user.email);
        const correctAnswers = progress.filter(p => p.is_correct).length;
        const totalAnswers = progress.length;
        const accuracy = totalAnswers > 0 ? (correctAnswers / totalAnswers * 100) : 0;
        
        return {
            totalAnswers,
            correctAnswers,
            accuracy: Math.round(accuracy),
            totalPoints: user.total_points || 0,
            level: user.level || 1
        };
    };

    const handleDeleteUser = async (user) => {
        try {
            // Сначала удаляем все записи прогресса пользователя
            const userProgressRecords = userProgress.filter(p => p.created_by === user.email);
            for (const progress of userProgressRecords) {
                await UserProgress.delete(progress.id);
            }
            
            // Затем удаляем самого пользователя
            await User.delete(user.id);
            
            // Обновляем данные
            loadData();
            setUserToDelete(null);
        } catch (error) {
            console.error("Ошибка удаления пользователя:", error);
            alert("Не удалось удалить пользователя. Попробуйте еще раз.");
        }
    };

    const filteredUsers = users.filter(user => {
        const matchesSearch = !searchTerm || 
            user.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            user.email?.toLowerCase().includes(searchTerm.toLowerCase());
        
        const matchesGrade = gradeFilter === 'all' || user.grade?.toString() === gradeFilter;
        
        return matchesSearch && matchesGrade;
    });

    if (loading) {
        return (
            <div className="flex justify-center items-center p-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Статистика */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3">
                            <UsersIcon className="w-8 h-8 text-blue-600" />
                            <div>
                                <h3 className="text-2xl font-bold">{users.length}</h3>
                                <p className="text-gray-600">Всего пользователей</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3">
                            <TrendingUp className="w-8 h-8 text-green-600" />
                            <div>
                                <h3 className="text-2xl font-bold">
                                    {users.filter(u => u.total_points > 0).length}
                                </h3>
                                <p className="text-gray-600">Активных учеников</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3">
                            <Crown className="w-8 h-8 text-yellow-600" />
                            <div>
                                <h3 className="text-2xl font-bold">
                                    {Math.round(users.reduce((sum, u) => sum + (u.total_points || 0), 0) / users.length)}
                                </h3>
                                <p className="text-gray-600">Средний балл</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Фильтры */}
            <Card>
                <CardHeader>
                    <CardTitle>Управление пользователями</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex gap-4 mb-6">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                            <Input
                                placeholder="Поиск по имени или email..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="pl-10"
                            />
                        </div>
                        <Select value={gradeFilter} onValueChange={setGradeFilter}>
                            <SelectTrigger className="w-48">
                                <SelectValue placeholder="Фильтр по классу" />
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

                    {/* Список пользователей */}
                    <div className="space-y-3">
                        {filteredUsers.map(user => {
                            const stats = getUserStats(user);
                            const canDelete = user.role !== 'admin'; // Не можем удалить админов
                            
                            return (
                                <div key={user.id} className="p-4 border rounded-lg">
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center gap-4">
                                            <div className="w-12 h-12 rounded-full overflow-hidden bg-gray-200 flex items-center justify-center">
                                                {user.profile_picture_url ? (
                                                    <img 
                                                        src={user.profile_picture_url} 
                                                        alt="Profile" 
                                                        className="w-full h-full object-cover" 
                                                    />
                                                ) : (
                                                    <span className="text-lg font-bold text-gray-600">
                                                        {user.full_name?.charAt(0) || user.email?.charAt(0) || 'У'}
                                                    </span>
                                                )}
                                            </div>
                                            <div>
                                                <h3 className="font-medium text-lg">
                                                    {user.full_name || 'Без имени'}
                                                </h3>
                                                <p className="text-gray-600">{user.email}</p>
                                                <div className="flex items-center gap-2 mt-1">
                                                    {user.role === 'admin' && (
                                                        <Badge variant="secondary" className="bg-red-100 text-red-800">
                                                            Админ
                                                        </Badge>
                                                    )}
                                                    {user.grade && (
                                                        <Badge variant="outline">
                                                            {user.grade} класс
                                                        </Badge>
                                                    )}
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex items-center gap-4">
                                            <div className="text-center">
                                                <div className="text-sm text-gray-500">Уровень</div>
                                                <div className="text-lg font-bold text-yellow-600">
                                                    {stats.level}
                                                </div>
                                            </div>
                                            <div className="text-center">
                                                <div className="text-sm text-gray-500">Баллы</div>
                                                <div className="text-lg font-bold text-blue-600">
                                                    {stats.totalPoints}
                                                </div>
                                            </div>
                                            <div className="text-center">
                                                <div className="text-sm text-gray-500">Точность</div>
                                                <div className="text-lg font-bold text-green-600">
                                                    {stats.accuracy}%
                                                </div>
                                            </div>
                                            <div className="text-center">
                                                <div className="text-sm text-gray-500">Ответов</div>
                                                <div className="text-lg font-bold text-gray-800">
                                                    {stats.totalAnswers}
                                                </div>
                                            </div>
                                            
                                            {canDelete && (
                                                <Dialog>
                                                    <DialogTrigger asChild>
                                                        <Button
                                                            variant="ghost"
                                                            size="icon"
                                                            className="text-red-500 hover:text-red-700"
                                                            onClick={() => setUserToDelete(user)}
                                                        >
                                                            <Trash2 className="w-4 h-4" />
                                                        </Button>
                                                    </DialogTrigger>
                                                    <DialogContent>
                                                        <DialogHeader>
                                                            <DialogTitle className="flex items-center gap-2">
                                                                <AlertTriangle className="w-5 h-5 text-red-500" />
                                                                Удаление пользователя
                                                            </DialogTitle>
                                                        </DialogHeader>
                                                        <div className="py-4">
                                                            <p className="text-gray-700">
                                                                Вы действительно хотите удалить пользователя <strong>{user.full_name || user.email}</strong>?
                                                            </p>
                                                            <p className="text-sm text-red-600 mt-2">
                                                                ⚠️ Это действие нельзя отменить. Будут удалены все данные пользователя, включая прогресс выполнения заданий.
                                                            </p>
                                                        </div>
                                                        <DialogFooter>
                                                            <DialogClose asChild>
                                                                <Button variant="outline">Отмена</Button>
                                                            </DialogClose>
                                                            <Button 
                                                                variant="destructive" 
                                                                onClick={() => handleDeleteUser(user)}
                                                            >
                                                                Удалить пользователя
                                                            </Button>
                                                        </DialogFooter>
                                                    </DialogContent>
                                                </Dialog>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            );
                        })}

                        {filteredUsers.length === 0 && (
                            <div className="text-center py-8 text-gray-500">
                                Пользователи не найдены
                            </div>
                        )}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}