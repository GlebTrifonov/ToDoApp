from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tasks, TaskHistory

@receiver(post_save, sender=Tasks)
def log_task_history(sender, instance, created, **kwargs):
    if created:
        action = TaskHistory.Action.CREATED
    else:
        action = TaskHistory.Action.UPDATED
    TaskHistory.objects.create(task=instance, changed_by=instance.user, action=action)