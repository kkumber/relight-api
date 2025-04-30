from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
import os

@receiver(reset_password_token_created)
def send_password_reset_token(sender, instance, reset_password_token, *args, **kwargs):
    # Pull the base URL from the environment
    frontend_base = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    token = reset_password_token.key
    reset_url = f"{frontend_base}/reset-password/{token}"

    send_mail(
        subject="RELIGHT Password Reset",
        message=f"Click here to reset your password: {reset_url}",
        from_email=os.getenv('DEFAULT_FROM_EMAIL'),
        recipient_list=[reset_password_token.user.email],
        fail_silently=False,
    )