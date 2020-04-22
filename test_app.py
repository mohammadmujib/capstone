import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie, db
from dotenv import load_dotenv

load_dotenv()

test_database_path = 'postgresql://postgres:1234@localhost:5432/castings_test'

bearer_tokens = {
    "casting_assistant": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhY2NmZGU0MzFhMGM4ZDY3MGNkMiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODc1MDk3MzQsImV4cCI6MTU4NzUxNjkzNCwiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.kGIXN_koE9fJcDxfNmBkmXO5LgKka2FRbJ-z2adTfK5p_LIoIF5Rd6sFsVNXnoVGHNywmXk51pGj0eewSBpfe7pAAK9F5eZhktUd2KT8nhppkeJ06wohOlnndGuqnSGOOXXyGlU5aVcae1oN7CyxMFH1RUHVmEjDm7QtC3tqOWO_Fh2kUWPwI62rR8N7hWepUhI_RIqwaUOJH2kzzX90Rlg06jhhtAGC9rtgbNgkvXu6UpNZ1Tk9KuHXQwxMIlQeOQRKDI6So7kfONGTNpDKAf6AV9q7y-_WHyvCKyG1VIVNILSfpesYhiK36FWMhTfvsimHVl0IwjyCST-IVjbD1A",
    "executive_producer": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhZDRhNjNmODAwMGM4YzIzNmJkZCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODc1MDg3NTYsImV4cCI6MTU4NzUxNTk1NiwiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.jfPiPx68QB3yVNqniVnDRcGrLNCMbrFmG1Uddu0ySAdRFA2R2z9UT2V2UCfrNmUxHjiBiBn3uz7DCiY4yHRhM1GY7w3wEivesWXe0kuq3VMqb3C2y6AZ7PVCWpJjyPVzaNS-_VmmpRDIB4O0ObRkCOJ2WloGxF5zTtS6gs7m3hK-TpjqOoqjhAdim3Xu_MoIGVSwNqItlqdIlHy3jPbziVjlJiP5-8mdTBg4Vg7gZMDVETMym6o_JQtztUchVFln3EzsObFwH2x_GDpAIgxwWnSDliIF4PGNg98Fy7ZqIaooutWDpmALMetDEDx1yEN3BZtTFaa7TLDe3dIBVBmz2A",
    "casting_director": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhY2ZlZGU0MzFhMGM4ZDY3MGQyYiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODc1MTAyMTUsImV4cCI6MTU4NzUxNzQxNSwiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.im7Lcft_HSzV1OR5IwKaWM0lhWID3zkH99k_DzyBBBStgXS2ydnTl1oeeVO1OecyNpYHdYpXI8-5q-1IGLYHCfiVR1gg_-5IWN6cZ2tmaLMtK3YE4avX7EqE-T-MxWtvdv-4uJaqAsYUP5Iw9DgEZ-sl_pRXLzPWFi0GbFTwfxAR0GQSMYH7oOunkXRQtnPvI8bgiwkdFYY4dEpo5OjOrhdUUEEK-ibwzS6GnYesdIOUUm36x_jws5rvvQ6WyZNFFVmWpax6zix_SLgzZvaNS3e_Nv_ku_NpTBXgCd9LWDHxp4pUP8w7jtNIpyr6akENovQmxIOnIDw9ZuzjruoV0Q"
}

casting_assistant_auth_header = {
    'Authorization': bearer_tokens['casting_assistant']
}

casting_director_auth_header = {
    'Authorization': bearer_tokens['casting_director']
}

executive_producer_auth_header = {
    'Authorization': bearer_tokens['executive_producer']
}

class CastingAgencyTestCase(unittest.TestCase):

    def insert_data(self):
        """Seed test database with initial data"""
        actor1 = Actor(name="NIck JOnas", age=25, gender='m')
        actor2 = Actor(name="rock", age=22, gender='f')
        actor3 = Actor(name="Salman", age=32, gender='f')

        movie1 = Movie(title="Joker", release_date="02/01/2000")
        movie2 = Movie(title="Titanic", release_date="05/07/2015")
        movie3 = Movie(title="abcd", release_date="09/11/2029")

        self.db.session.add(actor1)
        self.db.session.add(actor2)
        self.db.session.add(actor3)

        self.db.session.add(movie1)
        self.db.session.add(movie2)
        self.db.session.add(movie3)
        self.db.session.commit()
        self.db.session.close()

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        
        setup_db(self.app, database_path=test_database_path)
        with self.app.app_context():
            self.db = db

            self.db.drop_all()
            self.db.create_all()

            self.insert_data()

    def tearDown(self):
        """Runs cleanup after each test"""
        self.db.session.rollback()
        self.db.drop_all()
        self.db.session.close()
        pass
    
