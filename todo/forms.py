from django import forms
from .models import Categories, Tasks

class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'category', 'priority']

class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['category_name']