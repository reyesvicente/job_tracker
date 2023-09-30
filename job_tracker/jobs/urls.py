from django.urls import path
from .views import (
    ApplicationCreateView,
    ApplicationDeleteView,
    ApplicationDetailView,
    ApplicationListView,
    ApplicationUpdateView,
)

app_name = "jobs"

urlpatterns = [
    path("", ApplicationListView.as_view(), name="list"),
    path("add/", ApplicationCreateView.as_view(), name="add"),
    path("<str:slug>/", ApplicationDetailView.as_view(), name="detail"),
    path("<str:slug>/update/", ApplicationUpdateView.as_view(), name="update"),
    path("<str:slug>/delete/", ApplicationDeleteView.as_view(), name="delete"),
]
