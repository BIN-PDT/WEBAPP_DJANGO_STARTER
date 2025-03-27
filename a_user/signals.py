from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import User, Profile


@receiver(pre_save, sender=User)
def standardize_signup_user_information(sender, instance, **kwargs):
    instance.username = instance.username.lower()


@receiver(post_save, sender=User)
def create_or_update_user_information(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        current_email_address = instance.emailaddress_set.get(primary=True)
        if current_email_address.email != instance.email:
            current_email_address.email = instance.email
            current_email_address.verified = False
            current_email_address.save()
