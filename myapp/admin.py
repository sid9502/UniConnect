import imp
from django.contrib import admin
from .models import comment,post,userprofile
# # Register your models here.

admin.site.register(post)
admin.site.register(comment)
# admin.site.register(Userprofile)
admin.site.register(userprofile)