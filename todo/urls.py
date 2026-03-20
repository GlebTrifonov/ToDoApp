from django.urls import path
from .views import tasks_list, task_create, task_delete, task_toggle, category_list, category_create, category_delete

urlpatterns = [
        #Tasks
    path('', tasks_list, name='tasks_list'),
    path('create/', task_create, name='task_create'),
    path('<int:pk>/toggle/', task_toggle, name='task_toggle'),
    path('<int:pk>/delete/', task_delete, name='task_delete'),
    
        #Categories
    path('categories/', category_list, name='category_list'),
    path('categories/create/', category_create, name='category_create'),
    path('categories/delete/<int:pk>', category_delete, name='category_delete'),
]