from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def list(request):
    guestbooklist = Guestbook.objects.all().order_by('-regdate')
    data = {
        'list': guestbooklist
    }

    return render(request, 'guestbook/list.html', data)


def add(request):
    guestbook = Guestbook()
    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.contents = request.POST['contents']

    guestbook.save()

    return HttpResponseRedirect('/guestbook')


def deleteform(request, id=0):
    data = {'id':id}

    return render(request, 'guestbook/deleteform.html', data)


def delete(request):
    id = request.POST['no']
    password = request.POST['password']
    guestbook = Guestbook.objects.filter(id=id).filter(password=password)
    guestbook.delete()

    return HttpResponseRedirect('/guestbook')