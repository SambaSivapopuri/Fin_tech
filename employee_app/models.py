from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phoneNo = models.CharField(max_length=15)


class Address(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    hno = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

class WorkExperience(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    companyName = models.CharField(max_length=255)
    fromDate = models.DateField()
    toDate = models.DateField()
    address = models.CharField(max_length=255)

class Qualification(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    qualificationName = models.CharField(max_length=255)
    percentage = models.FloatField()

class Project(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
class Photo(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    img= models.ImageField(upload_to='employee/',blank=True,null=True) 

