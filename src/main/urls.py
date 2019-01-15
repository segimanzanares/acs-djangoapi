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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from shows import api_views, views
from . import token

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'api/v1/shows', api_views.ShowViewSet)

urlpatterns = [
    url("oauth/token/$", token.TokenView.as_view(), name="token"),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # The API URLs are now determined automatically by the router.
    path('', include(router.urls)),
    # Admin
    path('shows/', views.ShowList.as_view(), name="shows.list"),
    path('shows/create/', views.ShowCreate.as_view(), name='shows.create'),
    path('shows/<int:pk>/', views.ShowDetail.as_view(), name='shows.detail'),
    path('shows/<int:pk>/edit/', views.ShowUpdate.as_view(), name='shows.update'),
    path('shows/<int:pk>/delete/', views.ShowDelete.as_view(), name='shows.delete'),
    # Episodes
    path('shows/<int:pk>/episodes/', views.EpisodeList.as_view(), name='episodes.list'),
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGIN_REDIRECT_URL), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
