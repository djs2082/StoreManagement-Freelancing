from django.db import models
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
import datetime

class Customer(models.Model):
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed.")
	fname=models.CharField(max_length=50,null=True,blank=False)
	lname=models.CharField(max_length=50,null=True,blank=False)
	mobile=models.CharField(validators=[phone_regex],max_length=10,null=True,blank=False,unique=True)
	birth_day=models.DateField(null=True,blank=True)
	date=models.DateField(default=datetime.date.today(),null=True,blank=True)
	def __str__(self):
	    return self.fname+" "+self.lname+" : "+self.mobile