from unicodedata import name
from django.urls import path, include
from Login import views
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.LoginViewSet, basename="Login")

urlpatterns = [
    path('', include(router.urls)),

]

