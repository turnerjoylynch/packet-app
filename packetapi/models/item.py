from django.db import models

from packetapi.models.list import PacketList
from packetapi.models.user import PacketUser


class PacketItem(models.Model):

    userId = models.ForeignKey(PacketUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=150)
    lists = models.ForeignKey(PacketList, on_delete=models.CASCADE)
    created_on = models.DateTimeField
