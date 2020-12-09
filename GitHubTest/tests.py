from django.test import TestCase, Client
from .models import MySyllabus, MyUser
import unittest


# Create your tests here.
class StuffStrTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.testuser1 = MyUser(name="noman", password="1234", type="T")
        self.testuser2 = MyUser(name="Nick", password="5678", type="I")
        self.testuser3 = MyUser(name="Santha", password="1234", type="A")
        self.testuser1.save()
        self.testuser2.save()
        self.testuser3.save()

    def test_Session(self):
        client = Client()
        response = client.get('/TA/')
        self.assertEqual(response.status_code, 200)

    def test_something(self):
        session = self.client.session
        session['name'] = 'noman'
        session.save()
        response = self.client.get('/TA/')
        self.assertEqual(list(response.context["TA"]), list(map(str, list(MyUser.objects.filter(user=self.testuser1)))))

    def test_login(self):
        client = Client()

        # verify that a user can log in
        response = client.post('/', {"name": "noman", "password": "1234", "type": "T"})
        self.assertTrue(self.client.login())
        self.assertEqual(response.status_code, 200)

        response = client.post('/', {"name": "Nick", "password": "5678", "type": "I"})
        self.assertTrue(self.client.login())
        self.assertEqual(response.status_code, 200)

        response = client.post('/', {"name": "Santha", "password": "1234", "type": "A"})
        self.assertTrue(self.client.login())
        self.assertEqual(response.status_code, 200)

        # type of Instructor/Ta flag must be capitalized
        response = client.post('/', {"name": "noman", "password": "1234", "type": "t"})
        self.assertFalse(self.client.login())
        self.assertEqual(response.status_code, 200)

        response = client.post('/', {"name": "noman", "password": "1234", "type": "i"})
        self.assertFalse(self.client.login())
        self.assertEqual(response.status_code, 200)

        # password needs to be a string
        response = client.post('/', {"name": "noman", "password": 1234, "type": "T"})
        self.assertFalse(self.client.login())
        self.assertEqual(response.status_code, 200)

        # password needs to match user
        response = client.post('/', {"name": "noman", "password": "5678", "type": "T"})
        self.assertFalse((self.client.login()))
        self.assertEqual(response.status_code, 200)

        response = client.post('/', {"name": "Nick", "password": "1234", "type": "I"})
        self.assertFalse((self.client.login()))
        self.assertEqual(response.status_code, 200)

        # Instruction Type must match user records
        response = client.post('/', {"name": "noman", "password": "1234", "type": "I"})
        self.assertFalse((self.client.login()))
        self.assertEqual(response.status_code, 200)

        response = client.post('/', {"name": "Nick", "password": "5678", "type": "T"})
        self.assertFalse((self.client.login()))
        self.assertEqual(response.status_code, 200)


class TestPersonalInfo(unittest.TestCase):
    def set_up_personal_info(self):
        self.client = Client()
        self.user = MyUser(name="Santha", password="1234", type="A")
        self.user.save()

    def test_max_length(self):
        # overTwentyChars = "012345678901234567890"
        self.user.lastName = "Do"
        self.user.firstName = "Kate"
        self.user.officeHours = "12:00 - 1:00"
        self.user.officeNumber = "205"
        self.user.email = "katetdo@uwm.edu"
        self.user.phoneNumber = "262-716-5272"


def suit():
    suite = unittest.TestSuite()
    suite.addTests(StuffStrTest(), TestPersonalInfo())
