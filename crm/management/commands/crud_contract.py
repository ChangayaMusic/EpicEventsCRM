from django.core.management.base import BaseCommand
from crm.models import Contract, Client
from login.models import Staff
from login.authorization import management_required, sales_or_management_required

class Command(BaseCommand):
    help = 'Create, list, update, or delete contracts'

    def add_arguments(self, parser):
        parser.add_argument('action', choices=['create_contract', 'list_contracts', 'update_contract', 'delete_contract', 'show_unsigned', 'show_due'])

    def handle(self, *args, **options):
        action = options['action']

        if action == 'create_contract':
            self.create_contract()
        elif action == 'list_contracts':
            self.list_contracts()
        elif action == 'update_contract':
            self.update_contract()
        elif action == 'delete_contract':
            self.delete_contract()
        elif action == 'show_unsigned':
            self.show_unsigned()
        elif action == 'show_due':
            self.show_due()
            
    @management_required
    def create_contract(self):
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

    def list_contracts(self):
        contracts = Contract.objects.all()

        if contracts:
            for contract in contracts:
                self.stdout.write(f'ID: {contract.id} - Status: {"Signed" if contract.status else "Not Signed"}')
        else:
            self.stdout.write('No contracts found.')
            
    @sales_or_management_required
    def update_contract(self):
        contract_id = input("Enter contract ID to update: ")
        try:
            contract = Contract.objects.get(pk=contract_id)
        except Contract.DoesNotExist:
            self.stdout.write(self.style.ERROR('Contract not found.'))
            return

        total_amount = input(f'Enter new total amount (current: {contract.total_amount}): ') or contract.total_amount
        amount_due = input(f'Enter new amount due (current: {contract.amount_due}): ') or contract.amount_due
        status = input(f'Is the contract signed? (yes/no, current: {"yes" if contract.status else "no"}): ').lower() == 'yes'

        contract.total_amount = total_amount
        contract.amount_due = amount_due
        contract.status = status

        contract.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully updated contract: {contract.id}'))
    @management_required
    def delete_contract(self):
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

    @sales_or_management_required
    def show_unsigned(self):
        unsigned_contracts = Contract.objects.filter(status=False)

        for contract in unsigned_contracts:
            print(f"Contract {contract.id} - {contract.client.full_name}, Status: {'Not Signed'}")

    @sales_or_management_required
    def show_due(self):
        contracts_with_amount_due = Contract.objects.filter(amount_due__gt=0)

        for contract in contracts_with_amount_due:
            print(f"Contract {contract.id} - {contract.client.full_name}, Amount Due: {contract.amount_due}")