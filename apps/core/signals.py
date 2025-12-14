from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models_profile import ParentProfile

@receiver(post_save, sender=User)
def create_parent_profile(sender, instance, created, **kwargs):
    """Yeni istifadəçi yarandıqda avtomatik profil yarat"""
    if created:
        ParentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_parent_profile(sender, instance, **kwargs):
    """İstifadəçi yenilənəndə profili də yenilə"""
    if hasattr(instance, 'parent_profile'):
        instance.parent_profile.save()
