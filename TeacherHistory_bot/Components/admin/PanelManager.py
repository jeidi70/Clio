import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Plus, Settings, Trash2, Eye } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
  DialogClose
} from "@/components/ui/dialog";

export default function PanelManager() {
    const [customPanels, setCustomPanels] = useState([
        {
            id: 'reports',
            name: 'Отчеты',
            description: 'Генерация и просмотр отчетов по успеваемости',
            icon: 'BarChart3',
            active: true
        },
        {
            id: 'notifications',
            name: 'Уведомления',
            description: 'Управление системными уведомлениями',
            icon: 'Bell',
            active: false
        }
    ]);
    const [newPanel, setNewPanel] = useState({
        name: '',
        description: '',
        icon: 'Settings'
    });
    const [isDialogOpen, setIsDialogOpen] = useState(false);

    const defaultPanels = [
        { id: 'topics', name: 'Темы', description: 'Управление учебными темами', active: true },
        { id: 'assignments', name: 'Задания', description: 'Создание и редактирование заданий', active: true },
        { id: 'users', name: 'Пользователи', description: 'Управление учениками и их данными', active: true },
        { id: 'preview', name: 'Предпросмотр', description: 'Просмотр материалов глазами ученика', active: true },
        { id: 'review', name: 'Проверка заданий', description: 'Проверка развернутых ответов', active: true },
        { id: 'stats', name: 'Статистика', description: 'Аналитика и отчеты', active: true }
    ];

    const handleAddPanel = () => {
        if (!newPanel.name.trim()) return;
        
        const panel = {
            id: `custom_${Date.now()}`,
            name: newPanel.name,
            description: newPanel.description,
            icon: newPanel.icon,
            active: true,
            custom: true
        };
        
        setCustomPanels([...customPanels, panel]);
        setNewPanel({ name: '', description: '', icon: 'Settings' });
        setIsDialogOpen(false);
    };

    const handleDeletePanel = (panelId) => {
        if (window.confirm('Вы уверены, что хотите удалить эту панель?')) {
            setCustomPanels(customPanels.filter(p => p.id !== panelId));
        }
    };

    const togglePanelStatus = (panelId) => {
        setCustomPanels(customPanels.map(panel => 
            panel.id === panelId ? { ...panel, active: !panel.active } : panel
        ));
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle className="flex items-center gap-2">
                            <Settings className="w-5 h-5" />
                            Управление панелями администратора
                        </CardTitle>
                        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                            <DialogTrigger asChild>
                                <Button className="flex gap-2">
                                    <Plus className="w-4 h-4" />
                                    Добавить панель
                                </Button>
                            </DialogTrigger>
                            <DialogContent>
                                <DialogHeader>
                                    <DialogTitle>Создать новую панель</DialogTitle>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                    <div>
                                        <label className="block text-sm font-medium mb-2">Название панели</label>
                                        <Input
                                            value={newPanel.name}
                                            onChange={(e) => setNewPanel({...newPanel, name: e.target.value})}
                                            placeholder="Например: Экспорт данных"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium mb-2">Описание</label>
                                        <Textarea
                                            value={newPanel.description}
                                            onChange={(e) => setNewPanel({...newPanel, description: e.target.value})}
                                            placeholder="Описание функциональности панели..."
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium mb-2">Иконка</label>
                                        <select
                                            value={newPanel.icon}
                                            onChange={(e) => setNewPanel({...newPanel, icon: e.target.value})}
                                            className="w-full p-2 border rounded-lg"
                                        >
                                            <option value="Settings">Settings</option>
                                            <option value="FileText">FileText</option>
                                            <option value="Download">Download</option>
                                            <option value="Upload">Upload</option>
                                            <option value="Mail">Mail</option>
                                            <option value="Bell">Bell</option>
                                            <option value="Calendar">Calendar</option>
                                        </select>
                                    </div>
                                </div>
                                <DialogFooter>
                                    <DialogClose asChild>
                                        <Button variant="outline">Отмена</Button>
                                    </DialogClose>
                                    <Button onClick={handleAddPanel} disabled={!newPanel.name.trim()}>
                                        Создать панель
                                    </Button>
                                </DialogFooter>
                            </DialogContent>
                        </Dialog>
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="space-y-6">
                        {/* Системные панели */}
                        <div>
                            <h3 className="text-lg font-medium mb-4">Системные панели</h3>
                            <div className="grid gap-3">
                                {defaultPanels.map(panel => (
                                    <div key={panel.id} className="flex items-center justify-between p-4 border rounded-lg bg-gray-50">
                                        <div className="flex items-center gap-3">
                                            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                                                <Eye className="w-5 h-5 text-blue-600" />
                                            </div>
                                            <div>
                                                <h4 className="font-medium">{panel.name}</h4>
                                                <p className="text-sm text-gray-600">{panel.description}</p>
                                            </div>
                                        </div>
                                        <Badge variant="outline" className="bg-green-100 text-green-800">
                                            Активна
                                        </Badge>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Пользовательские панели */}
                        <div>
                            <h3 className="text-lg font-medium mb-4">Пользовательские панели</h3>
                            <div className="grid gap-3">
                                {customPanels.map(panel => (
                                    <div key={panel.id} className="flex items-center justify-between p-4 border rounded-lg">
                                        <div className="flex items-center gap-3">
                                            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
                                                <Settings className="w-5 h-5 text-purple-600" />
                                            </div>
                                            <div>
                                                <h4 className="font-medium">{panel.name}</h4>
                                                <p className="text-sm text-gray-600">{panel.description}</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <Badge 
                                                variant="outline" 
                                                className={panel.active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'}
                                            >
                                                {panel.active ? 'Активна' : 'Неактивна'}
                                            </Badge>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                onClick={() => togglePanelStatus(panel.id)}
                                            >
                                                <Eye className="w-4 h-4" />
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                onClick={() => handleDeletePanel(panel.id)}
                                                className="text-red-500 hover:text-red-700"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </Button>
                                        </div>
                                    </div>
                                ))}
                                
                                {customPanels.length === 0 && (
                                    <div className="text-center py-8 text-gray-500">
                                        Пользовательских панелей пока нет. Создайте первую!
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Предварительный просмотр структуры панелей */}
            <Card>
                <CardHeader>
                    <CardTitle>Предварительный просмотр панелей</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="border rounded-lg p-4 bg-gray-50">
                        <div className="text-sm text-gray-600 mb-2">Структура вкладок админ-панели:</div>
                        <div className="flex flex-wrap gap-2">
                            {[...defaultPanels, ...customPanels.filter(p => p.active)].map(panel => (
                                <Badge key={panel.id} variant="secondary">
                                    {panel.name}
                                </Badge>
                            ))}
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}