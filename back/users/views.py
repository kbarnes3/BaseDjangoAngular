from django.conf import settings
from django.http import JsonResponse


def site_config(request):
    return JsonResponse({
        'account_creation_mode': getattr(settings, 'ACCOUNT_CREATION_MODE', 'default'),
    })