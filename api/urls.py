from rest_framework.routers import DefaultRouter
from .views import SubtaskViewSet, TaskViewSet, CategoryViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')
router.register('subtasks', SubtaskViewSet, basename='subtasks')
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = router.urls