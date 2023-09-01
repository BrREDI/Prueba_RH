from typing import Any
from django import http
from django.shortcuts import render
from django.views import View
from .models import Task
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime

# Create your views here.
class TaskView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self,request,id=0):
        if(id>0):
            tasks=list(Task.objects.filter(id=id).values())
            if len(tasks)>0:
                task = tasks[0]
                datos={'message':"Success","tasks":task}
            else:
                datos={'message':"No tasks..."}
            return JsonResponse(datos)
        else:
            tasks= list(Task.objects.values())
            if len(tasks)>0:
                datos={'message':"Success","tasks":tasks}
            else:
                datos={'message':"No tasks..."}
            return JsonResponse(datos)

    def post(self,request):
        jd = json.loads(request.body)
        Task.objects.create(title=jd['title'],description=jd['description'],status=jd['status'],create_at=jd['create_at'],update_at=jd['update_at'])
        datos={'message':"Success"}
        return JsonResponse(datos)
    def put(self,request,id):
        jd = json.loads(request.body)
        tasks = list(Task.objects.filter(id=id).values())
        if len(tasks)>0:
            task = Task.objects.get(id=id)
            task.title = jd['title']
            task.description = jd['description']
            task.status = jd['status']
            task.create_at = jd['create_at']
            task.update_at = jd['update_at']
            task.save()
            datos={'message':"Success"}
        else:
            datos={'message':"No tasks..."}
        return JsonResponse(datos)
    def delete(self,request,id):
        tasks = list(Task.objects.filter(id=id).values())
        if len(tasks)>0:
            Task.objects.filter(id=id).delete()
            datos={'message':"Success"}
        else:
            datos={'message':"No tasks..."}
        return JsonResponse(datos)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
