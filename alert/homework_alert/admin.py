from django.contrib import admin

from .models import Homework
from .models import User
from .models import UserHomework

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('lecture', 'name', 'deadline')

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'password')

class UserHomeworkAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'homework_id')

admin.site.register(Homework, HomeworkAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserHomework, UserHomeworkAdmin)
