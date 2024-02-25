from django.core.management.base import CommandError
from crm.models import SUPPORT, SALES, MANAGEMENT
from rest_framework_simplejwt.tokens import AccessToken

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
            raise CommandError("You don't have permission to run this command.")
    return wrapper

def support_required(command_func):
    def wrapper(request, *args, **kwargs):
        if is_support(request):
            return command_func(request, *args, **kwargs)
        else:
            raise CommandError("You don't have permission to run this command.")
    return wrapper

def management_required(command_func):
    def wrapper(request, *args, **kwargs):
        if is_management(request):
            return command_func(request, *args, **kwargs)
        else:
            raise CommandError("You don't have permission to run this command.")
    return wrapper
