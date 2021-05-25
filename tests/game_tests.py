from gamerraterapi.models.category import Category
import json
from rest_framework import status
from rest_framework.test import APITestCase
from gamerraterapi.models import Game, Rating

class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new user, game
        """
        ################################  Dummy User  ################################

        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        # Initiate request, capture resposne
        response = self.client.post(url, data, format='json')

        # Parse JSON in response 
        json_response = json.loads(response.content)

        # Store token
        self.token = json_response["token"]

        # Assert user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        ################################  Dummy Category  ################################

        category = Category()
        category.label = "thing"
        category.save()

        ################################  Dummy Game  ################################

        url = "/games"
        data = {
            "title": "stuff",
            "released": 2001,
            "description": "A cool game",
            "player_min": 2,
            "player_max": 4,
            "age_min": 8,
            "designer": "Jim Jarmoosh",
            "user": 1,
            "categories": [1]
        }

        # Authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request, sore response
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ################################  Dummy Rating  ################################

        url = "/ratings"
        data = {
            "user": 1,
            "game_id": 1,
            "score": 9
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        

    def test_create_game(self):
        """
        Ensure we can create a new game
        """

        # Parameters
        url = "/games"
        data = {
            "title": "things",
            "released": 2021,
            "description": "A cool game for fine folks",
            "player_min": 2,
            "player_max": 4,
            "age_min": 8,
            "designer": "Jim Jarmoosh",
            "user": 1,
            "categories": [1]
        }

        # Authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request, sore response
        response = self.client.post(url, data, format='json')

        # Parse JSON in response body
        json_response = json.loads(response.content)

        # Assert game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Properties check
        self.assertEqual(json_response["title"], "things")
        self.assertEqual(json_response["released"], 2021)
        self.assertEqual(json_response["description"], "A cool game for fine folks")
        self.assertEqual(json_response["player_min"], 2)
        self.assertEqual(json_response["player_max"], 4)
        self.assertEqual(json_response["age_min"], 8)
        self.assertEqual(json_response["designer"], "Jim Jarmoosh")
        self.assertEqual(json_response["user"]["id"], 1)
        self.assertEqual(json_response["categories"][0]["id"], 1)

    def test_rating_a_game(self):
        """
        Ensure we can rate a game
        """

        url = "/ratings"
        data = {
            "user": 1,
            "game_id": 1,
            "score": 9
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["user"]["id"], 1)
        self.assertEqual(json_response["game"]["id"], 1)
        self.assertEqual(json_response["score"], 9)


    def test_updating_a_game(self):
        """
        Make sure we can update a game
        """

        url = "/games/1"
        data = {
            "title": "zzz",
            "released": 2022,
            "description": "look ma no hands",
            "player_min": 4,
            "player_max": 8,
            "age_min": 10,
            "designer": "Jim Jarmoosh 2",
            "user": 1,
            "categories": [1]
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleting_a_game(self):
        """
        Make sure we can delete a game
        """

        url = "/games/1"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_a_single_game(self):
        """
        Make sure we can get a single game
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get("/games/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_res = json.loads(response.content)
       
        self.assertEqual(json_res["title"], "stuff")
        self.assertEqual(json_res["released"], 2001)
        self.assertEqual(json_res["description"], "A cool game")
        self.assertEqual(json_res["player_min"], 2)
        self.assertEqual(json_res["player_max"], 4)
        self.assertEqual(json_res["age_min"], 8)
        self.assertEqual(json_res["designer"], "Jim Jarmoosh")
        self.assertEqual(json_res["user"]["id"], 1)
        self.assertEqual(json_res["categories"][0]["id"], 1)


    def test_get_all_games(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get("/games")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_res = json.loads(response.content)
        # Check to see that the array has something in it
        self.assertEqual(len(json_res), 1)
        # Check to see that the first object's title is right
        self.assertEqual(json_res[0]["title"], "stuff")

    def test_post_a_review(self):
        url = "/reviews"
        data = {
            "user_id": 1,
            "game_id": 1,
            "text": "this is a game",
            "timestamp": "2021-02-02"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        json_response = json.loads(response.content)
        self.assertEqual(json_response["user"]["id"], 1)
        self.assertEqual(json_response["game"]["id"], 1)
        self.assertEqual(json_response["text"], "this is a game")

    def test_change_a_rating(self):

        url = "/ratings/1"
        data = {
            "user": 1,
            "game_id": 1,
            "score": 8
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_res = json.loads(response.content)
        self.assertEqual(json_res["score"], 8)

        
