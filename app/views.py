"""Views for the starter project."""

from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response


class HomeView(TemplateView):
    template_name = "app/home.html"


@api_view(["GET"])
def health_check(request):
    return Response(
        {
            "status": "ok",
            "service": "ptech-django-starter",
        }
    )