#----------------------------------------------------------------------------#
# Tests for /actors POST
#----------------------------------------------------------------------------#

    def test_create_new_actor(self):
        """Test POST new actor."""

        json_create_actor = {
            "name": "Crisso",
            "gender": "m",
            "age": 25
        }

        res = self.client().post('/actors', json=json_create_actor,
                                 headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_error_401_new_actor(self):
        """Test POST new actor w/o Authorization."""

        json_create_actor = {
            'name': 'Crisso',
            'age': 25
        }

        res = self.client().post('/actors', json=json_create_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

#----------------------------------------------------------------------------#
# Tests for /actors GET
#----------------------------------------------------------------------------#
    def test_get_all_actors(self):
        """Test GET all actors."""
        res = self.client().get('/actors', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_error_401_get_all_actors(self):

        """Test GET all actors w/o Authorization."""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

#----------------------------------------------------------------------------#
# Tests for /actors PATCH
#----------------------------------------------------------------------------#
    def test_edit_actor(self):
        """Test PATCH existing actors"""
        json_edit_actor_with_new_age = {
            'age': 30
        }
        res = self.client().patch('/actors/2', json=json_edit_actor_with_new_age,
                                  headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_error_404_edit_actor(self):
        """Test PATCH with non json body"""

        res = self.client().patch('/actors/123412', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
#----------------------------------------------------------------------------#
# Tests for /actors DELETE
#----------------------------------------------------------------------------#

    def test_error_401_delete_actor(self):
        """Test DELETE existing actor w/o Authorization"""
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_403_delete_actor(self):
        """Test DELETE existing actor with missing permissions"""
        res = self.client().delete('/actors/1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_actor(self):
        """Test DELETE existing actor"""
        res = self.client().delete('/actors/1', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_error_404_delete_actor(self):
        """Test DELETE non existing actor"""
        res = self.client().delete('/actors/15125', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
#----------------------------------------------------------------------------#
# Tests for /movies POST
#----------------------------------------------------------------------------#

    def test_create_new_movie(self):
        """Test POST new movie."""

        json_create_movie = {
            'title': 'Crisso Movie',
            'release_date': "02/07/2020"
        }

        res = self.client().post('/movies', json=json_create_movie,
                                 headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_error_401_create_new_movie(self):
        """Test Error POST new movie."""

        json_create_movie_without_name = {
            'release_date': "02/07/2020"
        }

        res = self.client().post('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
#----------------------------------------------------------------------------#
# Tests for /movies GET
#----------------------------------------------------------------------------#

    def test_get_all_movies(self):
        """Test GET all movies."""
        res = self.client().get('/movies', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_error_401_get_all_movies(self):
        """Test GET all movies w/o Authorization."""
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

#----------------------------------------------------------------------------#
# Tests for /movies PATCH
#----------------------------------------------------------------------------#

    def test_edit_movie(self):
        """Test PATCH existing movies"""
        json_edit_movie = {
            "title":"fast and furious"
        }
        res = self.client().patch('/movies/1', json=json_edit_movie,
                                  headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_error_404_edit_movie(self):
        """Test PATCH with non valid id json body"""
        res = self.client().patch('/movies/1', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_error_404_edit_movie(self):
        """Test PATCH with non valid id"""
        json_edit_movie = {
            'release_date': "02/03/2020"
        }
        res = self.client().patch('/movies/123412', json=json_edit_movie,
                                  headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /movies DELETE
#----------------------------------------------------------------------------#

    def test_error_401_delete_movie(self):
        """Test DELETE existing movie w/o Authorization"""
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_403_delete_movie(self):
        """Test DELETE existing movie with wrong permissions"""
        res = self.client().delete('/movies/1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_movie(self):
        """Test DELETE existing movie"""
        res = self.client().delete('/movies/1', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_error_404_delete_movie(self):
        """Test DELETE non existing movie"""
        res = self.client().delete('/movies/151251', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

if __name__ == "__main__":
    unittest.main()
    
