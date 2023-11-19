from django.shortcuts import redirect, render
from django.db import connection
from django.conf import settings

from .models import Message


def index(request):
    if request.method == 'POST':
        text = request.POST['message']
        sender_id = request.user.id

        if settings.FIX_FLAWS:
            query = "INSERT INTO blog_message (text, sender_id) VALUES (%s, %s);"
            with connection.cursor() as cursor:
                cursor.execute(query, [text, sender_id])
        else:
            query = f"INSERT INTO blog_message (text, sender_id) VALUES ('{text}', {sender_id});"
            with connection.cursor() as cursor:
                cursor.execute(query)

    try:
        messages = Message.objects.all()
    except:
        return redirect('blog:index')

    context = { 'messages': messages }
    return render(request, 'blog/index.html', context=context)
