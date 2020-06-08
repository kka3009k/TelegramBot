from django.contrib import admin
from .models import * 

# Register your models here.

@admin.register(UsersBot)
class UsersBotAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'full_name', 'fin_institute','is_active','date_create')
    list_filter = ('full_name', 'is_active',)
    search_fields = ('full_name', 'user_id')
