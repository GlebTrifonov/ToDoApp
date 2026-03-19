from django.urls import path
from .views import tasks_list, task_create, task_delete, task_toggle

urlpatterns = [
    path('', tasks_list, name='tasks_list'),
    path('create/', task_create, name='task_create'),
    path('<int:pk>/toggle/', task_toggle, name='task_toggle'),
    path('<int:pk>/delete/', task_delete, name='task_delete'),
]