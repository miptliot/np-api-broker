from django.shortcuts import render, redirect


def index(request):
    context = {
        'np_external_auth': 'LIOT',
        'user': request.user,
    }
    return render(request, 'np_api_broker/index.html', context)


def login(request):
    return redirect('/docs')