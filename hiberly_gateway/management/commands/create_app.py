from oauth2_provider.models import Application
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        app = Application.objects.create(name='hiberly', skip_authorization=True, redirect_uris='https://app.hiberly.com/complete/gitlab/')
        self.stdout.write("Created Hiberly OAuth app")
        self.stdout.write(' - client id: %s' % app.client_id)
        self.stdout.write(' - client secret: %s' % app.client_secret)