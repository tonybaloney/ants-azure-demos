from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("break", views.as_breakpoint, name="break"),
    path("exc", views.as_exception, name="exc"),
]