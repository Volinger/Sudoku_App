from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
import json
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse


class LoginViewSet(viewsets.GenericViewSet):
	serializer_class = RegisterSerializer

	@action(detail=False, methods=['get', 'post'])
	def login(self, request):
		if request.method == 'GET':
			serializer = LoginSerializer()
			return render(request, 'Login/login.html', context={'serializer': serializer})
		else:
			data = json.loads(request.data['data'])
			username = data['username']
			password = data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return Response(data=reverse('Sudoku-sudoku-game'), status=status.HTTP_200_OK)
			data = {"error": "User not recognized. Either specified user does not exist, or the password is incorrect."}
			return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

	@action(detail=False, methods=['get', 'post'])
	def register(self, request):
		if request.method == 'GET':
			serializer = RegisterSerializer()
			return render(request, 'Login/register.html', context={'serializer': serializer})
		else:
			data = json.loads(request.data['data'])
			result = RegisterSerializer(data=data)
			if result.is_valid():
				result.save()
				return Response(data=reverse('Login-login'), status=status.HTTP_200_OK)
			error = result.errors.values()
			data = {"error": error}
			return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

	@action(detail=False, methods=['get'])
	def logout(self, request):
		logout(request)
		return HttpResponseRedirect(reverse('Sudoku-sudoku-game'))
