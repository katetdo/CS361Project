from django.test import TestCase, Client
from .models import MySyllabus, MyUser, PersonalInfo
import unittest
# Create your tests here.
class StuffStrTest(TestCase):

    def setUp(self):
        self.clint = Client()
        self.testuser1 = MyUser(name= "noman", password= "1234",  type="T")
        self.testuser2 = MyUser(name="Nick", password="1234", type="I")
        self.testuser3 = MyUser(name="Jason", password="1234", type="T")
        self.testuser1.save()
        self.testuser2.save()
        self.testuser3.save()


    def test_Session(self):
        client = Client()
        response = client.get('/things/')
        self.assertEqual(response.status_code, 200)

    def test_something(self):
        session = self.client.session
        session['name'] = 'noman'
        session.save()
        response = self.client.get('/things/')
        self.assertEqual(list(response.context["things"]), list(map(str, list(Stuff.objects.filter(user=self.testuser1)))))

    def test_post(self):
        client = Client()
        response = client.post('/', {"name": "noman","passward" : 1234})
        self.assertTrue((self.clint.login() == False))
        self.assertEqual(response.status_code, 200)
