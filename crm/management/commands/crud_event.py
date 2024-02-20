# myapp/management/commands/crud_commands.py

from django.core.management.base import BaseCommand
from crm.models import Event, Contract, Staff
from login.models import Staff


class CreateEventCommand(BaseCommand):
    help = 'Create a new event'

    def handle(self, *args, **options):
        contract_id = input("Enter contract ID: ")
        try:
            contract = Contract.objects.get(pk=contract_id)
        except Contract.DoesNotExist:
            self.stdout.write(self.style.ERROR('Contract not found.'))
            return

        event_start_date = input(
            "Enter event start date (YYYY-MM-DD HH:MM:SS): ")
        event_end_date = input("Enter event end date (YYYY-MM-DD HH:MM:SS): ")

        staff_id = input("Enter staff ID (optional, press Enter to skip): ")
        staff = Staff.objects.get(pk=staff_id) if staff_id else None

        location = input("Enter event location: ")
        attendees = input("Enter number of attendees: ")
        notes = input("Enter event notes: ")

        event = Event.objects.create(
            contract=contract,
            event_start_date=event_start_date,
            event_end_date=event_end_date,
            staff=staff,
            location=location,
            attendees=attendees,
            notes=notes
        )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created event: {event.id}'))


class ListEventsCommand(BaseCommand):
    help = 'List all events'

    def handle(self, *args, **options):
        events = Event.objects.all()

        if events:
            for event in events:
                self.stdout.write(
                    f'{event} - Location: {event.location}, Attendees: {event.attendees}')
        else:
            self.stdout.write('No events found.')


class UpdateEventCommand(BaseCommand):
    help = 'Update event information'

    def handle(self, *args, **options):
        event_id = input("Enter event ID to update: ")
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            self.stdout.write(self.style.ERROR('Event not found.'))
            return

        event_start_date = input(
            "Enter new event start date (YYYY-MM-DD HH:MM:SS): ")
        event_end_date = input(
            "Enter new event end date (YYYY-MM-DD HH:MM:SS): ")

        staff_id = input("Enter staff ID (optional, press Enter to skip): ")
        event.staff = Staff.objects.get(pk=staff_id) if staff_id else None

        location = input("Enter new event location: ")
        attendees = input("Enter new number of attendees: ")
        notes = input("Enter new event notes: ")

        event.event_start_date = event_start_date
        event.event_end_date = event_end_date
        event.location = location
        event.attendees = attendees
        event.notes = notes

        event.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully updated event: {event.id}'))


class DeleteEventCommand(BaseCommand):
    help = 'Delete an event'

    def handle(self, *args, **options):
        event_id = input("Enter event ID to delete: ")
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            self.stdout.write(self.style.ERROR('Event not found.'))
            return

        confirmation = input(f'Are you sure you want to delete Event {
                             event.id}? (yes/no): ').lower()

        if confirmation == 'yes':
            event.delete()
            self.stdout.write(self.style.SUCCESS(
                f'Successfully deleted event: {event.id}'))
        else:
            self.stdout.write(self.style.ERROR('Deletion canceled.'))
