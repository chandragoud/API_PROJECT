from django.db import models
from rest_framework import serializers
# Create your models here.
class userregistration(models.Model):

    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=200, null=True, blank=True, default=0)
    lastname = models.CharField(max_length=200, null=True, blank=True, default=0)
    username = models.CharField(max_length=200, null=True, blank=True, default=0)
    email = models.CharField(max_length=200,null=True, unique=True, blank=True, default=0)
    password = models.CharField(max_length=200, null=True, blank=True, default=0)
    mobile = models.CharField(max_length=200,null=True, unique=True, blank=True, default=0)
    createdDate = models.DateTimeField(auto_now_add = True )
    deletedDate = models.DateTimeField(auto_now = True)
    updatedDate = models.DateTimeField(auto_now = True,blank=True)
    loginDateTime = models.DateTimeField(auto_now = True)
    logoutDateTime = models.DateTimeField(auto_now = True,blank=True)
    is_authenticated = models.IntegerField(null=True, blank=True,default=0)
    access_token = models.CharField(max_length=200, blank=True, null=True)

    def __int__(self):
        return self.user_id

class loginSerializerget(serializers.Serializer):
    user_id = serializers.SerializerMethodField()
    def get_user_id(self, obj):
        return obj[0]
    


