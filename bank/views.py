from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Account


def index(request):
    return render(request, 'bank/index.html')


def transfer(send, receive, amount):
    pass


@login_required
def account(request, username):
    if request.method == 'POST':
        pass

    try:
        account = Account.objects.get(owner__username=username)
        others = Account.objects.exclude(owner__username=username)
    except:
        return redirect('bank:index')

    context = { 'account': account, 'others': others }
    return render(request, 'bank/account.html', context)
