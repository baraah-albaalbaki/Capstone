import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie



class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        # self.database_path = "postgresql://postgres:12postgres34@localhost:5432/castingagency"
        
        self.director_token = os.environ['DIRECTOR_TOKEN']
        self.assistant_token = os.environ['ASSISTANT_TOKEN']

        # self.director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjdRU1k3RTdGUmNjNlBnNXBNalNLMSJ9.eyJpc3MiOiJodHRwczovL2thaHZlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGExM2UzYWEwYjBiYjAwNmFkOWI4MzMiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjI0MTQxODM3LCJleHAiOjE2MjQxNzc4MzcsImF6cCI6IjhLbDVWdE5OTlNEVmxTOWdJR3lCb2VDekc1eklpblhNIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicG9zdDphY3RvciJdfQ.ZZuw0zUxBLSTqv6YQuHygzK5rsGMuxtuhH4EScxdlsrI2roVoOPh-JSO65bq7vUq45KrdqdR5BNzI8CIQWztYhST7WKgPoruXVNxN-jSNXQQtO1O3OU62MYG8j7ZNOLMCiOjjMxQYqsZBn8rc0xZyr-P-GdZD6qGXhE3pCQDwKybHUnw4Ye3ZulLfrqO7mh-a4YSXBysACIDQ7LJiBzxhZ3L_6ZvAw_XqDluHcO59cEVIZUeigQcXKUdKWidUA8rP_L_F2QR0g5qes_cDIm5l1855rVY0eBhPF7p4zEzcMv97-MYsC8aT8ev1VqG9lQeLulYGCdKdU4sQIduiDAnJQ'
        # self.assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjdRU1k3RTdGUmNjNlBnNXBNalNLMSJ9.eyJpc3MiOiJodHRwczovL2thaHZlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGE0NzJiZmEwYjBiYjAwNmFkYTI4MGQiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjI0MTQzNzYyLCJleHAiOjE2MjQxNzk3NjIsImF6cCI6IjhLbDVWdE5OTlNEVmxTOWdJR3lCb2VDekc1eklpblhNIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6W119.DlY6RAKVN55cm9-BlFyvEIndgCXaXi-mMWQ2_ebwoouuJiII0PN0GrrpXSoUDlffI_CI-Rea6WZmC8sTkeej2TizxYrQTPQMRi--DScjoWB9o1_-l4bfrhiErdrmH3DkdMekyH33OVMimLARm6MWnhSWouCqyzSiwpUOYRLxW1w3TAk2elbN0tYigglrPZ5fC__tb6ZUpgeumjXAF8soHldCHWTnD56KXts9vzA5bvraFDbUwK5utBUWR_emkXjh7VIGsDj4cfFuYGUbkfl8hWc032Rs_nFct8HpMbFWpYIMUGqE_Q2cUuN8A4cHqb46dqrBUGUmED61nDmSWSuSGA'
        self.try_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjdRU1k3RTdGUmNjNlBnNXBNalNLMSJ9'
        
        self.header_director = {"Authorization": "Bearer {}".format(self.director_token)}
        self.header_assistant = {"Authorization": "Bearer {}".format(self.assistant_token)}
        self.header_try = {"Authorization": "Bearer {}".format(self.try_token)}
        
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = {
            'name': 'smith',
            'age':'32',      
            'gender': 'male', 
        }
        self.new_actor_missing = {
            'name': '',
            'age':'43',      
            'gender': 'male', 
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    # def test_get_movies(self):
    #     # res = self.client().get('/movies', headers = self.header_director)
    #     res = self.client().get('/movies')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)



    def test_get_actor(self):
        res = self.client().get('/actors/1', headers = self.header_director)
        # res = self.client().get('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_404_get_actor(self):
        res = self.client().get('/actors/99', headers = self.header_director)
        # res = self.client().get('/actors/8')
        self.assertEqual(res.status_code, 404) 



    def test_post_actor(self):
        res = self.client().post('/actors', headers=self.header_director, json=self.new_actor)
        # res = self.client().post('/actors', json = self.new_actor)
        self.assertEqual(res.status_code, 200)

    def test_422_post_if_data_missing(self):
        res = self.client().post('/actors', headers = self.header_director, json=self.new_actor_missing)    
        # res = self.client().post('/actors', json = self.new_actor_missing)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)



    def test_get_actors(self):
        res = self.client().get('/actors', headers = self.header_director)
        # res = self.client().get('/actors')
        self.assertEqual(res.status_code, 200)
    
    # def test_404_get_actors(self):
    #     # res = self.client().get('/actors', headers = self.header_director)
    #     res = self.client().get('/actors')
    #     self.assertEqual(res.status_code, 404)


    def test_patch_actor(self):
        res = self.client().patch('/actors/1', headers = self.header_director, json=self.new_actor)
        # res = self.client().patch('/actors/1', json = self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_404_patch_actor(self):
        res = self.client().patch('/actors/45', headers = self.header_director, json=self.new_actor)
        # res = self.client().patch('/actors/45', json = self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)



    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers = self.header_director)
        # res = self.client().delete('/actors/1')
        self.assertEqual(res.status_code, 200)

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/5999', headers = self.header_director)
        # res = self.client().delete('/actors/5999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
    
    

    def test_401_unauthorized(self):
        res = self.client().get('/actors', headers = self.header_try)
        self.assertEqual(res.status_code, 401)
    
    def test_403_forbidden(self):
        res = self.client().post('/actors', headers = self.header_assistant, json = self.new_actor)
        self.assertEqual(res.status_code, 403)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()