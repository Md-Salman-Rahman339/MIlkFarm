from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE

# Create your models here.

class UserAccount(models.Model):
    user=models.OneToOneField(User,related_name='account',on_delete=models.CASCADE)
    account_no=models.IntegerField(unique=True)
    gender=models.CharField(max_length=10,choices=GENDER_TYPE)
    phone = models.CharField(max_length=20, help_text='Enter phone number')
    balance=models.DecimalField(default=0,max_digits=12,decimal_places=2)
    
    def __str__(self):
        return str(self.account_no)
    
    
    
class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length= 100)
    country = models.CharField(max_length=100)
    def __str__(self):
        return str(self.user.email)