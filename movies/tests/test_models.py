from django.test import TestCase
from django.contrib.auth import get_user_model
from movies.models import Movies, Collections


def create_movie(**params):
    """create and return new movie"""
    return Movies.objects.create(**params)

class CollectionModelTest(TestCase):
    """Test for collection model"""

    def setUp(self) -> None:
        """Set up the test"""
        self.userdata = {
        "username": "testname",
        "password": "testpass123",
        }
        self.user = get_user_model().objects.create_user(**self.userdata)
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
        
        
    def test_favourite_genres(self):
        expected_genres = ['Action','Fantasy', 'Drama']
        self.assertListEqual(list(self.collection.favourite_genres), expected_genres)
        
