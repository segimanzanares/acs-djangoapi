
from shows.models import Show
from shows.serializers import ShowSerializer
from rest_framework import viewsets, status
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
    
    def destroy(self, request, pk=None):
        show = self.get_object()
        show.deleted_at = str(datetime.datetime.utcnow())
        show.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        pass