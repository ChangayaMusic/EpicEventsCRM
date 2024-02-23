# login/management/commands/crud_commands.py

from django.core.management.base import BaseCommand
from login.models import Staff
from django.contrib.auth.hashers import make_password, check_password


class Command(BaseCommand):
    help = 'Create, list, update, or delete staff members'

    def add_arguments(self, parser):
        parser.add_argument('action', choices=[
                            'create_staff', 'list_staff', 'update_staff', 'delete_staff'])

    def handle(self, *args, **options):
        action = options['action']

        if action == 'create_staff':
            self.create_staff()
        elif action == 'list_staff':
            self.list_staff()
        elif action == 'update_staff':
            self.update_staff()
        elif action == 'delete_staff':
            self.delete_staff()

    def create_staff(self):
        name = input("Enter staff member name: ")
        email = input("Enter staff member email: ")
        department = input(
            "Enter staff member department (Sales/Support/Management): ").capitalize()
        password = input("Enter staff member password: ")

        staff = Staff.objects.create(
            name=name,
            email=email,
            department=department,
            username=email  # Set username to the email
        )
        staff.set_password(password)
        staff.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created staff member: {staff.name}'))


    def list_staff(self):
        staff_members = Staff.objects.all()

        if staff_members:
            for staff_member in staff_members:
                self.stdout.write(f'ID: {staff_member.id}, Name: {staff_member.name} - Email: {staff_member.email}, Department: {staff_member.department}')
        else:
            self.stdout.write('No staff members found.')

    def update_staff(self):
        staff_id = input("Enter staff member ID to update: ")
        try:
            staff = Staff.objects.get(pk=staff_id)
        except Staff.DoesNotExist:
            self.stdout.write(self.style.ERROR('Staff member not found.'))
            return

        name = input("Enter new staff member name: ")
        email = input("Enter new staff member email: ")
        department = input(
            "Enter new staff member department (Sales/Support/Management): ").capitalize()
        password = input(
            "Enter new staff member password (press Enter to keep current password): ")

        staff.name = name
        staff.email = email
        staff.department = department

        if password:
            staff.set_password(password)

        staff.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully updated staff member: {staff.name}'))

    def delete_staff(self):
        staff_id = input("Enter staff member ID to delete: ")
        try:
            staff = Staff.objects.get(pk=staff_id)
        except Staff.DoesNotExist:
            self.stdout.write(self.style.ERROR('Staff member not found.'))
            return

        confirmation = input(f'Are you sure you want to delete {staff.name}? (yes/no): ')


        if confirmation == 'yes':
            staff.delete()
            self.stdout.write(self.style.SUCCESS(
                f'Successfully deleted staff member: {staff.name}'))
        else:
            self.stdout.write(self.style.ERROR('Deletion canceled.'))
