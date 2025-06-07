import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { MessageCircle, Share, Star, ExternalLink } from 'lucide-react';

export default function TelegramHelper() {
  const [tg, setTg] = useState(null);
  const [isInTelegram, setIsInTelegram] = useState(false);
  const [supportedMethods, setSupportedMethods] = useState({
    switchInlineQuery: false,
    showPopup: false,
    showAlert: false,
    openTelegramLink: false
  });

  useEffect(() => {
    if (window.Telegram?.WebApp) {
      const telegramApp = window.Telegram.WebApp;
      setTg(telegramApp);
      setIsInTelegram(true);
      
      // Проверяем поддерживаемые методы
      setSupportedMethods({
        switchInlineQuery: typeof telegramApp.switchInlineQuery === 'function',
        showPopup: typeof telegramApp.showPopup === 'function',
        showAlert: typeof telegramApp.showAlert === 'function',
        openTelegramLink: typeof telegramApp.openTelegramLink === 'function'
      });
      
      // Настройка приложения для лучшего UX
      try {
        telegramApp.expand();
        telegramApp.enableClosingConfirmation();
      } catch (error) {
        console.log('Некоторые методы Telegram WebApp не поддерживаются:', error);
      }
    }
  }, []);

  const shareProgress = () => {
    if (tg && supportedMethods.switchInlineQuery) {
      try {
        const shareText = `🎓 Изучаю историю с помощью TeacherHelper! \n📊 Мой прогресс: уровень 1\n🏆 Присоединяйтесь!`;
        tg.switchInlineQuery(shareText);
      } catch (error) {
        console.error('Ошибка при попытке поделиться:', error);
        fallbackShare();
      }
    } else {
      fallbackShare();
    }
  };

  const sendFeedback = () => {
    if (tg && supportedMethods.showPopup) {
      try {
        tg.showPopup({
          title: 'Обратная связь',
          message: 'Хотите поделиться мнением о приложении?',
          buttons: [
            { type: 'ok', text: 'Да' },
            { type: 'cancel', text: 'Отмена' }
          ]
        }, (buttonId) => {
          if (buttonId === 'ok') {
            if (supportedMethods.openTelegramLink) {
              tg.openTelegramLink('https://t.me/your_bot_username');
            } else {
              fallbackFeedback();
            }
          }
        });
      } catch (error) {
        console.error('Ошибка при отправке обратной связи:', error);
        fallbackFeedback();
      }
    } else {
      fallbackFeedback();
    }
  };

  const rateApp = () => {
    if (tg && supportedMethods.showAlert) {
      try {
        tg.showAlert('Спасибо за использование TeacherHelper! Оцените нас в Telegram Store.');
      } catch (error) {
        console.error('Ошибка при показе рейтинга:', error);
        fallbackRate();
      }
    } else {
      fallbackRate();
    }
  };

  // Fallback функции для случаев, когда Telegram методы недоступны
  const fallbackShare = () => {
    if (navigator.share) {
      navigator.share({
        title: 'TeacherHelper',
        text: '🎓 Изучаю историю с помощью TeacherHelper! Присоединяйтесь!',
        url: window.location.href
      }).catch(console.error);
    } else {
      // Копируем ссылку в буфер обмена
      navigator.clipboard.writeText(window.location.href).then(() => {
        alert('Ссылка скопирована в буфер обмена!');
      }).catch(() => {
        alert('Поделитесь ссылкой: ' + window.location.href);
      });
    }
  };

  const fallbackFeedback = () => {
    const email = 'support@teacherhelper.ru';
    const subject = 'Обратная связь по TeacherHelper';
    const body = 'Здравствуйте! Хочу поделиться мнением о приложении TeacherHelper...';
    
    if (window.confirm('Хотите отправить обратную связь по email?')) {
      window.open(`mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`);
    }
  };

  const fallbackRate = () => {
    alert('Спасибо за использование TeacherHelper! Ваше мнение очень важно для нас.');
  };

  // Показываем компонент только если мы в Telegram или есть поддержка веб-функций
  if (!isInTelegram && !navigator.share) {
    return null;
  }

  return (
    <Card className="mt-6 border-blue-200 bg-blue-50">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-blue-900">
          <MessageCircle className="w-5 h-5" />
          {isInTelegram ? 'Telegram возможности' : 'Поделиться'}
          <Badge variant="secondary" className="bg-blue-100 text-blue-800">
            {isInTelegram ? 'Telegram' : 'Web'}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <Button
          onClick={shareProgress}
          variant="outline"
          className="w-full justify-start gap-2 border-blue-300 hover:bg-blue-100"
        >
          <Share className="w-4 h-4" />
          Поделиться прогрессом
        </Button>
        
        <Button
          onClick={sendFeedback}
          variant="outline"
          className="w-full justify-start gap-2 border-blue-300 hover:bg-blue-100"
        >
          <MessageCircle className="w-4 h-4" />
          Отправить отзыв
        </Button>
        
        <Button
          onClick={rateApp}
          variant="outline"
          className="w-full justify-start gap-2 border-blue-300 hover:bg-blue-100"
        >
          <Star className="w-4 h-4" />
          Оценить приложение
        </Button>

        {isInTelegram && (
          <div className="mt-4 p-3 bg-blue-100 rounded-lg">
            <p className="text-xs text-blue-800">
              🔧 Доступные методы: {Object.values(supportedMethods).filter(Boolean).length} из {Object.keys(supportedMethods).length}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}