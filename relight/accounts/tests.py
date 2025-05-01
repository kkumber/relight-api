from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework.test import APIClient
from django.core import mail

User = get_user_model()

class PasswordResetEmailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_email = 'testuser@example.com'
        self.user = User.objects.create_user(email=self.user_email, password='testpassword', username='testusername')

    def test_password_reset_email_content(self):
        response = self.client.post(
            reverse('password_reset:reset-password-request'),
            data={'email': self.user_email}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Click here to reset your password', mail.outbox[0].body)
        self.assertIn(self.user_email, mail.outbox[0].to)
        email = mail.outbox[0]
        print(email.subject)
        print(email.body)
        print(email.to)
