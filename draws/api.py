from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .models import Draw
from .serializers import DrawSerializer


class DrawAPIv2Pagination(PageNumberPagination):
    """
    Set the number of draws that are showed in a page
    """
    page_size = 10


class DrawAPIv2ViewSet(ModelViewSet):
    queryset = Draw.objects.filter(
        is_published=True
    ).order_by('-id').select_related(
        'author'
    ).prefetch_related('like')
    serializer_class = DrawSerializer
    pagination_class = DrawAPIv2Pagination
