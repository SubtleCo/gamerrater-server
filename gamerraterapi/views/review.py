### View module for handling requests about reviews
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from gamerraterapi.models import Game, Review
from django.utils import timezone

class ReviewViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        reviews = Review.objects.all()

        game = self.request.query_params.get('game_id', None)
        if game is not None:
            reviews = reviews.filter(game=game)
        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def create(self, request):
        req = request.data
        review = Review()

        review.user = User.objects.get(pk=request.auth.user.id)
        review.game = Game.objects.get(pk=req['game_id'])
        review.text = req['text']
        review.timestamp = timezone.now()

        try:
            review.save()
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)


################################  SERIALIZERS  ################################

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'game', 'text', 'timestamp')
        depth = 1




