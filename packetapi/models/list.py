from django.db import models


class PacketList(models.Model):

    userId = models.OneToOneField(User, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=150)
    created_on = models.DateTimeField
    
    
     ## To be refined