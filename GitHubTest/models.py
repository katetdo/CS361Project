from django.db import models


class MySyllabus(models.Model):
    courseName = models.CharField(max_length=20, default="")
    assignmentWeight = models.CharField(max_length=20)
    gradeScale = models.CharField(max_length=20)


class MyUser(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    type = models.CharField(max_length=1)  # T=TA  I=Instructor  A=Admin


class PersonalInfo(models.Model):
    lastName = models.CharField(max_length=20)
    firstName = models.CharField(max_length=20)
    officeHours = models.CharField(max_length=20)
    officeNumber = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=20)
    syllabus = models.ForeignKey(MySyllabus, on_delete=models.CASCADE)  # permissions access for T vs I
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.lastName
