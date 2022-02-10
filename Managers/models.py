''' Models for Managers '''
from django.db import models
from Users.models import AppComment

class Manager(models.Model):
    ''' Models for Manager '''

    account = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.account

class ManagerResponse(models.Model):
    ''' Models for Manager Response to appcomments'''

    manager = models.ForeignKey(Manager, related_name="responses", on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    response = models.OneToOneField(AppComment, on_delete=models.CASCADE)
