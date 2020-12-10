from django.db import models


class MyUserLogin(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class MyUser(models.Model):
    login = models.ForeignKey(MyUserLogin, on_delete=models.CASCADE)
    type = models.CharField(max_length=1)  # T=TA  I=Instructor  A=Admin
    lastName = models.CharField(max_length=20)
    firstName = models.CharField(max_length=20)
    officeHours = models.CharField(max_length=20)
    officeNumber = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=20)

    def __str__(self):
        return self.lastName + ", " + self.firstName


class MyCourse(models.Model):
    courseName = models.CharField(max_length=20)
    instructor = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class MySection(models.Model):
    sectionNumber = models.IntegerField()
    course = models.ForeignKey(MyCourse, on_delete=models.CASCADE)
    teachingAssistant = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class MySyllabus(models.Model):
    course = models.ForeignKey(MyCourse, on_delete=models.CASCADE)
    courseDescription = models.CharField(max_length=200, default="")
    assignmentWeight = models.CharField(max_length=20)
    gradeScale = models.CharField(max_length=20)
