from django.shortcuts import render


def hello_world(request):
    return render(request, 'common/hello_world.html', {})
