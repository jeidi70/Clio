import React, { useState, useEffect } from 'react';
import { User } from '@/entities/User';
import { createPageUrl } from '@/utils';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ShieldCheck, BookCopy, ListChecks, BarChart2, Users, Eye, ClipboardCheck, Settings, Navigation } from 'lucide-react';
import TopicManager from '../components/admin/TopicManager';
import AssignmentManager from '../components/admin/AssignmentManager';
import StatisticsViewer from '../components/admin/StatisticsViewer';
import UserManager from '../components/admin/UserManager';
import ContentPreview from '../components/admin/ContentPreview';
import AssignmentReview from '../components/admin/AssignmentReview';
import PanelManager from '../components/admin/PanelManager';
import NavigationManager from '../components/admin/NavigationManager';

export default function AdminPanel() {
    const [isAdmin, setIsAdmin] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAdmin = async () => {
            try {
                const user = await User.me();
                if (user.role === 'admin') {
                    setIsAdmin(true);
                } else {
                   window.location.href = createPageUrl("Learning");
                }
            } catch (error) {
                window.location.href = createPageUrl("Learning");
            }
            setLoading(false);
        };
        checkAdmin();
    }, []);

    if (loading) {
        return (
            <div className="p-8 flex justify-center items-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }
    
    if (!isAdmin) {
        return null;
    }

    return (
        <div className="p-6">
            <div className="flex items-center gap-3 mb-6">
                <ShieldCheck className="w-8 h-8 text-green-600" />
                <div>
                    <h1 className="text-3xl font-bold">Панель администратора TeacherHelper</h1>
                    <p className="text-gray-500">Полное управление образовательной платформой</p>
                </div>
            </div>

            <Tabs defaultValue="topics" className="w-full">
                <TabsList className="grid w-full grid-cols-8">
                    <TabsTrigger value="topics" className="flex gap-2">
                        <BookCopy className="w-4 h-4" />
                        Темы
                    </TabsTrigger>
                    <TabsTrigger value="assignments" className="flex gap-2">
                        <ListChecks className="w-4 h-4" />
                        Задания
                    </TabsTrigger>
                    <TabsTrigger value="users" className="flex gap-2">
                        <Users className="w-4 h-4" />
                        Пользователи
                    </TabsTrigger>
                    <TabsTrigger value="preview" className="flex gap-2">
                        <Eye className="w-4 h-4" />
                        Предпросмотр
                    </TabsTrigger>
                    <TabsTrigger value="review" className="flex gap-2">
                        <ClipboardCheck className="w-4 h-4" />
                        Проверка
                    </TabsTrigger>
                    <TabsTrigger value="navigation" className="flex gap-2">
                        <Navigation className="w-4 h-4" />
                        Навигация
                    </TabsTrigger>
                    <TabsTrigger value="panels" className="flex gap-2">
                        <Settings className="w-4 h-4" />
                        Панели
                    </TabsTrigger>
                    <TabsTrigger value="stats" className="flex gap-2">
                        <BarChart2 className="w-4 h-4" />
                        Статистика
                    </TabsTrigger>
                </TabsList>
                <TabsContent value="topics">
                    <TopicManager />
                </TabsContent>
                <TabsContent value="assignments">
                    <AssignmentManager />
                </TabsContent>
                <TabsContent value="users">
                    <UserManager />
                </TabsContent>
                <TabsContent value="preview">
                    <ContentPreview />
                </TabsContent>
                <TabsContent value="review">
                    <AssignmentReview />
                </TabsContent>
                <TabsContent value="navigation">
                    <NavigationManager />
                </TabsContent>
                <TabsContent value="panels">
                    <PanelManager />
                </TabsContent>
                <TabsContent value="stats">
                    <StatisticsViewer />
                </TabsContent>
            </Tabs>
        </div>
    );
}