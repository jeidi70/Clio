import React from "react";
import { Link, useLocation } from "react-router-dom";
import { createPageUrl } from "@/utils";
import { 
  BookOpen, 
  Trophy, 
  BarChart3, 
  Brain, 
  Settings,
  GraduationCap,
  User,
  Crown
} from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  SidebarFooter,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { Badge } from "@/components/ui/badge";
import { User as UserEntity } from "@/entities/User";

export default function Layout({ children, currentPageName }) {
  const location = useLocation();
  const [user, setUser] = React.useState(null);
  const [telegramUser, setTelegramUser] = React.useState(null);
  const [telegramAvailable, setTelegramAvailable] = React.useState(false);

  const navigationItems = [
    {
      title: "Обучение",
      url: createPageUrl("Learning"),
      icon: BookOpen,
    },
    {
      title: "Рейтинг",
      url: createPageUrl("Leaderboard"),
      icon: Trophy,
    },
    {
      title: "Мой прогресс",
      url: createPageUrl("Progress"),
      icon: BarChart3,
    },
    {
      title: "Премиум",
      url: createPageUrl("Premium"),
      icon: Crown,
    },
    {
      title: "ИИ-Помощник",
      url: createPageUrl("AIHelper"),
      icon: Brain,
    },
    {
      title: "Профиль",
      url: createPageUrl("Profile"),
      icon: User,
    }
  ];
  
  const adminNav = {
    title: "Админ-панель",
    url: createPageUrl("AdminPanel"),
    icon: Settings,
  };

  React.useEffect(() => {
    // Загружаем Telegram Web Apps SDK
    const script = document.createElement('script');
    script.src = 'https://telegram.org/js/telegram-web-app.js';
    script.async = true;
    script.onload = () => {
      // Инициализируем Telegram Web App
      if (window.Telegram?.WebApp) {
        const tg = window.Telegram.WebApp;
        setTelegramAvailable(true);
        
        try {
          tg.ready();
          
          // Настраиваем тему (с проверкой поддержки)
          if (typeof tg.setHeaderColor === 'function') {
            tg.setHeaderColor('#ffffff');
          }
          if (typeof tg.setBackgroundColor === 'function') {
            tg.setBackgroundColor('#f8fafc');
          }
          
          // Получаем данные пользователя Telegram
          if (tg.initDataUnsafe?.user) {
            setTelegramUser(tg.initDataUnsafe.user);
          }

          // Настраиваем главную кнопку (с проверкой поддержки)
          if (tg.MainButton && typeof tg.MainButton.setText === 'function') {
            tg.MainButton.text = "Начать обучение";
            tg.MainButton.color = "#000000";
            tg.MainButton.textColor = "#ffffff";
            
            // Обработчик нажатия на главную кнопку
            if (typeof tg.MainButton.onClick === 'function') {
              tg.MainButton.onClick(() => {
                if (location.pathname !== createPageUrl("Learning")) {
                  window.location.href = createPageUrl("Learning");
                }
              });
            }

            // Показываем кнопку, если не на странице обучения
            if (location.pathname !== createPageUrl("Learning")) {
              if (typeof tg.MainButton.show === 'function') {
                tg.MainButton.show();
              }
            } else {
              if (typeof tg.MainButton.hide === 'function') {
                tg.MainButton.hide();
              }
            }
          }
        } catch (error) {
          console.log('Некоторые методы Telegram WebApp не поддерживаются:', error);
        }
      }
    };
    
    script.onerror = () => {
      console.log('Не удалось загрузить Telegram WebApp SDK');
      setTelegramAvailable(false);
    };
    
    document.head.appendChild(script);

    const loadUserData = async () => {
      try {
        const userData = await UserEntity.me();
        setUser(userData);
      } catch (error) {
        console.log("Пользователь не авторизован");
      }
    };
    
    loadUserData();

    return () => {
      // Очистка при размонтировании
      if (document.head.contains(script)) {
        document.head.removeChild(script);
      }
    };
  }, [location.pathname]);

  const finalNavItems = [...navigationItems];
  if (user?.role === 'admin') {
    finalNavItems.push(adminNav);
  }

  return (
    <>
      {/* Добавляем мета-теги для Telegram Web Apps */}
      <div style={{ display: 'none' }}>
        <meta name="telegram-web-app" content="1" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
      </div>
      
      <SidebarProvider>
        <div className="min-h-screen flex w-full bg-gradient-to-br from-gray-50 via-white to-gray-100">
          <Sidebar className="border-r border-gray-200 bg-white/80 backdrop-blur-sm">
            <SidebarHeader className="border-b border-gray-200 p-6">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg">
                  <GraduationCap className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h2 className="font-bold text-gray-900 text-lg">TeacherHelper</h2>
                  <p className="text-sm text-gray-600">
                    Умный помощник педагога
                  </p>
                </div>
              </div>
            </SidebarHeader>
            
            <SidebarContent className="p-3">
              <SidebarGroup>
                <SidebarGroupLabel className="text-xs font-semibold text-gray-500 uppercase tracking-wider px-3 py-2">
                  Навигация
                </SidebarGroupLabel>
                <SidebarGroupContent>
                  <SidebarMenu>
                    {finalNavItems.map((item) => (
                      <SidebarMenuItem key={item.title}>
                        <SidebarMenuButton 
                          asChild 
                          className={`hover:bg-gray-100 hover:text-gray-900 transition-all duration-200 rounded-xl mb-1 ${
                            location.pathname === item.url ? 'bg-gray-100 text-gray-900 shadow-sm' : ''
                          }`}
                        >
                          <Link to={item.url} className="flex items-center gap-3 px-4 py-3">
                            <item.icon className="w-5 h-5 text-gray-500" />
                            <span className="font-medium">{item.title}</span>
                          </Link>
                        </SidebarMenuButton>
                      </SidebarMenuItem>
                    ))}
                  </SidebarMenu>
                </SidebarGroupContent>
              </SidebarGroup>

              {user && (
                <SidebarGroup>
                  <SidebarGroupLabel className="text-xs font-semibold text-gray-500 uppercase tracking-wider px-3 py-2">
                    Мои достижения
                  </SidebarGroupLabel>
                  <SidebarGroupContent>
                    <div className="px-4 py-3 space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Crown className="w-4 h-4 text-yellow-500" />
                          <span className="text-sm font-medium text-gray-700">Уровень</span>
                        </div>
                        <Badge variant="secondary" className="bg-yellow-100 text-yellow-800">
                          {user.level || 1}
                        </Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Баллы</span>
                        <span className="font-bold text-gray-800">{user.total_points || 0}</span>
                      </div>
                    </div>
                  </SidebarGroupContent>
                </SidebarGroup>
              )}

              {telegramUser && (
                <SidebarGroup>
                  <SidebarGroupLabel className="text-xs font-semibold text-blue-500 uppercase tracking-wider px-3 py-2">
                    Telegram
                  </SidebarGroupLabel>
                  <SidebarGroupContent>
                    <div className="px-4 py-3">
                      <p className="text-sm font-medium text-gray-900">
                        {telegramUser.first_name} {telegramUser.last_name}
                      </p>
                      <p className="text-xs text-gray-500">@{telegramUser.username}</p>
                    </div>
                  </SidebarGroupContent>
                </SidebarGroup>
              )}
            </SidebarContent>

            <SidebarFooter className="border-t border-gray-200 p-4">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full overflow-hidden flex items-center justify-center bg-gray-200">
                  {telegramUser?.photo_url ? (
                    <img src={telegramUser.photo_url} alt="Telegram Profile" className="w-full h-full object-cover" />
                  ) : user?.profile_picture_url ? (
                    <img src={user.profile_picture_url} alt="Profile" className="w-full h-full object-cover" />
                  ) : (
                    <User className="w-4 h-4 text-gray-600" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-900 text-sm truncate">
                    {telegramUser?.first_name || user?.full_name || 'Ученик'}
                  </p>
                  <p className="text-xs text-gray-500 truncate">
                    {telegramUser ? 'Telegram User' : user?.email}
                  </p>
                </div>
                {telegramAvailable && (
                  <Badge variant="outline" className="text-xs text-blue-600 border-blue-200">
                    TG
                  </Badge>
                )}
              </div>
            </SidebarFooter>
          </Sidebar>

          <main className="flex-1 flex flex-col overflow-hidden">
            <header className="bg-white/90 backdrop-blur-sm border-b border-gray-200 px-6 py-4 md:hidden">
              <div className="flex items-center gap-4">
                <SidebarTrigger className="hover:bg-gray-100 p-2 rounded-lg transition-colors duration-200" />
                <h1 className="text-xl font-bold text-gray-900">TeacherHelper</h1>
                {telegramAvailable && (
                  <Badge variant="outline" className="ml-auto text-blue-600 border-blue-200">
                    Telegram
                  </Badge>
                )}
              </div>
            </header>

            <div className="flex-1 overflow-auto">
              {children}
            </div>
          </main>
        </div>
      </SidebarProvider>
    </>
  );
}
