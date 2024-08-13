from django.shortcuts import render, redirect
from .models import *
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.


def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    data = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
        )
    topic = Topic.objects.all()
    context = {'data': data, 'topic': topic}
    return render(request, 'room/home.html', context)

def room(request, id):
    room = Room.objects.get(id = id)
    context = {'data': room}
    return render(request, 'room/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'room/create.html', context)


def updateRoom(request, id):
    room = Room.objects.get(id = id)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'room/create.html', context)

def deleteRoom(request, id):
    room = Room.objects.get(id = id)

    if request.method == "POST":
        room.delete()
        return redirect('home')

    return render(request, 'room/delete.html', {'obj': room})


def userLoginRegister(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)

        except:
            messages.error(request, "No such user exist")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username and password don't match")
    
        
    return render(request, 'room/login.html')
