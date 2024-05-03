from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status


@csrf_exempt
@api_view(['POST'])
def login(request):
    data = JSONParser().parse(request)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return Response('Se requiere nombre de usuario y Contraseña', status= status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username = username, password = password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response('Credenciales Inválidas',status= status.HTTP_400_BAD_REQUEST)    