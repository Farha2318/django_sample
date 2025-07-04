import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from blogapp.models import Comment  # ✅ Use full app name

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Comment)
def notify_comment_created(sender, instance, created, **kwargs):
    if created:
        logger.info(f"A new comment was created by {instance.name} on '{instance.post.title}'")
