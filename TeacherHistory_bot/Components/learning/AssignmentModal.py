import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, XCircle, Send, Brain } from "lucide-react";
import { InvokeLLM } from "@/integrations/Core";

export default function AssignmentModal({ isOpen, assignment, onClose, onComplete }) {
  const [selectedAnswer, setSelectedAnswer] = useState("");
  const [textAnswer, setTextAnswer] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    if (!assignment) return;
    
    setIsSubmitting(true);
    const userAnswer = assignment.type === 'test' ? selectedAnswer : textAnswer;
    
    let isCorrect = false;
    let pointsEarned = 0;
    let aiFeedback = "";

    if (assignment.type === 'test') {
      isCorrect = userAnswer === assignment.correct_answer;
      pointsEarned = isCorrect ? assignment.points : 0;
    } else {
      // Для развернутых ответов используем ИИ для проверки
      try {
        const aiResult = await InvokeLLM({
          prompt: `Проверь ответ ученика на задание по истории/обществознанию.
          
          Задание: ${assignment.question}
          Правильный ответ: ${assignment.correct_answer}
          Ответ ученика: ${userAnswer}
          
          Оцени ответ по критериям:
          1. Правильность фактов
          2. Полнота ответа
          3. Структура изложения
          
          Выставь баллы от 0 до ${assignment.points} и дай обратную связь.`,
          response_json_schema: {
            type: "object",
            properties: {
              is_correct: { type: "boolean" },
              points_earned: { type: "number" },
              feedback: { type: "string" }
            }
          }
        });
        
        isCorrect = aiResult.is_correct;
        pointsEarned = aiResult.points_earned;
        aiFeedback = aiResult.feedback;
      } catch (error) {
        // Fallback: простая проверка
        isCorrect = userAnswer.length > 50;
        pointsEarned = isCorrect ? Math.floor(assignment.points * 0.7) : 0;
        aiFeedback = "Проверка выполнена автоматически. Обратитесь к учителю для подробной оценки.";
      }
    }

    setResult({
      isCorrect,
      pointsEarned,
      aiFeedback,
      userAnswer
    });
    
    setShowResult(true);
    setIsSubmitting(false);
  };

  const handleComplete = () => {
    onComplete(assignment, result.userAnswer, result.isCorrect, result.pointsEarned);
    resetModal();
  };

  const resetModal = () => {
    setSelectedAnswer("");
    setTextAnswer("");
    setShowResult(false);
    setResult(null);
  };

  const handleClose = () => {
    resetModal();
    onClose();
  };

  if (!assignment) return null;

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <Brain className="w-4 h-4 text-blue-600" />
            </div>
            {assignment.title}
            <Badge variant="outline" className="ml-auto">
              {assignment.points} баллов
            </Badge>
          </DialogTitle>
        </DialogHeader>

        <AnimatePresence mode="wait">
          {!showResult ? (
            <motion.div
              key="question"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="space-y-6"
            >
              <Card>
                <CardContent className="p-6">
                  <div className="mb-4">
                    <div className="flex gap-2 mb-3">
                      <Badge variant="outline">
                        {assignment.exam_format?.toUpperCase()}
                      </Badge>
                      <Badge variant="outline" className="capitalize">
                        {assignment.difficulty}
                      </Badge>
                    </div>
                    <p className="text-gray-700 whitespace-pre-wrap">
                      {assignment.question}
                    </p>
                  </div>

                  {assignment.type === 'test' && assignment.options ? (
                    <div className="space-y-3">
                      {assignment.options.map((option, index) => (
                        <label
                          key={index}
                          className={`block p-4 rounded-lg border cursor-pointer transition-colors ${
                            selectedAnswer === option
                              ? 'border-blue-500 bg-blue-50'
                              : 'border-gray-200 hover:border-gray-300'
                          }`}
                        >
                          <input
                            type="radio"
                            name="answer"
                            value={option}
                            checked={selectedAnswer === option}
                            onChange={(e) => setSelectedAnswer(e.target.value)}
                            className="sr-only"
                          />
                          <span>{option}</span>
                        </label>
                      ))}
                    </div>
                  ) : (
                    <Textarea
                      placeholder="Введите ваш развернутый ответ..."
                      value={textAnswer}
                      onChange={(e) => setTextAnswer(e.target.value)}
                      className="min-h-[200px]"
                    />
                  )}
                </CardContent>
              </Card>

              <div className="flex justify-end gap-3">
                <Button variant="outline" onClick={handleClose}>
                  Отмена
                </Button>
                <Button
                  onClick={handleSubmit}
                  disabled={
                    isSubmitting || 
                    (assignment.type === 'test' ? !selectedAnswer : !textAnswer.trim())
                  }
                  className="flex items-center gap-2"
                >
                  {isSubmitting ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                      Проверка...
                    </>
                  ) : (
                    <>
                      <Send className="w-4 h-4" />
                      Отправить ответ
                    </>
                  )}
                </Button>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="result"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-6"
            >
              <Card className={`border-2 ${
                result.isCorrect ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'
              }`}>
                <CardContent className="p-6">
                  <div className="flex items-center gap-3 mb-4">
                    {result.isCorrect ? (
                      <CheckCircle2 className="w-8 h-8 text-green-600" />
                    ) : (
                      <XCircle className="w-8 h-8 text-red-600" />
                    )}
                    <div>
                      <h3 className="text-xl font-bold">
                        {result.isCorrect ? 'Правильно!' : 'Неправильно'}
                      </h3>
                      <p className="text-lg">
                        Получено баллов: <span className="font-bold">{result.pointsEarned}</span> из {assignment.points}
                      </p>
                    </div>
                  </div>

                  {result.aiFeedback && (
                    <div className="p-4 bg-white rounded-lg border">
                      <h4 className="font-medium mb-2">Обратная связь:</h4>
                      <p className="text-gray-700">{result.aiFeedback}</p>
                    </div>
                  )}

                  {assignment.explanation && (
                    <div className="p-4 bg-blue-50 rounded-lg border border-blue-200 mt-4">
                      <h4 className="font-medium text-blue-900 mb-2">Объяснение:</h4>
                      <p className="text-blue-800">{assignment.explanation}</p>
                    </div>
                  )}
                </CardContent>
              </Card>

              <div className="flex justify-end">
                <Button onClick={handleComplete} className="bg-green-600 hover:bg-green-700">
                  Продолжить обучение
                </Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </DialogContent>
    </Dialog>
  );
}