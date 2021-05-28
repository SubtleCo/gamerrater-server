import sqlite3
from django.shortcuts import render
from gamerraterapi.models import Game, Category
from gamerraterreports.views import Connection

def games_per_category_list(request):
    """ Function to build a list of games, limit top 5"""
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    c.id,
                    c.label,
                    COUNT(g.title) count
                FROM
                    gamerraterapi_category c
                JOIN
                    gamerraterapi_game_categories gc ON gc.category_id = c.id
                JOIN
                    gamerraterapi_game g ON g.id = gc.game_id
                GROUP BY
                    c.id
                ORDER BY
                    count DESC
            """)

            dataset = db_cursor.fetchall()

            categories_with_game_count = {}

            for row in dataset:
                category = Category()
                category.label = row["label"]
                category.count = row["count"]
                category.id = row["id"]

                categories_with_game_count[category.id] = category

        categories_with_game_count_list = list(categories_with_game_count.values())

        def by_count(category):
            return category.count

        categories_with_game_count_list.sort(key=by_count, reverse=True)

        template = 'games/category_game_count.html'
        context = {
            'categories_with_game_count_list': categories_with_game_count_list
        }

        return render(request, template, context)


