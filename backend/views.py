from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework import status
from rest_framework.response import Response


@api_view(["GET", "POST"])
def drink_list(request):
    if request.method == "GET":
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def drink_details(request, id):
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = DrinkSerializer(instance=drink)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = DrinkSerializer(instance=drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
