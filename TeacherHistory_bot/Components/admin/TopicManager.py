import React, { useState, useEffect } from 'react';
import { Topic } from '@/entities/Topic';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
  DialogClose
} from "@/components/ui/dialog";
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { PlusCircle, Edit, Trash2, Crown, Upload } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { UploadFile } from '@/integrations/Core';

const TopicForm = ({ topic, onSave, onCancel }) => {
    const [formData, setFormData] = useState(topic || {
        title: '',
        grade: 5,
        subject: 'history',
        content: '',
        video_url: '',
        is_premium: false,
        order_index: 0
    });
    const [isUploading, setIsUploading] = useState(false);

    const handleChange = (field, value) => {
        setFormData(prev => ({...prev, [field]: value}));
    };

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        setIsUploading(true);
        try {
            const { file_url } = await UploadFile({ file: file });
            setFormData(prev => ({ ...prev, video_url: file_url }));
        } catch (error) {
            console.error("Ошибка загрузки файла:", error);
            alert("Не удалось загрузить файл. Попробуйте еще раз.");
        } finally {
            setIsUploading(false);
        }
    };
    
    const handleSubmit = async () => {
        await onSave(formData);
    };

    return (
        <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
            <DialogHeader>
                <DialogTitle>{topic ? 'Редактировать тему' : 'Создать новую тему'}</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="title" className="text-right">Название</Label>
                    <Input 
                        id="title" 
                        value={formData.title} 
                        onChange={e => handleChange('title', e.target.value)} 
                        className="col-span-3" 
                    />
                </div>

                <div className="grid grid-cols-4 items-start gap-4">
                    <Label htmlFor="content" className="text-right pt-2">Содержание</Label>
                    <Textarea 
                        id="content" 
                        value={formData.content} 
                        onChange={e => handleChange('content', e.target.value)} 
                        className="col-span-3 min-h-[200px]" 
                        placeholder="Введите содержание урока..."
                    />
                </div>

                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="grade" className="text-right">Класс</Label>
                    <Select onValueChange={value => handleChange('grade', parseInt(value))} defaultValue={String(formData.grade)}>
                        <SelectTrigger className="col-span-3">
                            <SelectValue placeholder="Выберите класс" />
                        </SelectTrigger>
                        <SelectContent>
                            {[5, 6, 7, 8, 9, 10, 11].map(g => (
                                <SelectItem key={g} value={String(g)}>{g} класс</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>

                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="subject" className="text-right">Предмет</Label>
                    <Select onValueChange={value => handleChange('subject', value)} defaultValue={formData.subject}>
                        <SelectTrigger className="col-span-3">
                            <SelectValue placeholder="Выберите предмет" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="history">История</SelectItem>
                            <SelectItem value="social_studies">Обществознание</SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="order_index" className="text-right">Порядок</Label>
                    <Input 
                        id="order_index" 
                        type="number" 
                        value={formData.order_index} 
                        onChange={e => handleChange('order_index', parseInt(e.target.value) || 0)} 
                        className="col-span-3" 
                    />
                </div>

                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="video_url" className="text-right">Медиа</Label>
                    <div className="col-span-3 space-y-2">
                        <Input 
                            id="video_url" 
                            value={formData.video_url} 
                            onChange={e => handleChange('video_url', e.target.value)} 
                            placeholder="URL видео или аудио"
                        />
                        <div className="flex items-center gap-2">
                            <input
                                type="file"
                                accept="video/*,audio/*,image/*"
                                onChange={handleFileUpload}
                                className="hidden"
                                id="file-upload"
                            />
                            <Button
                                type="button"
                                variant="outline"
                                size="sm"
                                onClick={() => document.getElementById('file-upload').click()}
                                disabled={isUploading}
                            >
                                {isUploading ? (
                                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current mr-2" />
                                ) : (
                                    <Upload className="w-4 h-4 mr-2" />
                                )}
                                Загрузить файл
                            </Button>
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="is_premium" className="text-right">Премиум контент</Label>
                    <div className="col-span-3 flex items-center gap-3">
                        <Switch 
                            id="is_premium" 
                            checked={formData.is_premium} 
                            onCheckedChange={value => handleChange('is_premium', value)} 
                        />
                        <div className="text-sm text-gray-600">
                            {formData.is_premium ? 'Только для платных пользователей' : 'Доступно всем'}
                        </div>
                    </div>
                </div>
            </div>
            <DialogFooter>
                <DialogClose asChild>
                    <Button type="button" variant="secondary">Отмена</Button>
                </DialogClose>
                <Button onClick={handleSubmit}>Сохранить</Button>
            </DialogFooter>
        </DialogContent>
    );
}

export default function TopicManager() {
    const [topics, setTopics] = useState([]);
    const [editingTopic, setEditingTopic] = useState(null);
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [filterGrade, setFilterGrade] = useState('all');
    const [filterSubject, setFilterSubject] = useState('all');

    useEffect(() => {
        loadTopics();
    }, []);

    const loadTopics = async () => {
        const data = await Topic.list('grade');
        setTopics(data);
    };

    const handleSave = async (topicData) => {
        if (topicData.id) {
            await Topic.update(topicData.id, topicData);
        } else {
            await Topic.create(topicData);
        }
        loadTopics();
        setIsDialogOpen(false);
        setEditingTopic(null);
    };
    
    const handleEdit = (topic) => {
        setEditingTopic(topic);
        setIsDialogOpen(true);
    };
    
    const handleCreate = () => {
        setEditingTopic(null);
        setIsDialogOpen(true);
    };
    
    const handleDelete = async (topicId) => {
        if (window.confirm("Вы уверены, что хотите удалить эту тему?")) {
            await Topic.delete(topicId);
            loadTopics();
        }
    };

    const filteredTopics = topics.filter(topic => {
        const gradeMatch = filterGrade === 'all' || topic.grade?.toString() === filterGrade;
        const subjectMatch = filterSubject === 'all' || topic.subject === filterSubject;
        return gradeMatch && subjectMatch;
    });

    return (
        <Card>
            <CardHeader>
                <CardTitle>Управление темами и контентом</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="flex justify-between items-center mb-4">
                    <div className="flex gap-4">
                        <Select value={filterGrade} onValueChange={setFilterGrade}>
                            <SelectTrigger className="w-32">
                                <SelectValue placeholder="Класс" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">Все классы</SelectItem>
                                {[5, 6, 7, 8, 9, 10, 11].map(g => (
                                    <SelectItem key={g} value={String(g)}>{g}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>

                        <Select value={filterSubject} onValueChange={setFilterSubject}>
                            <SelectTrigger className="w-40">
                                <SelectValue placeholder="Предмет" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">Все предметы</SelectItem>
                                <SelectItem value="history">История</SelectItem>
                                <SelectItem value="social_studies">Обществознание</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                        <DialogTrigger asChild>
                            <Button onClick={handleCreate} className="flex gap-2">
                                <PlusCircle className="w-4 h-4" />
                                Добавить тему
                            </Button>
                        </DialogTrigger>
                        <TopicForm topic={editingTopic} onSave={handleSave} onCancel={() => setIsDialogOpen(false)} />
                    </Dialog>
                </div>

                <div className="space-y-3">
                    {filteredTopics.map(topic => (
                        <div key={topic.id} className="flex items-center p-4 border rounded-lg justify-between">
                            <div className="flex-1">
                                <div className="flex items-center gap-2 mb-2">
                                    <h3 className="font-medium">{topic.title}</h3>
                                    {topic.is_premium && <Crown className="w-4 h-4 text-yellow-500" />}
                                </div>
                                <div className="flex items-center gap-2 mb-2">
                                    <Badge variant="outline">{topic.grade} класс</Badge>
                                    <Badge variant="secondary">
                                        {topic.subject === 'history' ? 'История' : 'Обществознание'}
                                    </Badge>
                                    {topic.is_premium && (
                                        <Badge className="bg-yellow-100 text-yellow-800">Премиум</Badge>
                                    )}
                                    {topic.video_url && (
                                        <Badge variant="outline">С медиа</Badge>
                                    )}
                                </div>
                                <p className="text-sm text-gray-600 line-clamp-2">
                                    {topic.content?.substring(0, 150)}...
                                </p>
                            </div>
                            <div className="flex gap-2 ml-4">
                                <Button variant="ghost" size="icon" onClick={() => handleEdit(topic)}>
                                    <Edit className="w-4 h-4" />
                                </Button>
                                <Button variant="ghost" size="icon" onClick={() => handleDelete(topic.id)}>
                                    <Trash2 className="w-4 h-4 text-red-500" />
                                </Button>
                            </div>
                        </div>
                    ))}

                    {filteredTopics.length === 0 && (
                        <div className="text-center py-8 text-gray-500">
                            Темы не найдены. Создайте первую тему!
                        </div>
                    )}
                </div>
            </CardContent>
        </Card>
    );
}