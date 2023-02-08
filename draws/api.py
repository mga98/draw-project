from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Draw
from .serializers import DrawSerializer


@api_view()
def draws_api_list(request):
    draws = Draw.objects.filter(
        is_published=True,
    ).order_by('-id')[:10]

    serializer = DrawSerializer(instance=draws, many=True)

    return Response(serializer.data)


@api_view()
def draws_api_detail(request, pk):
    draw = get_object_or_404(
        Draw,
        is_published=True,
        pk=pk,
    )

    serializer = DrawSerializer(instance=draw, many=False)

    return Response(serializer.data)
