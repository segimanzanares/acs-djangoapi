from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from shows.models import Show
from shows.serializers import ShowSerializer

@csrf_exempt
def show_list(request):
    """
    List all shows, or create a new show.
    """
    if request.method == 'GET':
        shows = Show.objects.all()
        serializer = ShowSerializer(shows, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ShowSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)