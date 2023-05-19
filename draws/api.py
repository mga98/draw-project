from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Draw
from .serializers import DrawSerializer
from .permissions import IsOwner


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
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )

        self.check_object_permissions(self.request, obj)

        return obj

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(), ]

        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        draw = self.get_object()
        serializer = DrawSerializer(
            instance=draw,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
        )

        return super().partial_update(request, *args, **kwargs)
