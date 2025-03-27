from django.db import models

# Create your models here.
class Login(models.Model):
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    user_type=models.CharField(max_length=10)

class User(models.Model):
    name=models.CharField(max_length=100)
    contact_no=models.CharField(max_length=10)
    gender=models.CharField(max_length=10)
    login=models.ForeignKey(Login,on_delete=models.CASCADE)

class Bussines(models.Model):
    bussines_name=models.CharField(max_length=100)
    bussines_category=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    contact_no=models.CharField(max_length=10)
    status=models.IntegerField(default=0)
    login=models.ForeignKey(Login,on_delete=models.CASCADE)

class Survey(models.Model):
    question=models.CharField(max_length=500)
    option1=models.CharField(max_length=100)
    option2=models.CharField(max_length=100)
    option3=models.CharField(max_length=100,null=True,blank=True)
    option4=models.CharField(max_length=100,null=True,blank=True)
    login=models.ForeignKey(Login,on_delete=models.CASCADE)
    
class UserSurvey(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    survey=models.ForeignKey(Survey,on_delete=models.CASCADE)
    option=models.CharField(max_length=100)