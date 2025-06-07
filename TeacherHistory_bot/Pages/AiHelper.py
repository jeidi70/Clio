import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Brain, User, Sparkles, Send } from 'lucide-react';
import { InvokeLLM } from '@/integrations/Core';

export default function AIHelperPage() {
  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: 'Здравствуйте! Я Clio, ваш ИИ-помощник по истории и обществознанию. Чем могу помочь?',
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const aiResponse = await InvokeLLM({
        prompt: `Ты — ИИ-ассистент Clio, эксперт по истории и обществознанию. Отвечай на вопросы учеников дружелюбно, точно и понятно.
        
        Вопрос ученика: "${input}"`,
      });
      
      const aiMessage = { sender: 'ai', text: aiResponse };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = { sender: 'ai', text: 'К сожалению, произошла ошибка. Попробуйте еще раз.' };
      setMessages(prev => [...prev, errorMessage]);
      console.error("Ошибка ИИ-помощника:", error);
    }
    
    setIsLoading(false);
  };

  return (
    <div className="p-6 h-full flex flex-col">
      <Card className="flex-1 flex flex-col shadow-lg">
        <CardHeader className="border-b">
          <CardTitle className="flex items-center gap-3">
            <Sparkles className="w-6 h-6 text-yellow-500" />
            ИИ-Помощник
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
          <AnimatePresence>
            {messages.map((msg, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex items-start gap-3 ${
                  msg.sender === 'user' ? 'justify-end' : ''
                }`}
              >
                {msg.sender === 'ai' && (
                  <div className="w-8 h-8 rounded-full bg-black text-white flex items-center justify-center flex-shrink-0">
                    <Brain className="w-4 h-4" />
                  </div>
                )}
                <div
                  className={`max-w-xl p-3 rounded-xl whitespace-pre-wrap ${
                    msg.sender === 'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100'
                  }`}
                >
                  {msg.text}
                </div>
                {msg.sender === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center flex-shrink-0">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </motion.div>
            ))}
            {isLoading && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-start gap-3"
              >
                 <div className="w-8 h-8 rounded-full bg-black text-white flex items-center justify-center flex-shrink-0">
                    <Brain className="w-4 h-4" />
                  </div>
                <div className="p-3 bg-gray-100 rounded-xl">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </CardContent>
        <div className="p-4 border-t">
          <div className="flex gap-3">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Спросите что-нибудь о Древнем Риме..."
              disabled={isLoading}
            />
            <Button onClick={handleSend} disabled={isLoading}>
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}