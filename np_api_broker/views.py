from django.shortcuts import render


def index(request):
    context = {
        'np_external_auth': 'LIOT',
    }
    return render(request, 'np_api_broker/index.html', context)

