"""
allexpensesback URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from .schema import schema
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True))),
]

static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)