
from shows.models import Show, Episode
from shows.serializers import ShowSerializer, EpisodeSerializer
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from django.utils import timezone

class ShowViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Show.objects.filter(deleted_at=None)
    serializer_class = ShowSerializer
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope,)
    
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        include = request.GET.get('include', '')
        if include != '':
            include = include.split(',')
            if 'episodes' in include:
                instance.episodes = Episode.objects.filter(show=instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        show = self.get_object()
        show.deleted_at = timezone.now()
        show.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        pass
    
    @action(detail=True, methods=['get'])
    def episodes(self, request, pk=None):
        show = self.get_object()
        episodes = Episode.objects.filter(show=show)
        serializer = EpisodeSerializer(episodes, many=True)
        return Response(serializer.data)
