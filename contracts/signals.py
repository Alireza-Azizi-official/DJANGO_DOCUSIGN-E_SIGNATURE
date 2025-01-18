from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Contract
from django.utils import timezone

@receiver(post_save, sender=Contract)
def update_signed_status(sender, instance, created, **kwargs):
    updated = False

    if instance.status == 'signed' or instance.status == 'completed':
        if not instance.signed_by_user:
            instance.signed_by_user = True
            updated = True 
        if not instance.signed_by_recipient:
            instance.signed_by_recipient = True
            updated = True  
    if updated:
        instance.save()

