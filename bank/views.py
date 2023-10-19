from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Account


def index(request):
    return render(request, 'bank/index.html')


@login_required
def account(request, iban):
    try:
        account = Account.objects.get(iban=iban)
    except:
        return redirect('bank:index')

    context = { 'account': account }
    return render(request, 'bank/account.html', context)
