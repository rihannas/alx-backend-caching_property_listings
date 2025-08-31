from django.shortcuts import render
from .utils import get_all_properties

# Create your views here.
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property

def property_list(request):
    properties = get_all_properties()
    # Serialize the list of Property objects
    data = [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "price": float(p.price),
            "location": p.location,
            "created_at": p.created_at,
        }
        for p in properties
    ]
    return JsonResponse(data, safe=False)
