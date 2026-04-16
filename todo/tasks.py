from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Tasks
# ФУНКЦИИ ДЛЯ ВЫПОЛНЕНИЯ  CELERY
@shared_task
def delete_old_completed_tasks():
    threshold = timezone.now() + timedelta(days=1)
    deleted_count = Tasks.objects.filter(
        is_active=False,
        completed_at__lt=threshold
    ).delete()
    print(f'Deleted {deleted_count[0]} old completed tasks')