import React, { useState, useEffect } from 'react';
import { User, UserProgress, Topic, Assignment } from '@/entities/all';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BarChart3, Trophy, Target, BookOpen, CheckCircle2, XCircle, Clock } from 'lucide-react';
import { motion } from 'framer-motion';

export default function ProgressPage() {
  const [user, setUser] = useState(null);
  const [userProgress, setUserProgress] = useState([]);
  const [topics, setTopics] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const userData = await User.me();
      setUser(userData);
      
      const [progressData, topicsData, assignmentsData] = await Promise.all([
        UserProgress.filter({ created_by: userData.email }),
        Topic.filter({ grade: userData.grade }),
        Assignment.list()
      ]);
      
      setUserProgress(progressData);
      setTopics(topicsData);
      setAssignments(assignmentsData);
    } catch (error) {
      console.error("Ошибка загрузки данных:", error);
    }
    setLoading(false);
  };

  const getProgressStats = () => {
    const totalAnswers = userProgress.length;
    const correctAnswers = userProgress.filter(p => p.is_correct).length;
    const totalPoints = user?.total_points || 0;
    const level = user?.level || 1;
    const accuracy = totalAnswers > 0 ? Math.round((correctAnswers / totalAnswers) * 100) : 0;
    
    return { totalAnswers, correctAnswers, totalPoints, level, accuracy };
  };

  const getSubjectProgress = (subject) => {
    const subjectTopics = topics.filter(t => t.subject === subject);
    const completedTopics = subjectTopics.filter(topic => 
      userProgress.some(p => p.topic_id === topic.id && p.is_correct)
    );
    
    return {
      total: subjectTopics.length,
      completed: completedTopics.length,
      percentage: subjectTopics.length > 0 ? Math.round((completedTopics.length / subjectTopics.length) * 100) : 0
    };
  };

  const getRecentActivity = () => {
    return userProgress
      .sort((a, b) => new Date(b.created_date) - new Date(a.created_date))
      .slice(0, 10)
      .map(progress => {
        const topic = topics.find(t => t.id === progress.topic_id);
        const assignment = assignments.find(a => a.id === progress.assignment_id);
        return { ...progress, topic, assignment };
      });
  };

  if (loading) {
    return (
      <div className="p-8 flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!user) {
    return <div className="p-8 text-center">Необходимо войти в систему</div>;
  }

  const stats = getProgressStats();
  const historyProgress = getSubjectProgress('history');
  const socialStudiesProgress = getSubjectProgress('social_studies');
  const recentActivity = getRecentActivity();

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Мой прогресс</h1>
          <p className="text-gray-600">Отслеживайте свои достижения и прогресс в обучении</p>
        </motion.div>

        {/* Основная статистика */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center gap-3">
                  <Trophy className="w-8 h-8 text-yellow-500" />
                  <div>
                    <h3 className="text-2xl font-bold">{stats.level}</h3>
                    <p className="text-gray-600">Уровень</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center gap-3">
                  <Target className="w-8 h-8 text-blue-500" />
                  <div>
                    <h3 className="text-2xl font-bold">{stats.totalPoints}</h3>
                    <p className="text-gray-600">Баллов</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center gap-3">
                  <BarChart3 className="w-8 h-8 text-green-500" />
                  <div>
                    <h3 className="text-2xl font-bold">{stats.accuracy}%</h3>
                    <p className="text-gray-600">Точность</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center gap-3">
                  <BookOpen className="w-8 h-8 text-purple-500" />
                  <div>
                    <h3 className="text-2xl font-bold">{stats.totalAnswers}</h3>
                    <p className="text-gray-600">Заданий выполнено</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Прогресс по предметам */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Прогресс по предметам</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium">История</h4>
                    <span className="text-sm text-gray-500">
                      {historyProgress.completed}/{historyProgress.total} тем
                    </span>
                  </div>
                  <Progress value={historyProgress.percentage} className="h-3" />
                  <p className="text-sm text-gray-500 mt-1">{historyProgress.percentage}% завершено</p>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium">Обществознание</h4>
                    <span className="text-sm text-gray-500">
                      {socialStudiesProgress.completed}/{socialStudiesProgress.total} тем
                    </span>
                  </div>
                  <Progress value={socialStudiesProgress.percentage} className="h-3" />
                  <p className="text-sm text-gray-500 mt-1">{socialStudiesProgress.percentage}% завершено</p>
                </div>
              </CardContent>
            </Card>

            {/* Последние достижения */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Последние достижения</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {recentActivity.map((activity, index) => (
                    <div key={activity.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                        activity.is_correct ? 'bg-green-100' : 'bg-red-100'
                      }`}>
                        {activity.is_correct ? (
                          <CheckCircle2 className="w-5 h-5 text-green-600" />
                        ) : (
                          <XCircle className="w-5 h-5 text-red-600" />
                        )}
                      </div>
                      <div className="flex-1">
                        <h4 className="font-medium text-sm">
                          {activity.assignment?.title || 'Задание'}
                        </h4>
                        <p className="text-sm text-gray-500">
                          {activity.topic?.title || 'Тема'} • {activity.points_earned || 0} баллов
                        </p>
                      </div>
                      <div className="text-sm text-gray-400">
                        {new Date(activity.created_date).toLocaleDateString()}
                      </div>
                    </div>
                  ))}
                  
                  {recentActivity.length === 0 && (
                    <p className="text-gray-500 text-center py-4">
                      Пока нет выполненных заданий
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Боковая панель с дополнительной информацией */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Ваши достижения</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Уровень</span>
                    <Badge variant="secondary" className="bg-yellow-100 text-yellow-800">
                      {stats.level}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Общий класс</span>
                    <Badge variant="outline">{user.grade}</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Точность ответов</span>
                    <span className="font-medium">{stats.accuracy}%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Всего баллов</span>
                    <span className="font-bold text-blue-600">{stats.totalPoints}</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Следующая цель</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600 mb-2">
                    {Math.ceil(stats.level * 100) - stats.totalPoints}
                  </div>
                  <p className="text-sm text-gray-600">
                    баллов до уровня {stats.level + 1}
                  </p>
                  <Progress 
                    value={(stats.totalPoints % 100)} 
                    className="h-2 mt-3" 
                  />
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}