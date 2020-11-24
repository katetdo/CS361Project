from django.db import models


class MyUser(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    type = models.CharField(max_length=1)


class MySyllabus(models.Model):
        assignmentWeight = models.CharField(max_length=20)
        gradeScale = models.CharField(max_length=20)
        user = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class PersonalInfo(models.Model):
    lastName = models.CharField(max_length=20)
    firstName = models.CharField(max_length=20)
    officeHours = models.CharField(max_length=20)
    officeNumber = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=20)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
