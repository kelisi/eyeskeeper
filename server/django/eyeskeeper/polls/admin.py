from django.contrib import admin

# Register your models here.
from .models import Question

# 在管理员界面注册Model接管
admin.site.register(Question)
