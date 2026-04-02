from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from todo.models import Tasks


class TaskListViewTest(TestCase):
    def setUP(self):
        
        pass
    
    def test_tasks_list_returns_200(self):
        pass