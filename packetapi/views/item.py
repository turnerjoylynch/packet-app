from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from packetapi.models.item import PacketItem
from packetapi.models.list import PacketList
from packetapi.models.user import PacketUser


class ItemView(ViewSet):
    """Item view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single Items"""

        item = PacketItem.objects.get(pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all Items """
        userId = PacketUser.objects.get(user=request.auth.user)
        item_view = PacketItem.objects.filter(userId=userId)

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

        item = PacketItem.objects.create(
            userId=userId,
            item_name=request.data["item_name"],
            created_on=datetime.now(),
        )

        item.save()
        serializer = CreateItemSerializer(item)
        new_item = PacketItem.objects.get(pk=serializer.data['id'])
        if request.data['lists']:
            for pk in request.data['lists']:
                lists_obj = PacketList.objects.get(pk=pk)
                new_item.lists.add(lists_obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a trip
        Returns:
            Response -- Empty body with 204 status code
        """
        item = PacketItem.objects.get(pk=pk)
        serializer = CreateItemSerializer(item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        item = PacketItem.objects.get(pk=pk)
        item.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ItemSerializer(serializers.ModelSerializer):
    """JSON serializer for items """
    class Meta:
        model = PacketItem
        fields = ('id', 'userId', 'item_name', 'lists', 'created_on')


class CreateItemSerializer(serializers.ModelSerializer):
    """JSON serializer for items """
    class Meta:
        model = PacketItem
        fields = ('id', 'userId', 'item_name', 'lists', 'created_on')
        depth = 2
