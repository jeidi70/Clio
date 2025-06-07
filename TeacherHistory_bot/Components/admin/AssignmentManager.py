import React, { useState, useEffect } from 'react';
import { Assignment, Topic } from '@/entities/all';
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
import { PlusCircle, Edit, Trash2, Plus, Minus } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const AssignmentForm = ({ assignment, topics, onSave, onCancel }) => {
    const [formData, setFormData] = useState(assignment || {
        topic_id: '',
        title: '',
        type: 'test',
        exam_format: 'regular',
        question: '',
        options: ['', '', '', ''],
        correct_answer: '',
        points: 5,
        explanation: '',
        difficulty: 'medium'
    });

    const handleChange = (field, value) => {
        setFormData(prev => ({...prev, [field]: value}));
    };

    const handleOptionChange = (index, value) => {
        const newOptions = [...formData.options];
        newOptions[index] = value;
        setFormData(prev => ({...prev, options: newOptions}));
    };

    const addOption = () => {
        setFormData(prev => ({...prev, options: [...prev.options, '']}));
    };

    const removeOption = (index) => {
        const newOptions = formData.options.filter((_, i) => i !== index);
        setFormData(prev => ({...prev, options: newOptions}));
    };
    
    const handleSubmit = async () => {
        const dataToSave = {...formData};
        if (formData.type !== 'test') {
            delete dataToSave.options;
        }
        await onSave(dataToSave);
    };

    return (
        <DialogContent className="sm:max-w-[800px] max-h-[90vh] overflow-y-auto">
            <DialogHeader>
                <DialogTitle>{assignment ? 'Редактировать задание' : 'Создать новое задание'}</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="topic_id" className="text-right">Тема</Label>
                    <Select onValueChange={value => handleChange('topic_id', value)} defaultValue={formData.topic_id}>
                        <SelectTrigger className="col-span-3">
                            <SelectValue placeholder="Выберите тему" />
                        </SelectTrigger>
                        <SelectContent>
                            {topics.map(topic => (
                                <SelectItem key={topic.id} value={topic.id}>
                                    {topic.title} ({topic.grade} класс)
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>

                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="title" className="text-right">Название</Label>
                    <Input 
                        id="title" 
                        value={formData.title} 
                        onChange={e => handleChange('title', e.target.value)} 
                        className="col-span-3" 
                    />
                </div>

                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="type" className="text-right">Тип</Label>
                    <Select onValueChange={value => handleChange('type', value)} defaultValue={formData.type}>
                        <SelectTrigger className="col-span-3">
                            <SelectValue placeholder="Выберите тип" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="test">Тест</SelectItem>
                            <SelectItem value="essay">Эссе</SelectItem>
                            <SelectItem value="document_analysis">Анализ документа</SelectItem>
                            <SelectItem value="case_study">Кейс-стади</SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="exam_format" className="text-right">Формат</Label>
                    <Select onValueChange={value => handleChange('exam_format', value)} defaultValue={formData.exam_format}>
                        <SelectTrigger className="col-span-3">
                            <SelectValue placeholder="Выберите формат" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="regular">Обычное</SelectItem>
                            <SelectItem value="oge">ОГЭ</SelectItem>
                            <SelectItem value="ege">ЕГЭ</SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="difficulty" className="text-right">Сложность</Label>
                    <Select onValueChange={value => handleChange('difficulty', value)} defaultValue={formData.difficulty}>
                        <SelectTrigger className="col-span-3">
                            <SelectValue placeholder="Выберите сложность" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="easy">Легкое</SelectItem>
                            <SelectItem value="medium">Среднее</SelectItem>
                            <SelectItem value="hard">Сложное</SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="points" className="text-right">Баллы</Label>
                    <Input 
                        id="points" 
                        type="number" 
                        value={formData.points} 
                        onChange={e => handleChange('points', parseInt(e.target.value))} 
                        className="col-span-3" 
                    />
                </div>

                <div className="grid grid-cols-4 items-start gap-4">
                    <Label htmlFor="question" className="text-right pt-2">Вопрос</Label>
                    <Textarea 
                        id="question" 
                        value={formData.question} 
                        onChange={e => handleChange('question', e.target.value)} 
                        className="col-span-3 min-h-[100px]" 
                    />
                </div>

                {formData.type === 'test' && (
                    <div className="grid grid-cols-4 items-start gap-4">
                        <Label className="text-right pt-2">Варианты ответов</Label>
                        <div className="col-span-3 space-y-2">
                            {formData.options.map((option, index) => (
                                <div key={index} className="flex gap-2">
                                    <Input 
                                        value={option}
                                        onChange={e => handleOptionChange(index, e.target.value)}
                                        placeholder={`Вариант ${index + 1}`}
                                        className="flex-1"
                                    />
                                    {formData.options.length > 2 && (
                                        <Button 
                                            type="button" 
                                            variant="outline" 
                                            size="icon"
                                            onClick={() => removeOption(index)}
                                        >
                                            <Minus className="w-4 h-4" />
                                        </Button>
                                    )}
                                </div>
                            ))}
                            <Button 
                                type="button" 
                                variant="outline" 
                                onClick={addOption}
                                className="w-full"
                            >
                                <Plus className="w-4 h-4 mr-2" />
                                Добавить вариант
                            </Button>
                        </div>
                    </div>
                )}

                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="correct_answer" className="text-right">Правильный ответ</Label>
                    <Textarea 
                        id="correct_answer" 
                        value={formData.correct_answer} 
                        onChange={e => handleChange('correct_answer', e.target.value)} 
                        className="col-span-3 min-h-[80px]" 
                    />
                </div>

                <div className="grid grid-cols-4 items-start gap-4">
                    <Label htmlFor="explanation" className="text-right pt-2">Объяснение</Label>
                    <Textarea 
                        id="explanation" 
                        value={formData.explanation} 
                        onChange={e => handleChange('explanation', e.target.value)} 
                        className="col-span-3 min-h-[80px]" 
                    />
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

export default function AssignmentManager() {
    const [assignments, setAssignments] = useState([]);
    const [topics, setTopics] = useState([]);
    const [editingAssignment, setEditingAssignment] = useState(null);
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [selectedTopic, setSelectedTopic] = useState('all');

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        const [assignmentsData, topicsData] = await Promise.all([
            Assignment.list('-created_date'),
            Topic.list('grade')
        ]);
        setAssignments(assignmentsData);
        setTopics(topicsData);
    };

    const handleSave = async (assignmentData) => {
        if (assignmentData.id) {
            await Assignment.update(assignmentData.id, assignmentData);
        } else {
            await Assignment.create(assignmentData);
        }
        loadData();
        setIsDialogOpen(false);
        setEditingAssignment(null);
    };
    
    const handleEdit = (assignment) => {
        setEditingAssignment(assignment);
        setIsDialogOpen(true);
    };
    
    const handleCreate = () => {
        setEditingAssignment(null);
        setIsDialogOpen(true);
    };
    
    const handleDelete = async (assignmentId) => {
        if (window.confirm("Вы уверены, что хотите удалить это задание?")) {
            await Assignment.delete(assignmentId);
            loadData();
        }
    };

    const getTopicTitle = (topicId) => {
        const topic = topics.find(t => t.id === topicId);
        return topic ? topic.title : 'Неизвестная тема';
    };

    const filteredAssignments = selectedTopic === 'all' 
        ? assignments 
        : assignments.filter(a => a.topic_id === selectedTopic);

    return (
        <Card>
            <CardHeader>
                <CardTitle>Управление заданиями</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="flex justify-between items-center mb-4">
                    <Select value={selectedTopic} onValueChange={setSelectedTopic}>
                        <SelectTrigger className="w-64">
                            <SelectValue placeholder="Фильтр по теме" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="all">Все темы</SelectItem>
                            {topics.map(topic => (
                                <SelectItem key={topic.id} value={topic.id}>
                                    {topic.title} ({topic.grade} класс)
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>

                    <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                        <DialogTrigger asChild>
                            <Button onClick={handleCreate} className="flex gap-2">
                                <PlusCircle className="w-4 h-4" />
                                Добавить задание
                            </Button>
                        </DialogTrigger>
                        <AssignmentForm 
                            assignment={editingAssignment} 
                            topics={topics}
                            onSave={handleSave} 
                            onCancel={() => setIsDialogOpen(false)} 
                        />
                    </Dialog>
                </div>

                <div className="space-y-3">
                    {filteredAssignments.map(assignment => (
                        <div key={assignment.id} className="flex items-center p-4 border rounded-lg justify-between">
                            <div className="flex-1">
                                <div className="flex items-center gap-2 mb-2">
                                    <h3 className="font-medium">{assignment.title}</h3>
                                    <Badge variant="outline">{assignment.type}</Badge>
                                    <Badge variant="secondary">{assignment.exam_format}</Badge>
                                    <Badge className={
                                        assignment.difficulty === 'easy' ? 'bg-green-100 text-green-800' :
                                        assignment.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                                        'bg-red-100 text-red-800'
                                    }>
                                        {assignment.difficulty}
                                    </Badge>
                                </div>
                                <p className="text-sm text-gray-500">
                                    Тема: {getTopicTitle(assignment.topic_id)} • {assignment.points} баллов
                                </p>
                                <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                                    {assignment.question.substring(0, 150)}...
                                </p>
                            </div>
                            <div className="flex gap-2 ml-4">
                                <Button variant="ghost" size="icon" onClick={() => handleEdit(assignment)}>
                                    <Edit className="w-4 h-4" />
                                </Button>
                                <Button variant="ghost" size="icon" onClick={() => handleDelete(assignment.id)}>
                                    <Trash2 className="w-4 h-4 text-red-500" />
                                </Button>
                            </div>
                        </div>
                    ))}

                    {filteredAssignments.length === 0 && (
                        <div className="text-center py-8 text-gray-500">
                            Заданий не найдено. Создайте первое задание!
                        </div>
                    )}
                </div>
            </CardContent>
        </Card>
    );
}