from django.http import JsonResponse


def logged_in_api(request):
    results = {'loggedIn': False}
    if request.user.is_authenticated:
        results['loggedIn'] = True
        results['givenName'] = request.user.given_name
        results['surname'] = request.user.surname

    return JsonResponse(results)
