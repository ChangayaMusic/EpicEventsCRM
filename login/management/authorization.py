from django.core.management.base import CommandError
from crm.models import SUPPORT, SALES, MANAGEMENT
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.decorators import user_passes_test


def get_user_role(request):
    if request.user.is_authenticated:
        try:
            # Utilisez le token pour extraire les informations de l'utilisateur
            token = AccessToken(request.auth)
            role = token.payload.get('role')
            return role
        except Exception as e:
            # Gérez les erreurs si le token ne peut pas être analysé
            print(f"Error extracting user role from token: {e}")
            return None
    return None


def is_sales(request):
    return get_user_role(request) == 'Sales'


def is_support(request):
    return get_user_role(request) == 'Support'


def is_management(request):
    return get_user_role(request) == 'Management'


def sales_required(command_func):
    def wrapper(request, *args, **kwargs):
        if is_sales(request):
            return command_func(request, *args, **kwargs)
        else:
            raise CommandError(
                "You don't have permission to run this command.")
    return wrapper


def support_required(command_func):
    def wrapper(request, *args, **kwargs):
        if is_support(request):
            return command_func(request, *args, **kwargs)
        else:
            raise CommandError(
                "You don't have permission to run this command.")
    return wrapper


def management_required(command_func):
    def wrapper(request, *args, **kwargs):
        if is_management(request):
            return command_func(request, *args, **kwargs)
        else:
            raise CommandError(
                "You don't have permission to run this command.")
    return wrapper


def superuser_required(command_func):
    def wrapper(request, *args, **kwargs):
        if is_superuser(request):
            return command_func(request, *args, **kwargs)
        else:
            raise CommandError(
                "You don't have permission to run this command.")
    return wrapper

def is_sales_or_management(user):
    return is_sales(user) or is_management(user)

def sales_or_management_required(command_func):
    return user_passes_test(is_sales_or_management)(command_func)

def can_update_event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return False

    # Check if the user is the event's support_contact or is staff
    return request.user == event.support_contact or request.user.is_staff

def event_update_permission_required(command_func):
    def wrapper(request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        if can_update_event(request, event_id):
            return command_func(request, *args, **kwargs)
        else:
            raise PermissionDenied("You don't have permission to update this event.")
    return wrapper

def is_management_or_client_staff(request, client):
    return is_management(request) or client.staff == request.user

def is_management_or_contract_staff(request, contract):
    return is_management(request) or (is_contract(request) and contract.staff == request.user)
def management_or_client_staff_required(command_func):
    @wraps(command_func)
    def wrapper(request, *args, **kwargs):
        client_id = kwargs.get('client_id')  # Assuming you pass the client_id as a keyword argument
        if client_id is not None:
            try:
                client = Client.objects.get(pk=client_id)
            except Client.DoesNotExist:
                raise CommandError('Invalid client ID or client not found.')

            if is_management(request) or (is_client(request) and client.staff == request.user):
                return command_func(request, client, *args, **kwargs)
        raise CommandError("You don't have permission to run this command.")
    return wrapper
def management_or_contract_staff_required(command_func):
    @wraps(command_func)
    def wrapper(request, *args, **kwargs):
        contract_id = kwargs.get('contract_id')  # Assuming you pass the contract_id as a keyword argument
        if contract_id is not None:
            try:
                contract = Contract.objects.get(pk=contract_id)
            except Contract.DoesNotExist:
                raise CommandError('Invalid contract ID or contract not found.')

            if is_management_or_contract_staff(request, contract):
                return command_func(request, contract, *args, **kwargs)
        raise CommandError("You don't have permission to run this command.")
    return wrapper

