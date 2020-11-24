from django.db import models
# Create your models here.


class MyUser(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class PersonalInfo(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class TA(models.Model):
    personInfo = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)



class Instructor(models.Model):
    personInfo = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)