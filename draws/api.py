
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Draw
from .serializers import DrawSerializer


class DrawAPIv2List(APIView):
    def get(self, request):
        draws = Draw.objects.filter(
            is_published=True,
        ).order_by('-id')[:10].select_related(
            'author'
        ).prefetch_related('like')

        serializer = DrawSerializer(instance=draws, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = DrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class DrawAPIv2Detail(APIView):
    def get_draw(self, pk):
        draw = get_object_or_404(
            Draw,
            is_published=True,
            pk=pk,
        )

        return draw

    def get(self, request, pk):
        draw = self.get_draw(pk)
        serializer = DrawSerializer(
            instance=draw,
            many=False,
        )

        return Response(serializer.data)

    def patch(self, request, pk):
        draw = self.get_draw(pk)
        serializer = DrawSerializer(
            instance=draw,
            data=request.data,
            many=False,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        draw = self.get_draw(pk)
        draw.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
