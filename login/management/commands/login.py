from django.core.management.base import BaseCommand
from login.models import Staff


class LoginCommand(BaseCommand):
    def handle(self, *args, **options):
        email = input("Enter email: ")
        password = input("Enter password: ")

        try:
            user = Staff.objects.get(email=email)
            if user.check_password(password):
                token_data = user.create_jwt()
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully logged in.\nToken: {token_data}'))
            else:
                self.stdout.write(self.style.ERROR(
                    'Incorrect password. Please try again.'))
        except Staff.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'User not found. Please check the email address.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
