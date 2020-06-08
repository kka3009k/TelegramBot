from django.db import models

class UsersBot(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    user_id = models.IntegerField(null=True, verbose_name='ID пользователя')
    full_name = models.CharField(max_length=500, verbose_name='ФИО',help_text=("ФИО"))
    is_active = models.BooleanField(default=False)
    date_create = models.DateTimeField(null=True)