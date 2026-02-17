from django.core.management.base import BaseCommand
from accounts.models import CustomUser

# This command can be run using: python manage.py create_user <email> <password> <role>
class Command(BaseCommand):
    help = 'Create a new user with email and password'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='User Email')
        parser.add_argument('password', type=str, help='User Password')
        parser.add_argument('role', type=str, choices=['ADMIN', 'AUTHOR', 'READER'], help='User Role')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        role = options['role']

        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'User with email {email} already exists.'))
            return

        user = CustomUser.objects.create_user(email=email, password=password, role=role)
        self.stdout.write(self.style.SUCCESS(f'User {email} created successfully with role {role}.'))