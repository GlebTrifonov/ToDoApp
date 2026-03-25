from rest_framework import viewsets
from .serializers import TaskSerializer, SubtaskSerializer, CategorySerializer
from todo.models import Tasks, Subtasks, Categories

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    def get_queryset(self):
        return Tasks.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    

class SubtaskViewSet(viewsets.ModelViewSet):
    serializer_class = SubtaskSerializer
    def get_queryset(self):
        return Subtasks.objects.filter(task__user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Categories.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

