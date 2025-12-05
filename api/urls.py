from django.urls import path
from .views import bbc_tech_latest

urlpatterns = [
    path("bbc-tech/", bbc_tech_latest),
]
