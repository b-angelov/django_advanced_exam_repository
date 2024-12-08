from datetime import date

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from izpitnik import settings
from izpitnik.accounts.models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance: User, created: bool, **kwargs):
    print(instance,sender.pk)
    if created:
        Profile.objects.create(user=instance, birth_date=date.today(), description='')