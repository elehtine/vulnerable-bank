from django.shortcuts import HttpResponse, redirect

from .models import Account


def index(request):
    return HttpResponse("Hello World!")


def account(request, iban):
    try:
        account = Account.objects.get(iban=iban)
    except:
        return redirect("bank:index")

    return HttpResponse(f"{iban}: {account.balance}")
