from django.core.management.base import BaseCommand
from crm.models import Event, Contract, Staff
import uuid

class Command(BaseCommand):
    help = 'Create, list, update, or delete events'

    def add_arguments(self, parser):
        parser.add_argument('action', choices=['create_event', 'list_events', 'update_event', 'delete_event'])

    def handle(self, *args, **options):
        action = options['action']

        if action == 'create_event':
            self.create_event()
        elif action == 'list_events':
            self.list_events()
        elif action == 'update_event':
            self.update_event()
        elif action == 'delete_event':
            self.delete_event()

    def create_event(self):
        contract_id = input("Enter contract ID: ")
        try:
            contract = Contract.objects.get(pk=contract_id)
        except Contract.DoesNotExist:
            self.stdout.write(self.style.ERROR('Contract not found.'))
            return


        event_start_date = input("Enter event start date (YYYY-MM-DD HH:MM:SS): ")
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

        self.stdout.write(self.style.SUCCESS(f'Successfully created event: {event.id}'))

    def list_events(self):
        events = Event.objects.all()

        if events:
            for event in events:
                self.stdout.write(f'Event ID: {event.id} - Location: {event.location}, Attendees: {event.attendees}')
        else:
            self.stdout.write('No events found.')

    def update_event(self):
        event_id = input("Enter event ID to update: ")
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            self.stdout.write(self.style.ERROR('Event not found.'))
            return

        event_start_date = input(
            f"Enter new event start date (current: {event.event_start_date}, press Enter to keep current): ") or event.event_start_date
        event_end_date = input(
            f"Enter new event end date (current: {event.event_end_date}, press Enter to keep current): ") or event.event_end_date

        staff_id = input(f"Enter staff ID (optional, current: {event.staff_id}, press Enter to keep current): ") or event.staff_id
        event.staff = Staff.objects.get(pk=staff_id) if staff_id else None

        location = input(f"Enter new event location (current: {event.location}, press Enter to keep current): ") or event.location
        attendees = input(f"Enter new number of attendees (current: {event.attendees}, press Enter to keep current): ") or event.attendees
        notes = input(f"Enter new event notes (current: {event.notes}, press Enter to keep current): ") or event.notes

        event.event_start_date = event_start_date
        event.event_end_date = event_end_date
        event.location = location
        event.attendees = attendees
        event.notes = notes

        event.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully updated event: {event.id}'))


    def delete_event(self):
        event_id = input("Enter event ID to delete: ")
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            self.stdout.write(self.style.ERROR('Event not found.'))
            return

        confirmation = input(f'Are you sure you want to delete Event {event.id}? (yes/no): ').lower()

        if confirmation == 'yes':
            event.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted event: {event.id}'))
        else:
            self.stdout.write(self.style.ERROR('Deletion canceled.'))
