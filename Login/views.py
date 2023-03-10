from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SignupForm, LoginUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
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
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('Sudoku-sudoku'))
            return Response(data="", status=status.HTTP_400_BAD_REQUEST)

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
        return HttpResponseRedirect(reverse('Sudoku-sudoku'))


class signUp(SuccessMessageMixin, generic.CreateView):
    form_class = SignupForm
    template_name = "Login/register.html"
    success_url = reverse_lazy('login')
    success_message = "User has been created, please login with your username and password"

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             "Please enter details properly")
        return redirect('Sudoku-sudoku')


class logIn(generic.View):
    form_class = LoginUserForm
    template_name = "Login/login.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == "POST":
            form = LoginUserForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(
                        request, f"You are logged in as {username}")
                    return redirect('Sudoku-sudoku')
                else:
                    messages.error(request, "Error")
            else:
                messages.error(request, "Username or password incorrect")
        form = LoginUserForm()
        return render(request, "Login/login.html", {"form": form})


class logOut(LoginRequiredMixin, generic.View):
    login_url = 'login'

    def get(self, request):
        logout(request)
        messages.success(request, "User logged out")
        return redirect('Sudoku-sudoku')
