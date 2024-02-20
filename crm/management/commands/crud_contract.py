from django.core.management.base import BaseCommand
from crm.models import Contract, Client
from login.models import Staff

class CreateContractCommand(BaseCommand):
    help = 'Create a new contract'

    def handle(self, *args, **options):
        client_id = input("Enter client ID: ")
        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR('Client not found.'))
            return

        staff_id = input("Enter staff ID (optional, press Enter to skip): ")
        staff = Staff.objects.get(pk=staff_id) if staff_id else None

        total_amount = input("Enter total amount: ")
        amount_due = input("Enter amount due: ")
        status = input("Is the contract signed? (yes/no): ").lower() == 'yes'

        contract = Contract.objects.create(
            client=client,
            staff=staff,
            total_amount=total_amount,
            amount_due=amount_due,
            status=status
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created contract: {contract.id}'))

class ListContractsCommand(BaseCommand):
    help = 'List all contracts'

    def handle(self, *args, **options):
        contracts = Contract.objects.all()

        if contracts:
            for contract in contracts:
                self.stdout.write(f'{contract} - Status: {"Signed" if contract.status else "Not Signed"}')
        else:
            self.stdout.write('No contracts found.')

class UpdateContractCommand(BaseCommand):
    help = 'Update contract information'

    def handle(self, *args, **options):
        contract_id = input("Enter contract ID to update: ")
        try:
            contract = Contract.objects.get(pk=contract_id)
        except Contract.DoesNotExist:
            self.stdout.write(self.style.ERROR('Contract not found.'))
            return

        total_amount = input("Enter new total amount: ")
        amount_due = input("Enter new amount due: ")
        status = input("Is the contract signed? (yes/no): ").lower() == 'yes'

        contract.total_amount = total_amount
        contract.amount_due = amount_due
        contract.status = status

        contract.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully updated contract: {contract.id}'))

class DeleteContractCommand(BaseCommand):
    help = 'Delete a contract'

    def handle(self, *args, **options):
        contract_id = input("Enter contract ID to delete: ")
        try:
            contract = Contract.objects.get(pk=contract_id)
        except Contract.DoesNotExist:
            self.stdout.write(self.style.ERROR('Contract not found.'))
            return

        confirmation = input(f'Are you sure you want to delete Contract {contract.id}? (yes/no): ').lower()

        if confirmation == 'yes':
            contract.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted contract: {contract.id}'))
        else:
            self.stdout.write(self.style.ERROR('Deletion canceled.'))