import pytest
from django.contrib.auth.models import User
from todo.models import Tasks, Categories, Subtasks

@pytest.mark.django_db
def test_tasks_page_status(client):
    #Регестрируем юзера для теста, тк у нас стоит обязательный @login_required во вьюхах
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')
    
    response = client.get('/tasks/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_task(client):
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')
    #у нас каты обязательные для тасков, соответственно создаем тестовую категорию
    category = Categories.objects.create(user=user, category_name='Test Category')
    response = client.post('/tasks/create/', {
        'title': 'Test Task',
        'priority': 'M',
        'category': [category.id],
    })
    #проверяет вернулись ли бы обратно на страницу /tasks/ после создания (редирект)
    assert response.status_code == 302
    assert response.url == '/tasks/'

    #Проверяет задачу в базе
    assert Tasks.objects.filter(title='Test Task').exists()