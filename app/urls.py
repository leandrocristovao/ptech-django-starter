from django.urls import path

from .views import HomeView, health_check

app_name = "app"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("api/health/", health_check, name="health"),
]
