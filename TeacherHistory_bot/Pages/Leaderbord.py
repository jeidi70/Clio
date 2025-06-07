import React, { useState, useEffect } from "react";
import { User } from "@/entities/User";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Trophy, Medal, Award, Crown, Star } from "lucide-react";
import { motion } from "framer-motion";

export default function LeaderboardPage() {
  const [users, setUsers] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLeaderboard();
  }, []);

  const loadLeaderboard = async () => {
    try {
      const userData = await User.me();
      setCurrentUser(userData);
      
      const allUsers = await User.list('-total_points');
      const filteredUsers = allUsers.filter(user => 
        user.total_points > 0 && user.grade
      ).slice(0, 50);
      
      setUsers(filteredUsers);
    } catch (error) {
      console.error("Ошибка загрузки рейтинга:", error);
    }
    setLoading(false);
  };

  const getRankIcon = (rank) => {
    if (rank === 1) return <Trophy className="w-6 h-6 text-yellow-500" />;
    if (rank === 2) return <Medal className="w-6 h-6 text-gray-400" />;
    if (rank === 3) return <Award className="w-6 h-6 text-amber-600" />;
    return <Star className="w-5 h-5 text-blue-500" />;
  };

  const getRankBadge = (rank) => {
    if (rank === 1) return "bg-gradient-to-r from-yellow-400 to-yellow-600 text-white";
    if (rank === 2) return "bg-gradient-to-r from-gray-300 to-gray-500 text-white";
    if (rank === 3) return "bg-gradient-to-r from-amber-400 to-amber-600 text-white";
    return "bg-blue-100 text-blue-800";
  };

  if (loading) {
    return (
      <div className="p-8 flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 p-6">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Рейтинг учеников</h1>
          <p className="text-gray-600">Лучшие ученики по количеству заработанных баллов</p>
        </motion.div>

        {/* Топ 3 */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {users.slice(0, 3).map((user, index) => (
            <motion.div
              key={user.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`relative ${index === 0 ? 'md:order-2' : index === 1 ? 'md:order-1' : 'md:order-3'}`}
            >
              <Card className={`text-center ${
                index === 0 ? 'scale-105 shadow-xl border-yellow-200' : 'shadow-lg'
              }`}>
                <CardHeader className="pb-4">
                  <div className="relative">
                    <div className={`w-20 h-20 mx-auto rounded-full flex items-center justify-center ${
                      index === 0 ? 'bg-gradient-to-r from-yellow-400 to-yellow-600' :
                      index === 1 ? 'bg-gradient-to-r from-gray-300 to-gray-500' :
                      'bg-gradient-to-r from-amber-400 to-amber-600'
                    }`}>
                      <span className="text-2xl font-bold text-white">
                        {user.full_name?.charAt(0) || 'У'}
                      </span>
                    </div>
                    <div className="absolute -top-2 -right-2">
                      {getRankIcon(index + 1)}
                    </div>
                  </div>
                  <CardTitle className="text-lg">{user.full_name || 'Ученик'}</CardTitle>
                  <Badge className={getRankBadge(index + 1)}>
                    {index + 1} место
                  </Badge>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Баллы:</span>
                      <span className="font-bold text-lg">{user.total_points || 0}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Уровень:</span>
                      <div className="flex items-center gap-1">
                        <Crown className="w-4 h-4 text-yellow-500" />
                        <span className="font-medium">{user.level || 1}</span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Класс:</span>
                      <span className="font-medium">{user.grade}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Остальной рейтинг */}
        <Card>
          <CardHeader>
            <CardTitle>Полный рейтинг</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {users.map((user, index) => (
                <motion.div
                  key={user.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className={`flex items-center justify-between p-4 rounded-lg border transition-colors ${
                    currentUser?.id === user.id 
                      ? 'border-blue-200 bg-blue-50' 
                      : 'border-gray-200 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center gap-4">
                    <Badge className={getRankBadge(index + 1)} variant="outline">
                      #{index + 1}
                    </Badge>
                    <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                      <span className="font-medium text-blue-600">
                        {user.full_name?.charAt(0) || 'У'}
                      </span>
                    </div>
                    <div>
                      <p className="font-medium">
                        {user.full_name || 'Ученик'}
                        {currentUser?.id === user.id && (
                          <span className="text-blue-600 ml-2">(Вы)</span>
                        )}
                      </p>
                      <p className="text-sm text-gray-500">{user.grade} класс</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-lg">{user.total_points || 0}</p>
                    <p className="text-sm text-gray-500">баллов</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}