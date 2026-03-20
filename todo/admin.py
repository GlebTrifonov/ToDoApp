from django.contrib import admin
from .models import Tasks, Categories, Subtasks


class SubtasksInline(admin.TabularInline):
    model = Subtasks


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ['title','description','created_at','is_active','priority']
    list_filter = ['category', 'is_active']
    search_fields = ['category__category_name', 'priority', 'title']
    inlines = [SubtasksInline]

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['category_name']
    search_fields = ['category_name']


@admin.register(Subtasks)
class SubtasksAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['task', 'is_active']
    search_fields = ['task__title', 'title']