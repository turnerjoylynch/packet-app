from datetime import datetime
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

    # def create(self, request):
    #     """Handle POST operations

    #     Returns
    #         Response -- JSON serialized Item instance
    #     """
    #     data = request.data
    #     userId = PacketUser.objects.get(user=request.auth.user)

    #     item = PacketItem.objects.create(
    #         userId=userId,
    #         item_name=request.data["item_name"],
    #         created_on=datetime.now(),
    #     )

    #     item.save()

    #     for lists in data['lists']:
    #         lists_obj = PacketList.objects.get(list_name=lists['list_name'])
    #         item.lists.add(lists_obj)

    #     serializer = CreateItemSerializer(item)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def create(self, request):
        """Handle POST operations for new idea
        Returns
            Response -- JSON serialized idea instance
        """
        userId = PacketUser.objects.get(user=request.auth.user)
        lists = request.data.get("lists")
        if lists: 
            del request.data["lists"]
        serializer = CreateItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(userId=userId)
        item = PacketItem.objects.get(pk=serializer.data["id"])
        if lists:
            for id in lists:
                lists = PacketList.objects.get(pk=id)
                item.lists.add(lists)
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

# class ItemListSerializer(serializers.ModelSerializer):
#     item = ItemSerializer(many = True,) #To represent the relationship as a string instead of id
#     list = serializers.ListSerializer(many = True, queryset = models.PacketList.objects.all(),slug_field = 'list_name')

#     class Meta:
#         model = models.Book
#         fields = ('name','authors','rating', 'genre')
