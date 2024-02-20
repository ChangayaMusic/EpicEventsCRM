from django.core.management.base import BaseCommand
from crm.models import Client

class CreateClientCommand(BaseCommand):
    help = 'Create a new client'

    def handle(self, *args, **options):
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

class ListClientsCommand(BaseCommand):
    help = 'List all clients'

    def handle(self, *args, **options):
        clients = Client.objects.all()

        if clients:
            for client in clients:
                self.stdout.write(f'{client.full_name} - {client.email}')
        else:
            self.stdout.write('No clients found.')

class UpdateClientCommand(BaseCommand):
    help = 'Update client information'

    def handle(self, *args, **options):
        client_id = input("Enter client ID to update: ")
        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR('Client not found.'))
            return

        client.full_name = input("Enter new full name: ")
        client.email = input("Enter new email: ")
        client.phone = input("Enter new phone: ")
        client.company_name = input("Enter new company name: ")

        client.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully updated client: {client.full_name}'))

class DeleteClientCommand(BaseCommand):
    help = 'Delete a client'

    def handle(self, *args, **options):
        client_id = input("Enter client ID to delete: ")
        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR('Client not found.'))
            return

        confirmation = input(f'Are you sure you want to delete {client.full_name}? (yes/no): ').lower()

        if confirmation == 'yes':
            client.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted client: {client.full_name}'))
        else:
            self.stdout.write(self.style.ERROR('Deletion canceled.'))