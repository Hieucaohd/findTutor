from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import CommentAboutUserModel, CommentAboutParentRoomModel
from .serializers import CommentAboutUserSerializer, CommentAboutParentRoomSerializer

from findTutor.viewsDic.baseView import UpdateBaseView, DeleteBaseView
from findTutor.models import TutorModel, ParentModel, ParentRoomModel

from authentication.models import User


class CommentListBaseView(APIView):
	#permission_classes = [permissions.IsAuthenticated]

	modelBase = None
	serializerBase = None
	aboutModel = None

	def get(self, request, format=None):
		about_who_pk = request.query_params.get('about_who_id', 0)

		try:
			about_who_pk = int(about_who_pk)
		except:
			return Response(status=status.HTTP_403_FORBIDDEN)
		
		if about_who_pk:
			about_who = self.aboutModel.objects.get(pk=about_who_pk)
			list_comment = self.modelBase.objects.filter(about_who=about_who)

			serializer = self.serializerBase(list_comment, many=True)

			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)


	def post(self, request, format=None):
		if not request.user.is_authenticated:
			return Response(status=status.HTTP_403_FORBIDDEN)

		about_who_pk = request.data.get('about_who_id', 0)
		belong_to_pk = request.data.get('belong_to_id', 0)

		if about_who_pk:
			about_who = self.aboutModel.objects.get(pk=about_who_pk)

			serializer = self.serializerBase(data=request.data)

			if serializer.is_valid():

				if belong_to_pk:
					belong_to = self.modelBase.objects.get(pk=belong_to_pk)
					serializer.save(about_who=about_who, user=request.user, belong_to=belong_to)
				else:
					serializer.save(about_who=about_who, user=request.user)

				data = serializer.data

				return Response(data, status=status.HTTP_200_OK)
			return Response({"du lieu khong hop le": "bad"}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"khong duoc phep": "khong duoc phep"}, status=status.HTTP_400_BAD_REQUEST)


class CommentAboutUserList(CommentListBaseView):
	modelBase = CommentAboutUserModel
	serializerBase = CommentAboutUserSerializer

	aboutModel = User


class CommentAboutParentRoomList(CommentListBaseView):
	modelBase = CommentAboutParentRoomModel
	serializerBase = CommentAboutParentRoomSerializer

	aboutModel = ParentRoomModel


class CommentDetailBaseView(UpdateBaseView, DeleteBaseView):
	def isOwner(self, request, pk):
		return self.get_object(pk).user == request.user

	def put(self, request, pk, format=None):
		if self.isOwner(request, pk):
			return super().put(request, pk)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def delete(self, request, pk):
		if self.isOwner(request, pk):
			return super().delete(request, pk)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)


class CommentAboutUserDetail(CommentDetailBaseView):
	modelBase = CommentAboutUserModel
	serializerBase = CommentAboutUserSerializer


class CommentAboutParentRoomDetail(CommentDetailBaseView):
	modelBase = CommentAboutParentRoomModel
	serializerBase = CommentAboutParentRoomSerializer


























