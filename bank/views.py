from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Account


@transaction.atomic
def transfer(sender_username, receiver_username, amount):
    sender = Account.objects.get(owner__username=sender_username)
    receiver = Account.objects.get(owner__username=receiver_username)

    illegal_argument = not 0 <= amount <= sender.balance
    if settings.FIX_FLAWS and illegal_argument:
        return

    sender.balance -= amount
    receiver.balance += amount
    sender.save()
    receiver.save()


@login_required
def account(request, username):
    authorised = username == request.user.username
    if settings.FIX_FLAWS and not authorised:
        return redirect('blog:index')

    if request.method == 'POST':
        receiver_username = request.POST['receiver']
        amount = int(request.POST['amount'])
        transfer(username, receiver_username, amount)

    try:
        account = Account.objects.get(owner__username=username)
        others = Account.objects.exclude(owner__username=username)
    except:
        return redirect('blog:index')

    context = {
        'account': account,
        'others': others,
        'FIX_FLAWS': settings.FIX_FLAWS
    }
    return render(request, 'bank/account.html', context)
