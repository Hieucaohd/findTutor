from channels.layers import get_channel_layer

from websocket.mongoModels import *
from websocket.models import ChannelNameModel

from authentication.models import User

from findTutor.models import ParentRoomModel

from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

from findTeacherProject.celery import app


class ChannelLayerHandler:
    def __init__(self):
        # function of this class:
        # - send websocket to a group and
        #   save websocket to database of the members of this group
        # - add a user's channel name to a group (save to database)
        pass

    @staticmethod
    def group_send(user_send, group_name, content, save_to_model, consumer="notify.message"):
        if not isinstance(content, dict):
            raise Exception("content is not a dictionary")

        if not isinstance(user_send, User):
            raise Exception("user is not object of User model")

        # send to group
        content['user_id_send'] = user_send.id
        content['type'] = consumer
        async_to_sync(channel_layer.group_send)(group_name, content)

        # save to database mongodb
        members = FollowModel().collection.find({ 
            "following_groups": {
                "$all": [group_name]
            } 
        })

        for member in members:
            content['user_id_receive'] = member["user_id"]
            save_to_model(**content).create(take_result=False)

    @staticmethod
    def group_send_except(user_send, group_name, content, save_to_model, except_users=[], consumer="notify.message"):
        if not isinstance(content, dict):
            raise Exception("content is not a dictionary")

        if not isinstance(user_send, User):
            raise Exception("user send is not object of User model")

        for user in except_users:
            if not isinstance(user, User):
                raise Exception("user in except_users is not object of User model")

        # send to group
        content['user_id_send'] = user_send.id
        content['type'] = consumer
        for user in except_users:
            channel_names = ChannelNameModel.objects.filter(user = user)
            for channel_name in channel_names:
                async_to_sync(channel_layer.group_discard)(group_name, channel_name.channel_name)
        async_to_sync(channel_layer.group_send)(group_name, content)

        # save to database
        members = FollowModel().collection.find({ 
            "following_groups": {
                "$all": [group_name]
            } 
        })

        id_users_except = list(user.id for user in except_users)

        for member in members:
            content['user_id_receive'] = member["user_id"]
            if member["user_id"] in id_users_except:
                continue
            save_to_model(**content).create(take_result=False)

        for user in except_users:
            channel_names = ChannelNameModel.objects.filter(user = user)
            for channel_name in channel_names:
                async_to_sync(channel_layer.group_add)(group_name, channel_name.channel_name)


    @staticmethod
    def group_add(user, group_name):
        if not isinstance(user, User):
            raise Exception("user is not object of User model")

        channel_names = ChannelNameModel.objects.filter(user = user)
        for channel_name in channel_names:
            async_to_sync(channel_layer.group_add)(group_name, channel_name.channel_name)

        follow_model_collection = FollowModel().collection
        follow_model_collection.find_one_and_update({ "user_id": user.id }, { 
            "$addToSet": { 
                "following_groups":  group_name,
            }
        }, upsert=True)

    @staticmethod
    def group_discard(user, group_name):
        if not isinstance(user, User):
            raise Exception("user is not object of User model")

        # remove user's channel name from group
        channel_names = ChannelNameModel.objects.filter(user = user)
        for channel_name in channel_names:
            async_to_sync(channel_layer.group_discard)(group_name, channel_name.channel_name)

        # remove group name from database of user
        follow_model_collection = FollowModel().collection
        follow_model_collection.update({ "user_id": user.id }, {
            "$pull": {
                "following_groups": group_name,
            }
        })

    @staticmethod
    def send(user_send, user_receive, content, save_to_model, consumer="notify.message"):
        if not (isinstance(user_send, User) and isinstance(user_receive, User)):
            raise Exception("user is not object of User model")

        content['user_id_send'] = user_send.id
        content['user_id_receive'] = user_receive.id
        content['type'] = consumer

        # send websocket
        channel_names = ChannelNameModel.objects.filter(user = user_receive)
        for channel_name in channel_names:
            async_to_sync(channel_layer.send)(channel_name.channel_name, content)

        # save to database
        save_to_model(**content).create(take_result=False)