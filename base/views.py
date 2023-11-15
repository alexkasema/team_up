from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q #! this enables us to add (&& or ||) so as to chain statements

#from django.contrib.auth.models import User #! remove this because we created a custom user model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages #! for flash messages

from . models import Room, Topic, Message, User
from .forms import RoomForm, UserForm

"""
rooms = [
    {"id": "1", "name": "Lets learn Python"},
    {"id": "2", "name": "Canva designs"},
    {"id": "3", "name": "Who is into Django?"},
    {"id": "4", "name": "API development with Django"},
]
"""

#! login is a key word
def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'username or password is incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #! this will hold the values so that we can 'clean' them
            user.username = user.username.lower()
            user.save()
            login(request, user) #! login the user we just registered
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during Registration')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        ) #! we filtered upwards from the Room model
    topics = Topic.objects.all()[0:5]

    room_count = rooms.count() #! counts number of rooms

    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    ) #! this is where you can change to what you exactly need

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):

    room = Room.objects.get(id=pk)
    #!querying child object of a specific room
    #! this is saying give us a set of messages that are related to this specific room 
    #! room_messages = room.message_set.all().order_by('-created') #! room.message_set.all() is one to many relationship
    room_messages = room.message_set.all()
    participants = room.participants.all() #! many to many relationship

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'), #! getting it from the form
        )
        room.participants.add(request.user) #! add a participant to the room

        return redirect('room', pk = room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)

    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
        """form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
        """
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room) #! The form will be pre filled with the room value

    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        """ form = RoomForm(request.POST, instance=room) #! instance allows you to update a specific form
        if form.is_valid():
            form.save()
            return redirect('home')
        """

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here!!")

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk = user.id)

    context = {'form': form}
    return render(request, 'base/update-user.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)

def activityPage(request):

    room_messages = Message.objects.all()

    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)