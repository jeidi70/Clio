import React, { useState, useEffect } from 'react';
import { Topic, User } from '@/entities/all';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Crown, Lock, Star, Zap, BookOpen, Play } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function PremiumPage() {
  const [user, setUser] = useState(null);
  const [premiumTopics, setPremiumTopics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const userData = await User.me();
      setUser(userData);
      
      const topics = await Topic.filter({ is_premium: true });
      setPremiumTopics(topics);
    } catch (error) {
      console.error("Ошибка загрузки данных:", error);
    }
    setLoading(false);
  };

  const getPremiumTopicsBySubject = (subject) => {
    return premiumTopics.filter(t => t.subject === subject);
  };

  const handlePurchase = () => {
    alert("Функция покупки будет доступна в следующих версиях. Пока что наслаждайтесь бесплатным контентом!");
  };

  if (loading) {
    return (
      <div className="p-8 flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6 bg-gradient-to-br from-yellow-50 via-white to-orange-50">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="w-20 h-20 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
            <Crown className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Премиум материалы</h1>
          <p className="text-xl text-gray-600 mb-8">
            Получите доступ к эксклюзивному контенту и дополнительным материалам
          </p>
        </motion.div>

        {/* Преимущества премиума */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            <Card className="border-yellow-200 bg-gradient-to-br from-yellow-50 to-white">
              <CardContent className="p-6 text-center">
                <Star className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
                <h3 className="text-lg font-bold mb-2">Эксклюзивные темы</h3>
                <p className="text-gray-600">Доступ к дополнительным темам и углубленным материалам</p>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <Card className="border-yellow-200 bg-gradient-to-br from-yellow-50 to-white">
              <CardContent className="p-6 text-center">
                <Zap className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
                <h3 className="text-lg font-bold mb-2">Видеоуроки HD</h3>
                <p className="text-gray-600">Качественные видеоматериалы от экспертов</p>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
            <Card className="border-yellow-200 bg-gradient-to-br from-yellow-50 to-white">
              <CardContent className="p-6 text-center">
                <BookOpen className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
                <h3 className="text-lg font-bold mb-2">Дополнительные материалы</h3>
                <p className="text-gray-600">Конспекты, схемы и дополнительные задания</p>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Кнопка покупки */}
        <div className="text-center mb-12">
          <Card className="border-yellow-300 bg-gradient-to-r from-yellow-100 to-orange-100 max-w-md mx-auto">
            <CardContent className="p-8">
              <Crown className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
              <h3 className="text-2xl font-bold mb-2">Премиум доступ</h3>
              <p className="text-gray-600 mb-6">Откройте все возможности TeacherHelper</p>
              <div className="text-3xl font-bold text-yellow-600 mb-4">
                299 ₽ <span className="text-lg text-gray-500">/месяц</span>
              </div>
              <Button 
                className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 hover:from-yellow-500 hover:to-orange-600 text-white font-bold py-3"
                onClick={handlePurchase}
              >
                <Crown className="w-5 h-5 mr-2" />
                Получить премиум
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Премиум контент */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Crown className="w-6 h-6 text-yellow-500" />
              Премиум материалы
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="history" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="history">История</TabsTrigger>
                <TabsTrigger value="social_studies">Обществознание</TabsTrigger>
              </TabsList>
              
              <TabsContent value="history">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
                  {getPremiumTopicsBySubject('history').map((topic, index) => (
                    <motion.div
                      key={topic.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Card className="border-yellow-200 bg-gradient-to-br from-yellow-50 to-white relative overflow-hidden">
                        <div className="absolute top-2 right-2 p-1.5 bg-yellow-400 rounded-full text-white shadow-lg">
                          <Crown className="w-4 h-4" />
                        </div>
                        <CardHeader className="pb-3">
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-xl bg-yellow-100 text-yellow-600 flex items-center justify-center">
                              <Lock className="w-5 h-5" />
                            </div>
                            <div>
                              <CardTitle className="text-base leading-tight">{topic.title}</CardTitle>
                              <p className="text-sm text-gray-500">История • {topic.grade} класс</p>
                            </div>
                          </div>
                        </CardHeader>
                        
                        <CardContent>
                          <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                            {topic.content?.substring(0, 120)}...
                          </p>
                          
                          <div className="flex items-center justify-between">
                            <Badge className="bg-yellow-100 text-yellow-800 text-xs">
                              Премиум
                            </Badge>
                            {topic.video_url && (
                              <div className="flex items-center gap-1 text-xs text-yellow-600">
                                <Play className="w-3 h-3" />
                                Видео HD
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
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
                  {getPremiumTopicsBySubject('social_studies').map((topic, index) => (
                    <motion.div
                      key={topic.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Card className="border-yellow-200 bg-gradient-to-br from-yellow-50 to-white relative overflow-hidden">
                        <div className="absolute top-2 right-2 p-1.5 bg-yellow-400 rounded-full text-white shadow-lg">
                          <Crown className="w-4 h-4" />
                        </div>
                        <CardHeader className="pb-3">
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-xl bg-yellow-100 text-yellow-600 flex items-center justify-center">
                              <Lock className="w-5 h-5" />
                            </div>
                            <div>
                              <CardTitle className="text-base leading-tight">{topic.title}</CardTitle>
                              <p className="text-sm text-gray-500">Обществознание • {topic.grade} класс</p>
                            </div>
                          </div>
                        </CardHeader>
                        
                        <CardContent>
                          <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                            {topic.content?.substring(0, 120)}...
                          </p>
                          
                          <div className="flex items-center justify-between">
                            <Badge className="bg-yellow-100 text-yellow-800 text-xs">
                              Премиум
                            </Badge>
                            {topic.video_url && (
                              <div className="flex items-center gap-1 text-xs text-yellow-600">
                                <Play className="w-3 h-3" />
                                Видео HD
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

            {premiumTopics.length === 0 && (
              <div className="text-center py-12">
                <Crown className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-500 mb-2">
                  Премиум материалы скоро появятся
                </h3>
                <p className="text-gray-400">
                  Мы работаем над созданием эксклюзивного контента для вас
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}