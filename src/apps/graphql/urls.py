from django.urls import path

from . import views
from .schema import schema

urlpatterns = [
    path("", views.SchemaView.as_view(graphiql=True, schema=schema)),
]
