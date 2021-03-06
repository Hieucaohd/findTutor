from ..serializers import PriceSerializer
from ..models import PriceModel, ParentRoomModel

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from django.http import Http404

from .baseView import *
from .relateParentRoomBaseView import *


class PriceList(ItemRelateListBaseView):
    modelBase = PriceModel
    serializerBase = PriceSerializer

    def isOwnerOfRoom(self, request):
        room = self.get_room(request)
        return room.parent.user == request.user

    def post(self, request, format=None):
        if self.isOwnerOfRoom(request):
            room = self.get_room(request)
            serializer = self.serializerBase(data=request.data)
            if serializer.is_valid():
                serializer.save(parent_room=room)
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class PriceDetail(RetrieveUpdateDeleteBaseView):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = PriceModel
    serializerBase = PriceSerializer

    def isOwnerOfPrice(self, request, pk):
        price_obj = self.get_object(pk)
        return price_obj.parent_room.parent.user == request.user

    def put(self, request, pk, format=None):
        if self.isOwnerOfPrice(request, pk):
            return super().put(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        if self.isOwnerOfPrice(request, pk):
            return super().delete(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
