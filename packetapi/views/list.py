from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from packetapi.models.item import PacketItem

from packetapi.models.list import PacketList
from packetapi.models.user import PacketUser


class ListView(ViewSet):
    """List view"""
    def retrieve(self, request,pk):
        
        list = PacketList.objects.get(pk=pk)
        serializer = ListSerializer(list)
        return Response(serializer.data)
    
    def list(self, request):
        """Handle GET requests to get all Lists """
        list_view = PacketList.objects.all()

        serializer = ListSerializer(list_view, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized list instance
        """
        data = request.data
        userId = PacketUser.objects.get(user=request.auth.user)
        
        list = PacketList.objects.create(
            userId = userId,
            list_name = request.data["list_name"],
            created_on = datetime.now()
        )
        
        for items in data['items']:
            items_obj = PacketItem.objects.get(item_name=items['item_name'])
            list.items.add(items_obj)        
        
        serializer = CreateListSerializer(list)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def update(self, request, pk):
        """Handle PUT requests for a list
        Returns:
            Response -- Empty body with 204 status code
        """
        list = PacketList.objects.get(pk=pk)
        list.list_name = request.data["list_name"]
        
        item = PacketItem.objects.get(pk=pk)
        # item.name = request.data["item_name"]
        
        lists = PacketList.objects.get(pk=request.data["lists"])
        item.lists = lists
        
        item.save()
        list.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        list = PacketList.objects.get(pk=pk)
        list.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


  
class ListSerializer(serializers.ModelSerializer):
    """JSON serializer for lists """

    class Meta:
        model = PacketList
        fields = ('id', 'userId','list_name','created_on')
        
class CreateListSerializer(serializers.ModelSerializer):
    """JSON serializer for lists """

    class Meta:
        model = PacketList
        fields = ('id', 'userId','list_name','created_on')