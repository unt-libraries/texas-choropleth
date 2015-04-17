from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail

from model_mommy import mommy


class RecoverInvalidTestCase(TestCase):

    def test_password_reset_unknown_email_or_user(self):
        response = self.client.post(
            reverse('password_reset_recover'),
            {'username_or_email': 'unknown'}
        )

        self.assertTrue("An email was sent to" in response.content)
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_known_email_or_user(self):
        user = mommy.make(User, username='tuser', email='test@example.com')

        response = self.client.post(
            reverse('password_reset_recover'),
            {'username_or_email': user.email},
            follow=True
        )

        self.assertTrue("An email was sent to" in response.content)
        self.assertEqual(len(mail.outbox), 1)
