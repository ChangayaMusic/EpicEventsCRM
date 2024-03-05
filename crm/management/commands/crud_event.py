from django.core.management.base import BaseCommand, CommandError
from crm.models import Event, Contract, Staff
from login.authorization import (
    sales_required,
    event_update_permission_required,
    management_required,
    support_required
)

class Command(BaseCommand):
    help = 'Create, list, update, or delete events'

    def add_arguments(self, parser):
        parser.add_argument('action', choices=[
                            'create_event', 'list_events', 'update_event', 'delete_event', 'show_events_without_support', 'assign_support_contact', 'list_my_events'])

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
        elif action == 'show_events_without_support':
            self.show_events_without_support()
        elif action == 'assign_support_contact':
            event_id = input("Enter event ID to assign support contact: ")
            staff_id = input("Enter staff ID to assign as support contact: ")
            result = self.assign_support_contact(event_id, staff_id)
            self.stdout.write(self.style.SUCCESS(result))
        elif action == 'list_my_events':
            user_id = input("Enter user ID to list their events: ")
            self.list_my_events(user_id)
            
    @sales_required
    def create_event(self):
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

    def list_events(self):
        events = Event.objects.all()

        if events:
            for event in events:
                self.stdout.write(f'Event ID: {
                                  event.id} - Location: {event.location}, Attendees: {event.attendees}')
        else:
            self.stdout.write('No events found.')

    @event_update_permission_required
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

        staff_id = input(f"Enter staff ID (optional, current: {
                         event.staff_id}, press Enter to keep current): ") or event.staff_id
        event.staff = Staff.objects.get(pk=staff_id) if staff_id else None

        location = input(f"Enter new event location (current: {
                         event.location}, press Enter to keep current): ") or event.location
        attendees = input(f"Enter new number of attendees (current: {
                          event.attendees}, press Enter to keep current): ") or event.attendees
        notes = input(f"Enter new event notes (current: {
                      event.notes}, press Enter to keep current): ") or event.notes

        event.event_start_date = event_start_date
        event.event_end_date = event_end_date
        event.location = location
        event.attendees = attendees
        event.notes = notes

        event.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully updated event: {event.id}'))

    @event_update_permission_required
    def delete_event(self):
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

    @management_required
    def show_events_without_support(self):
        events_without_support = Event.objects.filter(support=None)

        if events_without_support:
            for event in events_without_support:
                print(
                    f"Event {event.id} - {event.client.full_name}, No Support Assigned")
        else:
            print("No events without support found.")

    @management_required
    def assign_support_contact(self, event_id, staff_id):
        try:
            event = Event.objects.get(pk=event_id)
            staff = Staff.objects.get(pk=staff_id)
        except Event.DoesNotExist:
            raise CommandError('Event not found.')
        except Staff.DoesNotExist:
            raise CommandError('Staff not found.')

        event.support_contact = staff
        event.save()
        return f'Successfully assigned {staff.full_name} as support contact for Event {event.id}.'

    @support_required
    def list_my_events(self, user_id):
        # Filter events where the user is the support_contact
        events = Event.objects.filter(support_contact__id=user_id)

        if events:
            for event in events:
                self.stdout.write(f'Event ID: {event.id} - Location: {event.location}, Attendees: {event.attendees}')
        else:
            self.stdout.write('No events found for the current user.')