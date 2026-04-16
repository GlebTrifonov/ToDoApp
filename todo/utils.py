from .models import TaskHistory

def cleanup_task_history(task, limit=None):
    if limit is None:
        from django.conf import settings
        limit = settings.TASK_HISTORY_LIMIT

    history = TaskHistory.objects.filter(task=task).order_by('-id')

    if history.count() > limit:

        ids_to_delete = history.values_list('id', flat=True)[limit:]

        TaskHistory.objects.filter(id__in=ids_to_delete).delete()