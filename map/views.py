import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import Room


def is_staff_api(user):
    return user.is_staff


def home(request):
    rooms = Room.objects.filter(floor=1)
    rooms_data = [
        {
            "id": r.id,
            "name": r.name,
            "code": r.code,
            "x": r.x,
            "y": r.y,
            "width": r.width,
            "height": r.height,
        }
        for r in rooms
    ]
    context = {
        "rooms": rooms,
        "rooms_json": json.dumps(rooms_data),
    }
    return render(request, "map/index.html", context)


def rooms_api(request):
    rooms = Room.objects.filter(floor=1).values(
        "id", "name", "code", "x", "y", "width", "height"
    )
    return JsonResponse(list(rooms), safe=False)


@require_POST
def save_rooms(request):
    if not request.user.is_staff:
        return JsonResponse(
            {"status": "error", "message": "Только для администратора"},
            status=403,
        )
    try:
        data = json.loads(request.body)
        updates = data.get("rooms", [])
        for item in updates:
            Room.objects.filter(id=item["id"]).update(
                x=item["x"],
                y=item["y"],
                width=item["width"],
                height=item["height"],
            )
        return JsonResponse({"status": "ok", "updated": len(updates)})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
