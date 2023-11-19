from django.shortcuts import redirect, render

from .models import Message


def index(request):
    if request.method == 'POST':
        text = request.POST['message']
        message = Message(sender=request.user, text=text)
        message.save()

    try:
        messages = Message.objects.all()
    except:
        return redirect('blog:index')

    context = { 'messages': messages }
    return render(request, 'blog/index.html', context=context)
