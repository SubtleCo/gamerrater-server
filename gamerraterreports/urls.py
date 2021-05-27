from django.urls import path
from .views import top_5_games_list

urlpatterns = [
    path('reports/games/top5', top_5_games_list)
]