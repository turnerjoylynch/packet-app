from django.db import models

from packetapi.models.user import PacketUser


class PacketList(models.Model):

    userId = models.ForeignKey(PacketUser, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=150)
    created_on = models.DateTimeField
