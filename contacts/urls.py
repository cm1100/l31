from django.contrib import admin
from django.urls import path,include
from .views import CollegeView

app_name ="contacts"

urlpatterns = [
    path("",CollegeView.as_view(),name="search")
]
