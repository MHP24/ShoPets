from django.shortcuts import render
from django.http import JsonResponse
from Shop.models import PerfilUsuario
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from rest_framework.views import APIView
import json
# Create your views here.
class SubscribersAPI(APIView):
    def get(self, request, idu = 0):
        data = {'message': 'User not found...'}
        if(idu > 0):
            users = list(PerfilUsuario.objects.filter(id=idu).values())
            if(len(users) > 0):
                data = users[0]
        else:
            users = list(PerfilUsuario.objects.values())
            usersFullData = []
            for user in users:
                if(user["esSubscriptor"] == 'Si'):
                    userAuth = User.objects.get(id=user["id"])
                    usersFullData.append(
                    {
                        "id": userAuth.id,
                        "rut": user["rut"],
                        "first_name": userAuth.first_name,
                        "last_name": userAuth.last_name,
                        "username": userAuth.username,
                        "email": userAuth.email,
                        "address": user["direccion"],
                        "subscriber": user["esSubscriptor"],
                        "profile_picture": user["urlImagenUsuario"],
                        "active": userAuth.is_active,
                    })
            data = {'respuesta': 'Ok', 'usuarios': usersFullData}
        return JsonResponse(data)

    def put(self, request, idu):
        data = {'message': 'User not found...'}
        jd = json.loads(request.body)
        users = list(PerfilUsuario.objects.filter(id=idu).values())
        if(len(users) > 0):
            user = PerfilUsuario.objects.get(id = idu)
            user.esSubscriptor = jd["esSubscriptor"]
            user.save()
            data = {'message': 'Success'}
        return JsonResponse(data)