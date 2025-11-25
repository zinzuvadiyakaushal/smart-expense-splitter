from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Member

@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        member_name = instance.get_full_name() or instance.username
        Member.objects.create(
            name=member_name,
            email=instance.email,
            user=instance,
        )

@receiver(post_save, sender=User)
def save_member_profile(sender, instance, **kwargs):
    try:
        member = instance.member_profile
        member.name = instance.get_full_name() or instance.username
        member.email = instance.email
        member.save()
    except Member.DoesNotExist:
        member_name = instance.get_full_name() or instance.username
        Member.objects.create(name=member_name, email=instance.email, user=instance)
