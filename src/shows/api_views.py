
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
    
    @action(detail=True, methods=['get', 'post'])
    def episodes(self, request, pk=None):
        show = self.get_object()
        if request.method == 'GET':
            episodes = Episode.objects.filter(show=show, deleted_at=None)
            serializer = EpisodeSerializer(episodes, many=True)
            return Response(serializer.data)
        else:
            request.data['show'] = show.id
            serializer = EpisodeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class EpisodeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Episode.objects.filter(deleted_at=None)
    serializer_class = EpisodeSerializer
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope,)
    
    def destroy(self, request, pk=None):
        episode = self.get_object()
        episode.deleted_at = timezone.now()
        episode.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
