
import React, { useState, useEffect } from 'react';
import { User } from '@/entities/User';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { User as UserIcon, Mail, Save, LogOut } from 'lucide-react';
import { motion } from 'framer-motion';
import { createPageUrl } from '@/utils';

export default function ProfilePage() {
  const [user, setUser] = useState(null);
  const [fullName, setFullName] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const userData = await User.me();
        setUser(userData);
        setFullName(userData.full_name || '');
      } catch (error) {
        console.error("Не удалось загрузить пользователя", error);
      }
    };
    fetchUser();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      await User.updateMyUserData({ full_name: fullName });
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 2000);
    } catch (error) {
      console.error("Ошибка сохранения", error);
    }
    setIsSaving(false);
  };
  
  const handleLogout = async () => {
    await User.logout();
    window.location.href = createPageUrl("Learning");
  }

  if (!user) {
    return <div className="p-8 text-center">Загрузка...</div>;
  }

  return (
    <div className="min-h-screen p-6 flex items-center justify-center">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md"
      >
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="text-2xl">Мой профиль</CardTitle>
            <CardDescription>Здесь вы можете обновить информацию о себе.</CardDescription>
          </CardHeader>
          <form onSubmit={handleSave}>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <div className="flex items-center gap-3 p-3 bg-gray-100 rounded-md">
                  <Mail className="w-4 h-4 text-gray-500" />
                  <span className="text-gray-700">{user.email}</span>
                </div>
                <p className="text-xs text-gray-500">Email нельзя изменить, так как он используется для входа через Google.</p>
              </div>
              <div className="space-y-2">
                <Label htmlFor="fullName">Полное имя</Label>
                <div className="flex items-center gap-3">
                  <UserIcon className="w-4 h-4 text-gray-400 absolute ml-3" />
                  <Input
                    id="fullName"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="pl-9"
                  />
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button type="button" variant="outline" onClick={handleLogout} className="flex gap-2">
                <LogOut className="w-4 h-4" />
                Выйти
              </Button>
              <Button type="submit" disabled={isSaving} className="flex gap-2">
                {isSaving ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                ) : showSuccess ? "Сохранено!" : <Save className="w-4 h-4" />}
                {showSuccess ? "" : "Сохранить"}
              </Button>
            </CardFooter>
          </form>
        </Card>
      </motion.div>
    </div>
  );
}
