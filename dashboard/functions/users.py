from django.utils.crypto import get_random_string
from dashboard.models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):

    # Create email confirmation token.
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


def generate_access_code():

    # Generate the key.
    unique_id = get_random_string(length=32)

    # Add the key to the database.
    AccessCode.objects.create(
        key=unique_id,
    )

    # Return the generate key.
    return unique_id


account_activation_token = TokenGenerator()

