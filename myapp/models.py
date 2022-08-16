from distutils.command.upload import upload
import imp
from pickle import TRUE
from statistics import mode
from tkinter import CASCADE
from tkinter.messagebox import NO
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from numpy import reciprocal




from sklearn.metrics import max_error

# class Userprofile(models.Model):
    
   



class post(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField(blank=False,max_length=400)
    image=models.ImageField(upload_to='uploads' ,blank=True,null=True)
    created_at=models.DateTimeField(default = datetime.now)
    likes=models.ManyToManyField(User,blank=True,related_name='likes')
    dislikes=models.ManyToManyField(User,blank=True,related_name='dislikes')
    
class comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey('post',on_delete=models.CASCADE)
    comment=models.TextField(blank=False,max_length=400)
    created_at=models.DateTimeField(default = datetime.now)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='+')
    @property
    def children(self):
        return comment.objects.filter(parent=self).order_by('-created_at').all()
    @property
    def isParent(self):
        if self.parent is None:
            return True
        return False

         


class userprofile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE,default='')
    name=models.CharField(max_length=30,blank=True,null=True)
    bio =models.TextField(blank=True,null=True) 
    #upload to a particular file
    profileimg =models.ImageField(upload_to='uploads' ,default='uploads\pic.jfif')
    organisation =models.CharField(max_length=200,blank=True,null=True)
    role=models.CharField(max_length=50,blank=True,null=True)
    yof=models.IntegerField(default =2001,validators=[MaxValueValidator(2024),MinValueValidator(2000)])
    LinkProfile=models.URLField(max_length=100,blank=True,null=True)


@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        userprofile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
