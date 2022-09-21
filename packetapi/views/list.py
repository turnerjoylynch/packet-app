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

    def retrieve(self, request, pk):

        list = PacketList.objects.get(pk=pk)
        serializer = ListSerializer(list)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all Lists """
        userId = PacketUser.objects.get(user=request.auth.user)
        list_view = PacketList.objects.filter(userId=userId)

        serializer = ListSerializer(list_view, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handles POST requests to create new List """
        userId = PacketUser.objects.get(user=request.auth.user)
        list = PacketList.objects.create(
            userId=userId,
            list_name=request.data["list_name"],
            created_on=datetime.now(),
        )
        list.save()
        serializer = CreateListSerializer(list)
        new_list = PacketList.objects.get(pk=serializer.data['id'])
        if request.data['items']:
            for pk in request.data['items']:
                items_obj = PacketItem.objects.get(pk=pk)
                items_obj.lists.add(new_list)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        userId = PacketUser.objects.get(user=request.auth.user)
        list = PacketList.objects.get(pk=pk)
        serializer = CreateListSerializer(list, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(userId=userId)
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

# @action(methods=['delete'], detail=True)
# def remove(self, request, pk):
#         """Delete request of a item to be removed from a list"""
#         item = PacketItem.objects.get(pk=pk)
#         list = PacketList.objects.get(pk=pk)
#         list.items.remove(item)
#         return Response({'message': 'Item removed'}, status=status.HTTP_204_NO_CONTENT)


''' Actions to include the JOIN tables??
'''


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacketItem
        fields = ('id', 'userId', 'item_name', 'created_on')


class ListSerializer(serializers.ModelSerializer):
    """JSON serializer for lists """
    items = ItemSerializer(many=True)

    class Meta:
        model = PacketList
        fields = ('id', 'userId', 'list_name', 'created_on', 'items')


class CreateListSerializer(serializers.ModelSerializer):
    """JSON serializer for lists """

    class Meta:
        model = PacketList
        fields = ('id', 'list_name', 'created_on')
