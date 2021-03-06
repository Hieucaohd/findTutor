from findTutor.messages import RoomNotificationMessage
from ..serializers import WaitingTutorSerializer, ListInvitedSerializer
from ..models import TutorModel, ParentModel, WaitingTutorModel, ListInvitedModel, TutorTeachingModel

from rest_framework.response import Response
from rest_framework import status, permissions

from .relateParentRoomBaseView import ItemRelateListBaseView
from .baseView import RetrieveUpdateDeleteBaseView

from findTutor.signals import tutor_out_room_signal

import threading


class WaitingTutorList(ItemRelateListBaseView):
    modelBase = WaitingTutorModel
    serializerBase = WaitingTutorSerializer

    def get_tutor_from_request(self, request):
        return TutorModel.objects.get(user=request.user)

    def get_for_room(self, request):
        return super().get(request)

    def get_for_tutor(self, request):
        tutor_request = self.get_tutor_from_request(request)
        list_waiting_for_tutor = self.modelBase.objects.filter(tutor=tutor_request)
        serializer = self.serializerBase(list_waiting_for_tutor, many=True)
        data = serializer.data
        return Response(data)

    def get(self, request, format=None):
        if self.get_pk_room(request):
            return self.get_for_room(request)
        else:
            return self.get_for_tutor(request)

    def isTutor(self, request):
        take_tutor_request = TutorModel.objects.filter(user=request.user)   # take_tutor_request is a list.
        if take_tutor_request:
            return True
        return False

    def hasTutorInListWaiting(self, request):
        take_tutor_request = TutorModel.objects.filter(user=request.user)   # take_tutor_request is a list.

        if take_tutor_request:
            tutor_request = take_tutor_request[0]
        else:
            return True

        room = self.get_room(request)
        list_waiting = self.modelBase.objects.filter(parent_room=room)
        for wait in list_waiting:
            if wait.tutor == tutor_request:
                return True
        return False

    def post(self, request, format=None):
        """
            Use when tutor want to join waiting list of a room parent.
        """
        if self.isTutor(request) and (not self.hasTutorInListWaiting(request)):
            room = self.get_room(request)
            tutor = TutorModel.objects.get(user=request.user)
            serializer = self.serializerBase(data=request.data)
            if serializer.is_valid():
                serializer.save(parent_room=room, tutor=tutor)
                
                data = serializer.data

                return Response(data)
            return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class WaitingTutorDetail(RetrieveUpdateDeleteBaseView):
    permission_classes = [permissions.IsAuthenticated]

    modelBase = WaitingTutorModel
    serializerBase = WaitingTutorSerializer

    def isOwnerOfRoom(self, request, pk):
        waiting_obj = self.get_object(pk)
        return waiting_obj.parent_room.parent.user == request.user

    def isTutorCreate(self, request, pk):
        waiting_obj = self.get_object(pk)
        return waiting_obj.tutor.user == request.user

    def put(self, request, pk, format=None):
        """
            When parent (owner of room) invite tutor.
        """
        pass

    def delete(self, request, pk, format=None):
        """
            When parent or tutor don't want to continua waiting.
        """
        waiting_item = self.get_object(pk)
        kwargs = {
            "user_send": request.user,
            "instance": waiting_item,
            "sender": self.__class__
        }
        if self.isOwnerOfRoom(request, pk):
            # notify for tutor 
            kwargs["user_receive"] = waiting_item.tutor.user
            kwargs["text"] = RoomNotificationMessage.generate_text(
                                id=RoomNotificationMessage.message_type['parent_delete_tutor_from_waiting_list']['notify_tutor'],
                                user_send=request.user
                            )
            threading.Thread(target=tutor_out_room_signal.send, kwargs=kwargs).start()
            return super().delete(request, pk)
        elif self.isTutorCreate(request, pk):
            # notify for parent
            kwargs['user_receive'] = waiting_item.parent_room.parent.user
            kwargs['text'] = RoomNotificationMessage.generate_text(
                                id=RoomNotificationMessage.message_type['tutor_out_from_waiting_list']['notify_parent'],
                                user_send=request.user
                            )
            threading.Thread(target=tutor_out_room_signal.send, kwargs=kwargs).start()
            return super().delete(request, pk)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
