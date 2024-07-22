from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User

from apps.account.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates profile instance for user
    """
    if created:
        Profile.objects.create(
            user=instance
        )
