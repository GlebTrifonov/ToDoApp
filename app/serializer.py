from rest_framework import serializers
from todo.models import Tasks, Subtasks, Categories

class TaskSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(many=True, queryset=Categories.objects.all())
    total = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()
    percent = serializers.ReadOnlyField()
    class Meta:
        model = Tasks
        fields  = ['category', 'total', 'completed', 'percent', 'id', 'title', 'is_active', 'priority', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['category_name', 'id']

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtasks
        fields = ['id', 'title', 'is_active']