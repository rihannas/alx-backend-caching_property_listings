from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property

# Cache response for 15 minutes (900 seconds)
@cache_page(60 * 15)
def property_list(request):
    properties = Property.objects.all().values(
        "id", "title", "description", "price", "location", "created_at"
    )
    return JsonResponse(list(properties), safe=False)
