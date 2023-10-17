from django.shortcuts import HttpResponse


def index(request):
    return HttpResponse("Hello World!")


def account(request, iban):
    return HttpResponse(f"Account: {iban}")
