from django.urls import path
from .views import top_5_games_list, bottom_5_games_list, games_per_category_list, games_with_6_plus_players

urlpatterns = [
    path('reports/games/top5', top_5_games_list),
    path('reports/games/bottom5', bottom_5_games_list),
    path('reports/categories/count', games_per_category_list),
    path('reports/games/party', games_with_6_plus_players)
]