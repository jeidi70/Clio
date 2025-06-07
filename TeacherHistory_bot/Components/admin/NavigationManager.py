import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Plus, Navigation, Trash2, Edit, Eye, EyeOff } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
  DialogClose
} from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export default function NavigationManager() {
    const [navigationItems, setNavigationItems] = useState([
        { id: 'learning', title: 'Обучение', url: 'Learning', icon: 'BookOpen', visible: true, system: true },
        { id: 'leaderboard', title: 'Рейтинг', url: 'Leaderboard', icon: 'Trophy', visible: true, system: true },
        { id: 'progress', title: 'Мой прогресс', url: 'Progress', icon: 'BarChart3', visible: true, system: true },
        { id: 'premium', title: 'Премиум', url: 'Premium', icon: 'Crown', visible: true, system: true },
        { id: 'aihelper', title: 'ИИ-Помощник', url: 'AIHelper', icon: 'Brain', visible: true, system: true },
        { id: 'profile', title: 'Профиль', url: 'Profile', icon: 'User', visible: true, system: true }
    ]);
    
    const [newItem, setNewItem] = useState({
        title: '',
        url: '',
        icon: 'BookOpen'
    });
    const [editingItem, setEditingItem] = useState(null);
    const [isDialogOpen, setIsDialogOpen] = useState(false);

    const availableIcons = [
        'BookOpen', 'Trophy', 'BarChart3', 'Crown', 'Brain', 'User', 'Settings',
        'FileText', 'Download', 'Upload', 'Mail', 'Bell', 'Calendar', 'Star',
        'Heart', 'Home', 'Search', 'Plus', 'Minus', 'Check', 'X'
    ];

    const handleAddItem = () => {
        if (!newItem.title.trim() || !newItem.url.trim()) return;
        
        const item = {
            id: `custom_${Date.now()}`,
            title: newItem.title,
            url: newItem.url,
            icon: newItem.icon,
            visible: true,
            system: false
        };
        
        setNavigationItems([...navigationItems, item]);
        setNewItem({ title: '', url: '', icon: 'BookOpen' });
        setIsDialogOpen(false);
    };

    const handleEditItem = (item) => {
        setEditingItem(item);
        setNewItem({
            title: item.title,
            url: item.url,
            icon: item.icon
        });
        setIsDialogOpen(true);
    };

    const handleUpdateItem = () => {
        if (!newItem.title.trim() || !newItem.url.trim()) return;
        
        setNavigationItems(navigationItems.map(item => 
            item.id === editingItem.id 
                ? { ...item, title: newItem.title, url: newItem.url, icon: newItem.icon }
                : item
        ));
        
        setEditingItem(null);
        setNewItem({ title: '', url: '', icon: 'BookOpen' });
        setIsDialogOpen(false);
    };

    const handleDeleteItem = (itemId) => {
        if (window.confirm('Вы уверены, что хотите удалить этот пункт навигации?')) {
            setNavigationItems(navigationItems.filter(item => item.id !== itemId));
        }
    };

    const toggleVisibility = (itemId) => {
        setNavigationItems(navigationItems.map(item => 
            item.id === itemId ? { ...item, visible: !item.visible } : item
        ));
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle className="flex items-center gap-2">
                            <Navigation className="w-5 h-5" />
                            Управление навигацией
                        </CardTitle>
                        <Dialog open={isDialogOpen} onOpenChange={(open) => {
                            setIsDialogOpen(open);
                            if (!open) {
                                setEditingItem(null);
                                setNewItem({ title: '', url: '', icon: 'BookOpen' });
                            }
                        }}>
                            <DialogTrigger asChild>
                                <Button className="flex gap-2">
                                    <Plus className="w-4 h-4" />
                                    Добавить пункт
                                </Button>
                            </DialogTrigger>
                            <DialogContent>
                                <DialogHeader>
                                    <DialogTitle>
                                        {editingItem ? 'Редактировать пункт навигации' : 'Создать новый пункт навигации'}
                                    </DialogTitle>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                    <div>
                                        <label className="block text-sm font-medium mb-2">Название</label>
                                        <Input
                                            value={newItem.title}
                                            onChange={(e) => setNewItem({...newItem, title: e.target.value})}
                                            placeholder="Название пункта меню"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium mb-2">URL страницы</label>
                                        <Input
                                            value={newItem.url}
                                            onChange={(e) => setNewItem({...newItem, url: e.target.value})}
                                            placeholder="Например: MyPage"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium mb-2">Иконка</label>
                                        <Select 
                                            value={newItem.icon} 
                                            onValueChange={(value) => setNewItem({...newItem, icon: value})}
                                        >
                                            <SelectTrigger>
                                                <SelectValue placeholder="Выберите иконку" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                {availableIcons.map(icon => (
                                                    <SelectItem key={icon} value={icon}>
                                                        {icon}
                                                    </SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                    </div>
                                </div>
                                <DialogFooter>
                                    <DialogClose asChild>
                                        <Button variant="outline">Отмена</Button>
                                    </DialogClose>
                                    <Button 
                                        onClick={editingItem ? handleUpdateItem : handleAddItem}
                                        disabled={!newItem.title.trim() || !newItem.url.trim()}
                                    >
                                        {editingItem ? 'Обновить' : 'Создать'}
                                    </Button>
                                </DialogFooter>
                            </DialogContent>
                        </Dialog>
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="space-y-3">
                        {navigationItems.map(item => (
                            <div key={item.id} className="flex items-center justify-between p-4 border rounded-lg">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                                        <Navigation className="w-5 h-5 text-blue-600" />
                                    </div>
                                    <div>
                                        <h4 className="font-medium">{item.title}</h4>
                                        <p className="text-sm text-gray-500">
                                            {item.url} • {item.icon}
                                        </p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-2">
                                    <Badge 
                                        variant="outline" 
                                        className={item.visible ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'}
                                    >
                                        {item.visible ? 'Видимый' : 'Скрытый'}
                                    </Badge>
                                    {item.system && (
                                        <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                                            Системный
                                        </Badge>
                                    )}
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        onClick={() => toggleVisibility(item.id)}
                                    >
                                        {item.visible ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                                    </Button>
                                    {!item.system && (
                                        <>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                onClick={() => handleEditItem(item)}
                                            >
                                                <Edit className="w-4 h-4" />
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                onClick={() => handleDeleteItem(item.id)}
                                                className="text-red-500 hover:text-red-700"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </Button>
                                        </>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Предварительный просмотр навигации */}
            <Card>
                <CardHeader>
                    <CardTitle>Предварительный просмотр навигации</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="border rounded-lg p-4 bg-gray-50">
                        <div className="text-sm text-gray-600 mb-2">Видимые пункты меню:</div>
                        <div className="flex flex-wrap gap-2">
                            {navigationItems.filter(item => item.visible).map(item => (
                                <Badge key={item.id} variant="secondary">
                                    {item.title}
                                </Badge>
                            ))}
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}