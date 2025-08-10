from django.urls import path
from .views import edit_plan_stops
from . import views

urlpatterns = [
    path("plans/new/", views.plan_new, name="plan_new"),
    path("plans/<int:plan_id>/stops/", edit_plan_stops, name="edit_plan_stops"),
]

