from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from movies.models import Collections, Movies
from movies.tests.test_models import create_movie
from rest_framework_simplejwt.tokens import RefreshToken


class CollectionsAPITestCase(APITestCase):
    def setUp(self):
        self.userdata = {
        "username": "testname",
        "password": "testpass123",
        }
        self.user = get_user_model().objects.create_user(**self.userdata)
        self.client = APIClient()

        self.movie1data = {
            "title": "Movie1",
            "description":"movie description",
            "genres":"Action",
            "uuid":"3fa85f64-5717-4562-b3fc-2c963f66afa6"            
        }
        self.movie2data = {
            "title": "Movie2",
            "description":"movie description",
            "genres":"Action",
            "uuid":"3fa85f64-5717-4562-b3fc-2c963f66afa2"            
        }
        self.movie3data = {
            "title": "Movie3",
            "description":"movie description",
            "genres":"Drama",
            "uuid":"3fa85f64-5717-4562-b3fc-2c963f66afa3"            
        }
        self.movie4data = {
            "title": "Movie4",
            "description":"movie description",
            "genres":"Fantasy",
            "uuid":"3fa85f64-5717-4562-b3fc-2c963f66afa4"            
        }
        self.movie5data = {
            "title": "Movie5",
            "description":"movie description",
            "genres":"Adventure",
            "uuid":"3fa85f64-5717-4562-b3fc-2c963f66afa5"            
        }
        
        self.movie1 = create_movie(**self.movie1data)
        self.movie2 = create_movie(**self.movie2data)
        self.movie3 = create_movie(**self.movie3data)
        self.movie4 = create_movie(**self.movie4data)
        self.movie5 = create_movie(**self.movie5data)
        
        
        
        self.collection = Collections.objects.create(
            title='Test Collection',
            description='Test Description',
            user=self.user
        )
        self.collection.movies.set([self.movie1, self.movie2, self.movie3, self.movie4, self.movie5])
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
    
    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        
    def test_list_collections(self):
        self.authenticate()
        response = self.client.get(reverse('collections-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)  # PAGE_SIZE = 2
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(response.data['results'][0]['title'], self.collection.title)

    def test_create_collection(self):
        self.authenticate()
        data = {
        "title": "string",
        "description": "string",
        "movies": [
            {
            "title": "string",
            "description": "string",
            "genres": "string",
            "uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            }
        ]
        }
        response = self.client.post(reverse('collections-list'), data, format='json')
                
        self.assertEqual(response.status_code, 201)
        
    def test_update_collection_authenticated(self):
        self.authenticate()
        
        data = {
        "title": "string",
        "description": "string",
        "movies": [
            {
            "title": "string",
            "description": "string",
            "genres": "string",
            "uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            }
        ]
        }
        response = self.client.put(reverse('collections-detail', kwargs={'pk': self.collection.id}), data, format='json')
        self.assertEqual(response.status_code, 200)
        
    def test_delete_collection(self):
        self.authenticate()
        response = self.client.delete(reverse('collections-detail', kwargs={'pk': self.collection.id}))
        self.assertEqual(response.status_code, 204)