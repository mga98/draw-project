from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Draw
from .serializers import DrawSerializer


@api_view(http_method_names=['get', 'post'])
def draws_api_list(request):
    if request.method == 'GET':
        draws = Draw.objects.filter(
            is_published=True,
        ).order_by('-id')[:10].select_related(
            'author'
        ).prefetch_related('like')

        serializer = DrawSerializer(instance=draws, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


@api_view()
def draws_api_detail(request, pk):
    draw = get_object_or_404(
        Draw,
        is_published=True,
        pk=pk,
    )

    serializer = DrawSerializer(instance=draw, many=False)

    return Response(serializer.data)
