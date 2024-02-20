from django.core.management.base import BaseCommand
from crm.models import Client

class Command(BaseCommand):
    help = 'Create, list, update, or delete clients'

    def add_arguments(self, parser):
        parser.add_argument('action', choices=['create_client', 'list_clients', 'update_client', 'delete_client'])

    def handle(self, *args, **options):
        action = options['action']

        if action == 'create_client':
            self.create_client()
        elif action == 'list_clients':
            self.list_clients()
        elif action == 'update_client':
            self.update_client()
        elif action == 'delete_client':
            self.delete_client()

    def create_client(self):
        full_name = input("Enter full name: ")
        email = input("Enter email: ")
        phone = input("Enter phone: ")
        company_name = input("Enter company name: ")

        client = Client.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created client: {client.full_name}'))

    def list_clients(self):
        clients = Client.objects.all()

        if clients:
            for client in clients:
                self.stdout.write(f'ID: {client.id}, {client.full_name} - {client.email}')
        else:
            self.stdout.write('No clients found.')

    def update_client(self):
        client_id = input("Enter client ID to update: ")
        try:
            client = Client.objects.get(pk=client_id)
        except (Client.DoesNotExist, ValueError):
            self.stdout.write(self.style.ERROR('Invalid client ID or client not found.'))
            return

        client.full_name = input(f'Enter new full name (current: {client.full_name}): ') or client.full_name
        client.email = input(f'Enter new email (current: {client.email}): ') or client.email
        client.phone = input(f'Enter new phone (current: {client.phone}): ') or client.phone
        client.company_name = input(f'Enter new company name (current: {client.company_name}): ') or client.company_name

        client.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully updated client: {client.full_name}'))

    def delete_client(self):
        client_id = input("Enter client ID to delete: ")
        try:
            client = Client.objects.get(pk=client_id)
        except (Client.DoesNotExist, ValueError):
            self.stdout.write(self.style.ERROR('Invalid client ID or client not found.'))
            return

        confirmation = input(f'Are you sure you want to delete {client.full_name}? (yes/no): ')

        if confirmation.lower() == 'yes':
            client.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted client: {client.full_name}'))
        else:
            self.stdout.write(self.style.ERROR('Deletion canceled.'))
