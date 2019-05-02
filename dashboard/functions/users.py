from django.utils.crypto import get_random_string
from dashboard.models import *
from django.contrib.auth.models import User


def generate_access_code():

    # Generate the key.
    unique_id = get_random_string(length=32)

    # Add the key to the database.
    AccessCode.objects.create(
        key=unique_id,
    )

    # Return the generate key.
    return unique_id
