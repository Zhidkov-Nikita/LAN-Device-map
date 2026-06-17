from django.http import JsonResponse
from django.shortcuts import render

from .models import Room


def home(request):
    rooms = Room.objects.filter(floor=1)
    context = {"rooms": rooms}
    return render(request, "map/index.html", context)


def rooms_api(request):
    rooms = Room.objects.filter(floor=1).values("name", "code", "coordinates", "fill_color")
    return JsonResponse(list(rooms), safe=False)
