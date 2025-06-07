import React, { useState, useEffect } from "react";
import { Topic, Assignment, UserProgress, User } from "@/entities/all";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  BookOpen, 
  Award,
  Target
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

import GradeSelector from "../components/learning/GradeSelector";
import TopicCard from "../components/learning/TopicCard";
import AssignmentModal from "../components/learning/AssignmentModal";
import LoginPrompt from "../components/auth/LoginPrompt";
import TelegramHelper from "../components/telegram/TelegramHelper";

export default function LearningPage() {
  const [user, setUser] = useState(undefined);
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [assignments, setAssignments] = useState([]);
  const [userProgress, setUserProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAssignment, setShowAssignment] = useState(false);
  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [isInTelegram, setIsInTelegram] = useState(false);

  useEffect(() => {
    // Проверяем, запущено ли приложение в Telegram
    if (window.Telegram?.WebApp) {
      setIsInTelegram(true);
      const tg = window.Telegram.WebApp;
      
      // Настройка Telegram WebApp для обучения
      tg.MainButton.hide(); // Скрываем главную кнопку на странице обучения
      tg.BackButton.hide(); // Скрываем кнопку назад на главной странице
    }

    const checkAuthAndLoad = async () => {
      setLoading(true);
      try {
        const userData = await User.me();
        setUser(userData);
        if (userData.grade) {
          await loadData(userData);
        } else {
          setLoading(false);
        }
      } catch (error) {
        setUser(null);
        setLoading(false);
      }
    };
    checkAuthAndLoad();
  }, []);

  const loadData = async (currentUser) => {
    try {
      const topicsData = await Topic.filter({ grade: currentUser.grade }, 'order_index');
      setTopics(topicsData);
      
      const progressData = await UserProgress.filter({ created_by: currentUser.email });
      setUserProgress(progressData);
    } catch (error) {
      console.error("Ошибка загрузки данных:", error);
    }
    setLoading(false);
  };

  const handleGradeSelect = async (grade) => {
    setLoading(true);
    await User.updateMyUserData({ grade });
    const updatedUser = await User.me();
    setUser(updatedUser);
    await loadData(updatedUser);

    // Уведомляем Telegram о достижении
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.showAlert(`🎓 Добро пожаловать в ${grade} класс! Начинаем изучение истории.`);
    }
  };

  const handleTopicSelect = async (topic) => {
    setSelectedTopic(topic);
    const topicAssignments = await Assignment.filter({ topic_id: topic.id });
    setAssignments(topicAssignments);

    // Показываем кнопку "Назад" в Telegram
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.BackButton.show();
      tg.BackButton.onClick(() => {
        setSelectedTopic(null);
        tg.BackButton.hide();
      });
    }
  };

  const handleAssignmentStart = (assignment) => {
    setSelectedAssignment(assignment);
    setShowAssignment(true);
  };

  const handleAssignmentComplete = async (assignment, userAnswer, isCorrect, pointsEarned) => {
    await UserProgress.create({
      topic_id: selectedTopic.id,
      assignment_id: assignment.id,
      user_answer: userAnswer,
      is_correct: isCorrect,
      points_earned: pointsEarned
    });

    const newTotalPoints = (user.total_points || 0) + pointsEarned;
    await User.updateMyUserData({ 
      total_points: newTotalPoints,
      level: Math.floor(newTotalPoints / 100) + 1
    });

    // Показываем достижение в Telegram
    if (window.Telegram?.WebApp && isCorrect) {
      window.Telegram.WebApp.showAlert(`🎉 Правильно! +${pointsEarned} баллов`);
    }

    setShowAssignment(false);
    loadData(user);
  };

  const isTopicCompleted = (topicId) => {
    return userProgress.some(p => p.topic_id === topicId && p.is_correct);
  };

  const getTopicProgress = (topicId) => {
    const topicAssignments = assignments.filter(a => a.topic_id === topicId);
    const completedAssignments = userProgress.filter(p => 
      p.topic_id === topicId && p.is_correct
    );
    return topicAssignments.length > 0 ? 
      (completedAssignments.length / topicAssignments.length) * 100 : 0;
  };

  if (loading || user === undefined) {
    return (
      <div className="p-8 flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black"></div>
      </div>
    );
  }

  if (user === null) {
    return <LoginPrompt />;
  }
  
  if (!user.grade) {
    return <GradeSelector onGradeSelect={handleGradeSelect} />;
  }

  const historyTopics = topics.filter(t => t.subject === 'history');
  const socialStudiesTopics = topics.filter(t => t.subject === 'social_studies');

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Обучение • {user.grade} класс
                {isInTelegram && <Badge variant="outline" className="ml-2 text-blue-600">Telegram</Badge>}
              </h1>
              <p className="text-gray-600">Изучайте историю и обществознание в своем темпе</p>
            </div>
            <div className="flex items-center gap-4">
              <Badge variant="outline" className="flex items-center gap-2 px-4 py-2">
                <Award className="w-4 h-4 text-yellow-500" />
                Уровень {user.level || 1}
              </Badge>
              <Badge variant="outline" className="flex items-center gap-2 px-4 py-2">
                <Target className="w-4 h-4 text-blue-500" />
                {user.total_points || 0} баллов
              </Badge>
            </div>
          </div>
        </motion.div>

        {!selectedTopic ? (
          <>
            <Tabs defaultValue="history" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="history">История</TabsTrigger>
                <TabsTrigger value="social_studies">Обществознание</TabsTrigger>
              </TabsList>
              <TabsContent value="history">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
                  <AnimatePresence>
                    {historyTopics.map((topic, index) => (
                      <TopicCard
                        key={topic.id}
                        topic={topic}
                        index={index}
                        isCompleted={isTopicCompleted(topic.id)}
                        progress={getTopicProgress(topic.id)}
                        onSelect={handleTopicSelect}
                      />
                    ))}
                  </AnimatePresence>
                </div>
              </TabsContent>
              <TabsContent value="social_studies">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
                  <AnimatePresence>
                    {socialStudiesTopics.map((topic, index) => (
                      <TopicCard
                        key={topic.id}
                        topic={topic}
                        index={index}
                        isCompleted={isTopicCompleted(topic.id)}
                        progress={getTopicProgress(topic.id)}
                        onSelect={handleTopicSelect}
                      />
                    ))}
                  </AnimatePresence>
                </div>
              </TabsContent>
            </Tabs>
            
            {isInTelegram && <TelegramHelper />}
          </>
        ) : (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <Button
              variant="outline"
              onClick={() => {
                setSelectedTopic(null);
                if (window.Telegram?.WebApp) {
                  window.Telegram.WebApp.BackButton.hide();
                }
              }}
              className="mb-6"
            >
              ← Назад к темам
            </Button>

            <div className="grid lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <Card className="mb-6">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-3">
                      <BookOpen className="w-6 h-6 text-blue-600" />
                      {selectedTopic.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="prose max-w-none">
                      <p className="whitespace-pre-wrap">{selectedTopic.content}</p>
                    </div>
                    {selectedTopic.video_url && (
                      <div className="mt-6">
                        <Button variant="outline" className="flex items-center gap-2">
                          <BookOpen className="w-4 h-4" />
                          Посмотреть видеоурок
                        </Button>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>

              <div className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Задания по теме</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {assignments.map((assignment) => {
                      const isCompleted = userProgress.some(p => 
                        p.assignment_id === assignment.id && p.is_correct
                      );
                      
                      return (
                        <div
                          key={assignment.id}
                          className={`p-4 rounded-lg border transition-colors cursor-pointer ${
                            isCompleted 
                              ? 'border-green-200 bg-green-50' 
                              : 'border-gray-200 hover:border-blue-300 hover:bg-blue-50'
                          }`}
                          onClick={() => !isCompleted && handleAssignmentStart(assignment)}
                        >
                          <div className="flex items-center justify-between">
                            <div>
                              <h4 className="font-medium">{assignment.title}</h4>
                              <p className="text-sm text-gray-500 capitalize">
                                {assignment.type} • {assignment.points} баллов
                              </p>
                            </div>
                            {isCompleted ? (
                              <Award className="w-5 h-5 text-green-600" />
                            ) : (
                              <Target className="w-5 h-5 text-gray-400" />
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </CardContent>
                </Card>
              </div>
            </div>
          </motion.div>
        )}

        <AssignmentModal
          isOpen={showAssignment}
          assignment={selectedAssignment}
          onClose={() => setShowAssignment(false)}
          onComplete={handleAssignmentComplete}
        />
      </div>
    </div>
  );
}