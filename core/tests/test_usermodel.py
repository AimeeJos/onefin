from django.test import TestCase
from django.contrib.auth import get_user_model


class UserListCreateTest(TestCase):
    """Test models"""
    
    def test_for_create_user(self):
        self.userdata = {
        "username": "testname",
        "password": "testpass123",
        }
        user = get_user_model().objects.create_user(**self.userdata)
        self.assertEqual(user.username, self.userdata['username'])
        self.assertTrue(user.check_password(self.userdata['password']))
        
    def test_for_create_superuser(self):
        self.userdata = {
        "username": "testname",
        "password": "testpass123",
        }
        user = get_user_model().objects.create_superuser(**self.userdata)
        self.assertEqual(user.username, self.userdata['username'])
        self.assertTrue(user.check_password(self.userdata['password']))
        
    