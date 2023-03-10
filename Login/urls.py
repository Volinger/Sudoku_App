from unicodedata import name
from django.urls import path, include
from Login import views
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'login', views.LoginViewSet, basename="Login")

urlpatterns = [
    # path('create-new-account/', views.signUp.as_view(), name="register"),
    # path('login/', views.logIn.as_view(), name="login"),
    # path('logout/', views.logOut.as_view(), name="logout"),
    path('', include(router.urls)),

]

