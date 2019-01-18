
from django.core.management.base import BaseCommand
from oauth2_provider.generators import generate_client_id, generate_client_secret
from oauth2_provider.models import get_application_model
from django.forms.models import model_to_dict
import random
import string
import json

class Command(BaseCommand):
    help = "Create public application for password grant type"

    def handle(self, *args, **options):
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        client_id = generate_client_id()
        client_secret = generate_client_secret()
        client_type = 'public'
        authorization_grant_type = 'password'
        redirect_uris = ''
        skip_authorization = False
        # Save application
        application = get_application_model().objects.create(name=name, client_id=client_id, client_secret=client_secret, client_type=client_type,
                authorization_grant_type=authorization_grant_type, redirect_uris=redirect_uris, skip_authorization=skip_authorization)
        # Print application data
        print(json.dumps(model_to_dict(application), indent=4))
