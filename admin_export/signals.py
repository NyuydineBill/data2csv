from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def log_export_activity(sender, instance, created, **kwargs):
    """Log export activity for audit purposes."""
    if hasattr(instance, '_export_activity'):
        activity = instance._export_activity
        logger.info(
            f"Export activity: User {instance.username} exported {activity.get('count', 0)} "
            f"items from {activity.get('model', 'Unknown')} to {activity.get('format', 'Unknown')}"
        )
        delattr(instance, '_export_activity')

def log_export_action(user, model_name, count, format_type, success=True):
    """Log export actions for monitoring and debugging."""
    if getattr(settings, 'EXPORT_ENABLE_LOGGING', True):
        level = getattr(settings, 'EXPORT_LOG_LEVEL', 'INFO')
        log_func = getattr(logger, level.lower(), logger.info)
        
        status = "successfully" if success else "failed to"
        log_func(
            f"User {user.username} {status} export {count} items from {model_name} to {format_type}"
        ) 