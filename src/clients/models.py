from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    '''
    Data model for client entities
    '''
    client_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clients'
        default_permissions = () 

    def __str__(self):
        return self.client_name
