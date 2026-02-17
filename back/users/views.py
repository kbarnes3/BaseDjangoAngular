from django.http import JsonResponse


def logged_in_api(request):
    results = {'loggedIn': False}
    if request.user.is_authenticated:
        results['loggedIn'] = True
        results['firstName'] = request.user.first_name
        results['lastName'] = request.user.last_name

    return JsonResponse(results)
