from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from packetapi.models.item import PacketItem
from packetapi.models.list import PacketList
from packetapi.models.user import PacketUser

# Need to block out each method and test in Postman / rework if needed

class ItemView(ViewSet):
    """Item view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single Items"""

        item = PacketItem.objects.get(pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    
    def list(self, request):
        """Handle GET requests to get all Items """
        item_view = PacketItem.objects.all()
        list = request.query_params.get('list', None)
        if list is not None:
            item = item.filter(lists=list)

        serializer = ItemSerializer(item_view, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized Item instance
        """
        userId = PacketUser.objects.get(user=request.auth.user)
        lists = PacketList.objects.get(pk=request.data["lists"])

        item = PacketItem.objects.create(
            userId=userId,
            item_name=request.data["item_name"],
            lists=lists,
            created_on=True #Not sure if correct syntax
        )
        serializer = ItemSerializer(item)
        return Response(serializer.data)    

    def update(self, request, pk):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """

        item = PacketItem.objects.get(pk=pk)
        item.name = request.data["item_name"]
        
        lists = PacketList.objects.get(pk=request.data["lists"])
        item.lists = lists
        item.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        item = PacketItem.objects.get(pk=pk)
        item.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

        

class ItemSerializer(serializers.ModelSerializer):
    """JSON serializer for items """
    class Meta:
        model = PacketItem
        fields = ('id', 'userId','item_name', 'lists', 'created_on')
        
        