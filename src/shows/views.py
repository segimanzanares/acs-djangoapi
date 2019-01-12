
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from shows.models import Show
from shows.serializers import ShowSerializer
from rest_framework import permissions, viewsets, status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.response import Response
import datetime

class ShowViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Show.objects.filter(deleted_at=None)
    serializer_class = ShowSerializer
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope,)
    
    def destroy(self, request, pk=None):
        show = self.get_object()
        show.deleted_at = str(datetime.datetime.utcnow())
        show.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        pass
    
@login_required
@require_http_methods(["GET"])
def shows_index(request):
    shows = Show.objects.filter(deleted_at=None)[:20]
    context = {
        'shows': shows
    }
    return render(request, 'shows/index.html', context)

def logout(request):
    auth_logout(request)
    return redirect(reverse('login'))
