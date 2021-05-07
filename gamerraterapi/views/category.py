### View module for handling requests about category

from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gamerraterapi.models import Category

class CategoryViewSet(ViewSet):

    def list(self, request):
        categories = Category.objects.all()

        serializer = CategorySerializer(
            categories, many=True, context={'request': request}
        )
        return Response(serializer.data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')

