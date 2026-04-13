import pytest
from django.contrib.auth.models import User
from todo.models import Tasks, Categories, Subtasks

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def test_category(test_user):
    return Categories.objects.create(user=test_user, category_name='Test Category')

@pytest.fixture
def test_active_task(test_user, test_category):
    task = Tasks.objects.create(
        user=test_user,
        title='Active Task',
        priority='M',
        is_active=True,
    )
    task.category.set([test_category.id])
    return task

@pytest.fixture
def test_complite_task(test_user, test_category):
    task = Tasks.objects.create(
        user=test_user,
        title='Completed Task',
        priority='M',
        is_active=False,
    )
    task.category.set([test_category.id])
    return task

@pytest.mark.django_db
def test_tasks_page_status(client, test_user):
    #Регестрируем юзера для теста, тк у нас стоит обязательный @login_required во вьюхах

    client.login(username=test_user.username, password='testpass')
    
    response = client.get('/tasks/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_task(client, test_user, test_category):

    client.login(username=test_user.username, password='testpass')
    #у нас каты обязательные для тасков, соответственно создаем тестовую категорию
    category = test_category
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

@pytest.mark.django_db
def test_filter_completed_tasks(client, test_user, test_category, test_active_task, test_complite_task):
    client.login(username=test_user.username, password='testpass')

   
    response = client.get('/tasks/?status=completed')
    content = response.content.decode()

    assert 'Completed Task' in content
    assert 'Active Task' not in content

@pytest.mark.django_db
def test_search_tasks(client, test_user, test_category):
    client.login(username=test_user.username, password='testpass')

    task_in_search = Tasks.objects.create(
        user=test_user,
        title="Test With Milk",
        priority='M',
        is_active=True
    )
    task_in_search.category.set([test_category.id])
    
    task_not_in_search = Tasks.objects.create(
        user=test_user,
        title='I love Cats',
        priority='M',
        is_active=True
    )

    response = client.get('/tasks/?search=Milk')
    content = response.content.decode()
    assert 'Milk' in content
    assert 'Cats' not in content

@pytest.mark.django_db
def test_pagination_limit(client, test_user, test_category):
    client.login(username=test_user.username, password='testpass')
    for i in range(6, 0, -1):
        task = Tasks.objects.create(
            user=test_user,
            title=f'Task {i}',
            priority='M',
            is_active=True
        )
        task.category.set([test_category.id])

    response = client.get('/tasks/')
    content = response.content.decode()

    assert 'Task 1' in content
    assert 'Task 2' in content
    assert 'Task 3' in content
    assert 'Task 4' in content
    assert 'Task 5' in content
    assert 'Task 6' not in content