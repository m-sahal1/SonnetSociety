from django.shortcuts import render, redirect

# from django.http import HttpResponse
# Create your views here.
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {"id": 1, "name": "python"},
#     {"id": 2, "name": "django"},
#     {"id": 3, "name": "wtf"},
# ]


def home(request):
    query = None
    if request.GET.get("q") != None:
        query = request.GET.get("q")
    else:
        query = ""
    rooms = Room.objects.filter(topic__name__icontains=query)# icontains means it is not case sensitive, just contains means it is case sensitive
    topics = Topic.objects.all()
    context = {"rooms": rooms, "topics": topics}
    return render(
        request, "base/home.html", context
    )  # render generates html files not strings


def room(request, pk):
    room = Room.objects.get(id=pk)

    context = {"room": room}
    return render(request, "base/room.html", context)


def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "base/room_form.html", {"form": form})


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})
