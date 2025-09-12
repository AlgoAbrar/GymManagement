from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User


@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created and not instance.is_verified:
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = default_token_generator.make_token(instance)
        activation_link = f"{settings.BACKEND_URL}/api/v1/accounts/activate/{uid}/{token}/"

        subject = "Verify your AlgoFit account"
        message = f"Hi {instance.username},\n\nPlease verify your email by clicking the link below:\n{activation_link}\n\nThank you for joining AlgoFit!"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
