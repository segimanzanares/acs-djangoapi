"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from shows import views
from . import token

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'api/v1/shows', views.ShowViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url("oauth/token/$", token.TokenView.as_view(), name="token"),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # The API URLs are now determined automatically by the router.
    path('', include(router.urls)),
    path('shows/', views.shows_index, name="shows.index"),
    path('logout/', views.logout, name="logout"),
]
