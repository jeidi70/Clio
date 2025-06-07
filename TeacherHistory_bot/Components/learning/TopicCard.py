
import React from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { BookOpen, CheckCircle2, Crown, Lock, Play } from "lucide-react";

export default function TopicCard({ topic, index, isCompleted, progress, onSelect }) {
  const handleSelect = () => {
    if (topic.is_premium) {
      alert("Это премиум-контент. Скоро здесь появится возможность оплаты.");
      return;
    }
    onSelect(topic);
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      whileHover={{ y: -5 }}
      className={`cursor-pointer ${topic.is_premium ? 'opacity-80' : ''}`}
      onClick={handleSelect}
    >
      <Card className={`h-full transition-all duration-300 hover:shadow-xl relative overflow-hidden ${
        isCompleted 
          ? 'border-green-200 bg-gradient-to-br from-green-50 to-white' 
          : 'border-gray-200 hover:border-gray-300 bg-gradient-to-br from-white to-gray-50'
      }`}>
        {topic.is_premium && (
          <div className="absolute top-2 right-2 p-1.5 bg-yellow-400 rounded-full text-white shadow-lg">
            <Lock className="w-4 h-4" />
          </div>
        )}
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                isCompleted 
                  ? 'bg-green-100 text-green-600' 
                  : 'bg-blue-100 text-blue-600'
              }`}>
                {isCompleted ? (
                  <CheckCircle2 className="w-5 h-5" />
                ) : (
                  <BookOpen className="w-5 h-5" />
                )}
              </div>
              <div>
                <CardTitle className="text-lg leading-tight">{topic.title}</CardTitle>
                <p className="text-sm text-gray-500 capitalize">
                  {topic.subject === 'history' ? 'История' : 'Обществознание'}
                </p>
              </div>
            </div>
            {topic.is_premium && (
              <Crown className="w-5 h-5 text-yellow-500" />
            )}
          </div>
        </CardHeader>
        
        <CardContent>
          <p className="text-gray-600 text-sm mb-4 line-clamp-3">
            {topic.content?.substring(0, 120)}...
          </p>
          
          <div className="space-y-3">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-500">Прогресс</span>
              <span className="font-medium">{Math.round(progress)}%</span>
            </div>
            <Progress value={progress} className="h-2" />
            
            <div className="flex items-center justify-between">
              <Badge variant="outline" className="text-xs">
                +{topic.points_reward} баллов
              </Badge>
              {topic.video_url && (
                <div className="flex items-center gap-1 text-xs text-blue-600">
                  <Play className="w-3 h-3" />
                  Видео
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
