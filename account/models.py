from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.conf import settings

# Create your models here.

class Account(models.Model):
    
    user = models.OneToOneField(User,related_name="accounts", on_delete=models.CASCADE)
    phone_number = models.IntegerField(blank=True,null=True)
    present_address = models.CharField(max_length=300,blank=True,null=True)
    counter = models.IntegerField(default=0,blank=False)
    isVerified = models.BooleanField(blank=False,default=False)
    
    
    
    


    def __str__(self):
        return self.user.username
    



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


#token create import from rest framework Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.account.save()