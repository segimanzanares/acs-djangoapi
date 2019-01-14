
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from shows.models import Show

@login_required
@require_http_methods(["GET"])
def shows_index(request):
    shows = Show.objects.filter(deleted_at=None)[:20]
    context = {
        'shows': shows
    }
    return render(request, 'shows/index.html', context)