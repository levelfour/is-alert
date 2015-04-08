from django.contrib import admin

from .models import Homework
from .models import User
from .models import UserHomework

admin.site.register(Homework)
admin.site.register(User)
admin.site.register(UserHomework)
