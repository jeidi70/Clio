import React from 'react';
import { User } from '@/entities/User';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';
import { GraduationCap, LogIn } from 'lucide-react';

export default function LoginPrompt() {
  const handleLogin = async () => {
    try {
      await User.login();
    } catch (error) {
      console.error("Ошибка входа:", error);
    }
  };

  return (
    <div className="w-full h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <div className="w-20 h-20 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl">
          <GraduationCap className="w-10 h-10 text-white" />
        </div>
        <h1 className="text-5xl font-bold text-gray-900 mb-2">TeacherHelper</h1>
        <p className="text-xl text-gray-600 mb-8">Ваш персональный помощник в преподавании истории и обществознания</p>
        <Button
          onClick={handleLogin}
          size="lg"
          className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-full px-8 py-6 text-lg flex items-center gap-3 transition-transform transform hover:scale-105 shadow-lg"
        >
          <LogIn className="w-5 h-5" />
          Войти через Google
        </Button>
        <p className="text-sm text-gray-500 mt-6">
          Безопасный вход через Google Account
        </p>
      </motion.div>
    </div>
  );
}