from django.db.models.signals import post_save, pre_delete, pre_save
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from .models import Tasks, TaskHistory
from .utils import cleanup_task_history



@receiver(post_save, sender=Tasks)
def log_task_history(sender, instance, created, **kwargs):
    if created:
        action = TaskHistory.Action.CREATED
    else:
        action = TaskHistory.Action.UPDATED
    TaskHistory.objects.create(task=instance, changed_by=instance.user, action=action)
    cleanup_task_history(instance)


@receiver(pre_delete, sender=Tasks)
def log_task_delete(sender, instance, **kwargs):
    action = TaskHistory.Action.DELETED
    TaskHistory.objects.create(task=instance, changed_by=instance.user, action=action)
    cleanup_task_history(instance)

@receiver(pre_save, sender=Tasks)
def log_task__status_toggle(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_task = Tasks.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        return
    if old_task.is_active != instance.is_active:
        TaskHistory.objects.create(task=instance, changed_by=instance.user, action=TaskHistory.Action.TOGGLED)
        cleanup_task_history(instance)