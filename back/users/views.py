from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect, render

from users.forms import UserCreationForm


def create_user_account(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            primary_email = form.cleaned_data['primary_email']
            password = form.cleaned_data['password1']

            user = authenticate(username=primary_email, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'users/create_user_account.html', {'form': form})


def logged_in_api(request):
    results = {'loggedIn': False}
    if request.user.is_authenticated:
        results['loggedIn'] = True
        results['givenName'] = request.user.given_name
        results['surname'] = request.user.surname

    return JsonResponse(results)
