from django.test import TestCase, Client
from .models import MySyllabus, MyUser, MyCourse, MySection, MyUserLogin
from . import views
import unittest


# Create your tests here.
class TestStuffStr(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = MyUser(login=MyUserLogin(username="noman", password="1234"))
        self.user2 = MyUser(login=MyUserLogin(username="Nick", password="5678"))
        self.user3 = MyUser(login=MyUserLogin(username="Santha", password="1234"))

        self.user1.save()
        self.user2.save()
        self.user3.save()

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
        response = client.post('/', {"username": "noman", "password": "1234"})
        self.assertTrue(self.client.login())
        self.assertEqual(response.status_code, 200)

        response = client.post('/', {"username": "Nick", "password": "5678"})
        self.assertTrue(self.client.login())
        self.assertEqual(response.status_code, 200)

        response = client.post('/', {"username": "Santha", "password": "1234"})
        self.assertTrue(self.client.login())
        self.assertEqual(response.status_code, 200)

        # password needs to be a string
        response = client.post('/', {"username": "noman", "password": 1234})
        self.assertFalse(self.client.login())
        self.assertEqual(response.status_code, 200)

        # password needs to match user
        response = client.post('/', {"username": "noman", "password": "5678"})
        self.assertFalse((self.client.login()))
        self.assertEqual(response.status_code, 200)

        response = client.post('/', {"username": "Nick", "password": "1234"})
        self.assertFalse((self.client.login()))
        self.assertEqual(response.status_code, 200)


class TestPersonalInfo(unittest.TestCase):

    def test_officeNumber1(self):
        self.user.officeNumber = "205"
        self.assertTrue(self.user.officeNumber.isnumeric())

    def test_officeNumber2(self):
        self.user.officeNumber = "205"
        self.assertEqual(int(self.user.officeNumber), 205)

    def test_officeNumber3(self):
        self.user.officeNumber = "0"
        self.assertFalse(int(self.user.officeNumber), "officeNumber can't be 0")

    def test_phoneNumber(self):
        self.user.phoneNumber = "4145445978"
        self.assertTrue(self.user.phoneNumber.isnumeric())

    def test_phoneNumber2(self):
        self.user.phoneNumber = "4145445978"
        self.assertEqual(int(self.user.phoneNumber), 4145445978)

    def test_phoneNumber3(self):
        self.user.phoneNumber = "0"
        self.assertFalse(int(self.user.phoneNumber), "Phone numbers can't be 0")

    def test_email(self):
        self.user.email = "dakito@uwm.edu"
        self.assertTrue(self.user.email.find("@uwm.edu") > 0)

    def test_email2(self):
        self.user.email = "dakito@uwm.edu23"
        x = self.user.email.split(7, 16)
        self.assertNotEqual(x, "@uwm.edu", "There can not be characters after @uwm.edu")

    def test_email3(self):
        self.user.email = "@uwm.edu"
        self.assertFalse(self.user.email.index("@") == 0, "There has to be characters before the @ symbol")

    def test_email4(self):
        self.user.email = "34@45@uwm.edu"
        x = self.user.email.find("@")
        y = self.user.email.split(x, 13)
        z = y.find("@")
        self.assertEqual(z, -1, "There cannot be multiple @ in an email")


class TestSyllabus(unittest.TestCase):
    def test_syllabus_course(self):
        syllabus1 = MySyllabus(course="CS361", instructor="John")

        self.assertNotEquals(syllabus1.course, (MySyllabus(course="CS361")), "Can't have duplicate class syllabi")
        self.assertEquals(syllabus1.course, (MySyllabus(instructor="John")), "Instructors can teach multiple classes")


class TestSections(unittest.TestCase):
    def test_sections(self):
        syllabus1 = MySection(sectionNumber=802, course="CS361")

        self.assertNotEquals(syllabus1.sectionNumber, (MySection(sectionNumber=802)), "Can't have duplicate sections")
        self.assertEquals(syllabus1.course, (MySection(course="CS361")), "Can have multiple sections")


suite = unittest.TestSuite()
suite.addTests(TestStuffStr(), TestPersonalInfo(), TestSyllabus(), TestSections())
