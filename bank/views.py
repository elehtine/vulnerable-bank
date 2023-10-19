from django.conf import settings
from django.shortcuts import redirect, render

from .models import Account


def index(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    return render(request, 'bank/index.html')


def account(request, iban):
    try:
        account = Account.objects.get(iban=iban)
    except:
        return redirect('bank:index')

    context = { 'account': account }
    return render(request, 'bank/account.html', context)
