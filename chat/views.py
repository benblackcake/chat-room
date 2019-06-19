from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
import uuid

# Create your views here.
from chat.models import Message


def index(request):
    uid4 = str(uuid.uuid4())
    return render(request, 'chat/index.html', {'uid4': uid4})


def room(request, room_name):

    chat_messages = Message.objects.filter(group_name=room_name).order_by("created")
    for i in chat_messages:
        print(i.message)
    print("__debug__")
    return render(request, 'chat/room.html', {
        'chat_messages': chat_messages,
        'room_name': room_name
    })
