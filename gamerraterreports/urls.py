from django.urls import path
from .views import top_5_games_list, bottom_5_games_list, games_per_category_list

urlpatterns = [
    path('reports/games/top5', top_5_games_list),
    path('reports/games/bottom5', bottom_5_games_list),
    path('reports/categories/count', games_per_category_list)
]