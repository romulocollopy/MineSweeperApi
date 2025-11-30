from django.urls import path

from . import views

urlpatterns = [
    path("csrf_token/", views.CSRFView.as_view(), name="csrf_token"),
]
