from rest_framework.response import Response
from rest_framework import status

from .baseView import CreateBaseView, UpdateBaseView, DeleteBaseView

from ..models import ImagePrivateUserModel, OldImagePrivateUserModel
from ..serializers import ImagePrivateUserSerializer

from django.conf import settings
from ..firebaseConfig import UploadImage


class ImagePrivateUserList(CreateBaseView):
    modelBase = ImagePrivateUserModel
    serializerBase = ImagePrivateUserSerializer

    def post(self, request, format=None):
        serializer = self.serializerBase(data=request.data)
        if serializer.is_valid():

            if settings.USE_FIREBASE:
                #send_request_mutex = threading.Lock()
                threads = {}

                # lay du lieu
                avatar = request.data.get('avatar')
                identity_card = request.data.get('identity_card')
                student_card = request.data.get('student_card')

                avatar_url = None
                if avatar:
                    avatar_thread = UploadImage(avatar, "avatar")
                    threads['avatar'] = avatar_thread
                    avatar_thread.start()
                    

                identity_card_url = None
                if identity_card:
                    identity_card_thread = UploadImage(identity_card, "identity_card")
                    threads['identity_card'] = identity_card_thread
                    identity_card_thread.start()

                student_card_url = None
                if student_card:
                    student_card_thread = UploadImage(student_card, "student_card")
                    threads['student_card'] = student_card_thread
                    student_card_thread.start()

                for thread in threads:
                    threads[thread].join()

                if avatar:
                    avatar_url = threads.get('avatar').url

                if identity_card:
                    identity_card_url = threads.get('identity_card').url

                if student_card:
                    student_card_url = threads.get('student_card').url

                serializer.save(user=request.user, avatar=avatar_url, identity_card=identity_card_url, student_card=student_card_url)
            else:
                serializer.save(user=request.user)
            
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ImagePrivateUserDetail(UpdateBaseView, DeleteBaseView):
    modelBase = ImagePrivateUserModel
    serializerBase = ImagePrivateUserSerializer

    # def which_field_updated(self, request):


    def put(self, request, format=None):
        # print(request.META)
        # print(request.COOKIES)
        get_private_image = self.modelBase.objects.get(user=request.user)

        serializer = self.serializerBase(get_private_image, data=request.data)

        avatar = request.data.get('avatar')
        identity_card = request.data.get('identity_card')
        student_card = request.data.get('student_card')

        if serializer.is_valid():
            threads = {}

            array_item = []
            
            avatar_url = None
            if avatar and get_private_image.avatar:
                old_avatar = OldImagePrivateUserModel()
                old_avatar.image = get_private_image.avatar
                old_avatar.type_image = OldImagePrivateUserModel.type_image_array[0]    # avatar
                array_item.append(old_avatar)

                if settings.USE_FIREBASE:
                    avatar_thread = UploadImage(avatar, "avatar")
                    threads['avatar'] = avatar_thread
                    avatar_thread.start()
            elif avatar and settings.USE_FIREBASE:
                # avatar_url = get_url(avatar, "avatar")
                avatar_thread = UploadImage(avatar, "avatar")
                threads['avatar'] = avatar_thread
                avatar_thread.start()

            identity_card_url = None
            if identity_card and get_private_image.identity_card:
                old_identity_card = OldImagePrivateUserModel()
                old_identity_card.image = get_private_image.identity_card
                old_identity_card.type_image = OldImagePrivateUserModel.type_image_array[1] # identity_card
                array_item.append(old_identity_card)

                if settings.USE_FIREBASE:
                    identity_card_thread = UploadImage(identity_card, "identity_card")
                    threads['identity_card'] = identity_card_thread
                    identity_card_thread.start()
            elif identity_card and settings.USE_FIREBASE:
                # identity_card_url = get_url(identity_card, "identity_card")
                identity_card_thread = UploadImage(identity_card, "identity_card")
                threads['identity_card'] = identity_card_thread
                identity_card_thread.start()

            student_card_url = None
            if student_card and get_private_image.student_card:
                old_student_card = OldImagePrivateUserModel()
                old_student_card.image = get_private_image.student_card
                old_student_card.type_image = OldImagePrivateUserModel.type_image_array[2]  # student_card
                array_item.append(old_student_card)

                if settings.USE_FIREBASE:
                    student_card_thread = UploadImage(student_card, "student_card")
                    threads['student_card'] = student_card_thread
                    student_card_thread.start()
            elif student_card and settings.USE_FIREBASE:
                # student_card_url = get_url(student_card, "student_card")
                student_card_thread = UploadImage(student_card, "student_card")
                threads['student_card'] = student_card_thread
                student_card_thread.start()


            for item in array_item:
                item.type_action = OldImagePrivateUserModel.type_action_array[0]
                item.user = request.user
                item.save()

            for thread in threads:
                threads[thread].join()

            if settings.USE_FIREBASE:
                if threads.get('avatar'):
                    avatar_url = threads.get('avatar').url
                    serializer.save(avatar=avatar_url)

                if threads.get('identity_card'):
                    identity_card_url = threads.get('identity_card').url
                    serializer.save(identity_card=identity_card_url)

                if threads.get('student_card'):
                    student_card_url = threads.get('student_card').url
                    serializer.save(student_card=student_card_url)
            else:
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, format=None):
        get_private_image = self.modelBase.objects.get(user=request.user)
        id_of_item = get_private_image.id
        get_private_image.delete()
        return Response(
                {
                    "id": id_of_item
                }
            )


