"""Test for user api"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse("core:register")
REQUEST_COUNT_URL = reverse("core:request-count")
RESET_COUNT_URL = reverse("core:reset-count")

def create_user(**params):
    """create and return new user"""
    return get_user_model().objects.create_user(**params)



class PublicUserApiTestCase(TestCase):
    """Test without token authentication"""

    def setUp(self):
        self.client = APIClient()

    def test_for_create_user(self):
        """test for create user"""
        payload = {
            "username": "testname",
            "password": "testpass123",            
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=payload["username"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)




class PrivateUserApiTest(TestCase):
    """Test Api requests that require authentication"""

    def setUp(self):
        user_details = {
            "username": "testname",
            "password": "testpassword123",
            
        }
        self.user = create_user(**user_details)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
    def test_for_request_count(self):
        """test for request count"""
        res = self.client.get(REQUEST_COUNT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_for_reset_count(self):
        """test for reset count"""
        res = self.client.get(RESET_COUNT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
