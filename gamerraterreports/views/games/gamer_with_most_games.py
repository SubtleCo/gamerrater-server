"""Module for generating the gamer with the most games"""
import sqlite3
from django.shortcuts import render
from gamerraterapi.models import Game
from gamerraterreports.views import Connection


def gamer_with_most_games(request):
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT MAX(game_count), name
                FROM (
                    SELECT
                        first_name || ' ' || last_name name,
                        COUNT(title) game_count
                    FROM
                        auth_user u
                    JOIN
                        gamerraterapi_game g ON g.user_id = u.id
                    GROUP BY name
                )

                    
            """)

            data = db_cursor.fetchone()

            user_with_most_games = data["name"]

        template = "games/gamer_with_most_games.html"
        context = {
            'most_addicted_gamer': user_with_most_games
        }

        return render(request, template, context)
