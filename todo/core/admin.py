from django.contrib import admin
from .models import List, Task

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

class ListAdmin(admin.ModelAdmin):
    inlines = [TaskInline]

admin.site.register(List, ListAdmin)

