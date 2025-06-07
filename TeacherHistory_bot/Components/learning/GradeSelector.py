import React from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { GraduationCap } from "lucide-react";

export default function GradeSelector({ onGradeSelect }) {
  const grades = [5, 6, 7, 8, 9, 10, 11];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center p-6">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-2xl"
      >
        <Card className="shadow-xl border-0 bg-white/90 backdrop-blur-sm">
          <CardHeader className="text-center pb-8">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <GraduationCap className="w-8 h-8 text-white" />
            </div>
            <CardTitle className="text-3xl font-bold text-gray-900 mb-2">
              Добро пожаловать в HistoryLab!
            </CardTitle>
            <p className="text-gray-600 text-lg">
              Выберите свой класс, чтобы начать изучение истории и обществознания
            </p>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 md:grid-cols-4 gap-4">
              {grades.map((grade, index) => (
                <motion.div
                  key={grade}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Button
                    variant="outline"
                    className="w-full h-16 text-xl font-bold hover:bg-blue-50 hover:border-blue-300 hover:text-blue-700 transition-all duration-200"
                    onClick={() => onGradeSelect(grade)}
                  >
                    {grade}
                  </Button>
                </motion.div>
              ))}
            </div>
            <p className="text-center text-sm text-gray-500 mt-6">
              После выбора класса вы сможете изменить его только после завершения 80% программы
            </p>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}