from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from packetapi.models.item import PacketItem
from rest_framework.decorators import action
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
        items = PacketItem.objects.get(pk=request.data["items"])
        
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
        item = PacketItem.objects.get(pk=pk)
        list.list_name = request.data["list_name"]

        
        lists = PacketList.objects.get(pk=request.data["lists"])
        item.lists = lists
         
        list.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        list = PacketList.objects.get(pk=pk)
        list.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


''' Actions to include the JOIN tables??
'''

@action(methods=['post'], detail=True)
def join_list(self, request, pk):
        """Post request to add a item to a list"""
        list = PacketList.objects.get(pk=pk)
        item = request.data['item']
        list.items.add(item) 
        return Response({'message': 'Item added'}, status=status.HTTP_201_CREATED)
    
@action(methods=['delete'], detail=True)
def remove(self, request, pk):
        """Delete request of a item to be removed from a list"""
        item = PacketItem.objects.get(pk=pk)
        list = PacketList.objects.get(pk=pk)
        list.items.remove(item)
        return Response({'message': 'Item removed'}, status=status.HTTP_204_NO_CONTENT)
    
    # @action(methods=['get'], detail=True)
    # def partner_alert(self, request, pk):
    #     """ Gets user's partner pairing """
    #     try: 
    #         group = Group.objects.get(pk=pk)
    #         giver = Member.objects.get(user=request.auth.user)
    #         partner = Partner.objects.get(giver_id=giver.id, group_id=group.id)
    #         serializer = PartnerSerializer(partner)
    #         return Response(serializer.data)
    #     except Partner.DoesNotExist as ex:
    #         return Response({'message': ex.arg[0]}, status=status.HTTP_404_NOT_FOUND)
  
    
''' Actions to include the JOIN tables??
'''
  
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