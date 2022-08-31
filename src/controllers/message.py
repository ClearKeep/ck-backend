from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.message import MessageService, client_message_queue
from src.services.group import GroupService
from src.services.notify_push import NotifyPushService
from client.client_message import *
import grpc
from grpc import aio
import asyncio
import base64
import uuid
from datetime import datetime
from copy import deepcopy
from utils.config import *
from protos import message_pb2

import logging
logger = logging.getLogger(__name__)

class MessageController(BaseController):
    def __init__(self, *kwargs):
        self.service = MessageService()

    @request_logged
    @auth_required
    async def get_messages_in_group(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            group_id = request.group_id
            off_set = request.off_set
            last_message_at = request.last_message_at

            owner_workspace_domain = get_owner_workspace_domain()
            group = GroupService().get_group_info(group_id)

            if group and group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain:
                workspace_request = message_pb2.WorkspaceGetMessagesInGroupRequest(
                    group_id = group.owner_group_id,
                    client_id = client_id,
                    off_set = request.off_set,
                    last_message_at = request.last_message_at
                )
                obj_res = await ClientMessage(group.owner_workspace_domain).workspace_get_messages_in_group(workspace_request)
                if obj_res and obj_res.lst_message:
                    for obj in obj_res.lst_message:
                        obj.group_id = group_id
                        obj.client_workspace_domain = owner_workspace_domain
                    return obj_res
                else:
                    raise
            else:
                obj_res = self.service.get_message_in_group(client_id, group_id, off_set, last_message_at)
                return obj_res
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                # TODO: change message when got error
                errors = [Message.get_error_object(Message.GET_MESSAGE_IN_GROUP_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def workspace_get_messages_in_group(self, request, context):
        try:
            logger.info("workspace_get_messages_in_group")
            owner_workspace_domain = get_owner_workspace_domain()
            group = GroupService().get_group_info(request.group_id)
            if group.owner_workspace_domain is None or group.owner_workspace_domain == owner_workspace_domain:
                obj_res = self.service.get_message_in_group(request.client_id, request.group_id, request.off_set, request.last_message_at)
            else:
                raise Exception(Message.GET_MESSAGE_IN_GROUP_FAILED)
            return obj_res
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.GET_MESSAGE_IN_GROUP_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def Publish(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            user_id = introspect_token['sub']

            owner_workspace_domain = get_owner_workspace_domain()
            group = GroupService().get_group_info(request.groupId)

            if group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain:
                res_obj = await self.publish_to_group_not_owner(request, user_id, group)
                return res_obj
            else:
                res_obj = await self.publish_to_group_owner(request, user_id, group)
                return res_obj
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CLIENT_PUBLISH_MESSAGE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def workspace_publish(self, request, context):
        try:
            logger.info("workspace_publish from client_id {}".format(request.from_client_id))
            owner_workspace_domain = get_owner_workspace_domain()
            group = GroupService().get_group_info(request.group_id)
            if group.owner_workspace_domain is None or group.owner_workspace_domain == owner_workspace_domain:
                # store message here
                MessageService().store_message(
                    message_id=request.message_id,
                    created_at=datetime.now(),
                    group_id=request.group_id,
                    group_type=request.group_type,
                    from_client_id=request.from_client_id,
                    from_client_workspace_domain=request.from_client_workspace_domain,
                    client_id=request.client_id,
                    message=request.message,
                    sender_message=request.sender_message
                )
            else:
                MessageService().update_group_last_message(group_id=request.group_id, created_at=datetime.now(), message_id=request.message_id)

            new_message = message_pb2.MessageObjectResponse(
                id=request.message_id,
                client_id=request.client_id,
                group_id=request.group_id,
                group_type=request.group_type,
                from_client_id=request.from_client_id,
                from_client_workspace_domain=request.from_client_workspace_domain,
                message=request.message,
                created_at=request.created_at,
                updated_at=request.updated_at,
                sender_message=request.sender_message
            )
            # push notification for other client
            lst_client = GroupService().get_clients_in_group(request.group_id)
            for client in lst_client:
                if client.GroupClientKey.client_workspace_domain != request.from_client_workspace_domain:
                    if client.GroupClientKey.client_workspace_domain is None or client.GroupClientKey.client_workspace_domain == owner_workspace_domain:
                        if client.User is None:
                            continue
                        for notify_token in client.User.tokens:
                            device_id = notify_token.device_id
                            logger.info('device_id in real loop in handle {}'.format(device_id))
                            if client.GroupClientKey.client_id == request.from_client_id and device_id == request.from_client_device_id:
                                continue
                            message_channel = "message/{}/{}".format(client.GroupClientKey.client_id, device_id)
                            new_message_res_object = deepcopy(new_message)
                            new_message_res_object.client_id = client.GroupClientKey.client_id

                            if message_channel in client_message_queue:
                                logger.info('message channel in handle {}'.format(message_channel))
                                client_message_queue[message_channel].put(new_message_res_object)
                            else:
                                if new_message_res_object.group_type == 'peer' and new_message_res_object.client_id == request.from_client_id:
                                    logger.info('using sender_message')
                                    message_content = base64.b64encode(request.sender_message).decode('utf-8')
                                else:
                                    logger.info('using message')
                                    message_content = base64.b64encode(new_message_res_object.message).decode('utf-8')
                                push_service = NotifyPushService()
                                message = {
                                    'id': new_message_res_object.id,
                                    'client_id': new_message_res_object.client_id,
                                    'client_workspace_domain': get_owner_workspace_domain(),
                                    'created_at': new_message_res_object.created_at,
                                    'from_client_id': new_message_res_object.from_client_id,
                                    'from_client_workspace_domain': new_message_res_object.from_client_workspace_domain,
                                    'group_id': new_message_res_object.group_id,
                                    'group_type': request.group_type,
                                    'message': message_content
                                }
                                await push_service.push_text_to_client_with_device(client.GroupClientKey.client_id, device_id, title="",
                                                                       body="You have a new message",
                                                                       from_client_id=new_message.from_client_id,
                                                                       notify_type="new_message",
                                                                       data=json.dumps(message),
                                                                       from_client_device_id=request.from_client_device_id)
                                continue
                    else:
                        # call to other server
                        request.group_id = client.GroupClientKey.client_workspace_group_id
                        res_object = await ClientMessage(
                            client.GroupClientKey.client_workspace_domain).workspace_publish_message(request)
                        if res_object is None:
                            logger.error("Workspace Publish Message to client failed")
            return new_message

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CLIENT_PUBLISH_MESSAGE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    async def publish_to_group_owner(self, request, from_client_id, group):
        logger.info("publish_to_group_owner from client_id {}, group_id={}".format(from_client_id, str(group.id)))

        owner_workspace_domain = get_owner_workspace_domain()
        # store message here
        message_id = str(uuid.uuid4())
        created_at = datetime.now()

        message_res_object = MessageService().store_message(
            message_id=message_id,
            created_at=created_at,
            group_id=group.id,
            group_type=group.group_type,
            from_client_id=from_client_id,
            from_client_workspace_domain=owner_workspace_domain,
            client_id=request.clientId,
            message=request.message,
            sender_message=request.sender_message
        )
        lst_client = GroupService().get_clients_in_group(group.id)
        push_service = NotifyPushService()

        for client in lst_client:
            if client.GroupClientKey.client_workspace_domain is None or client.GroupClientKey.client_workspace_domain == owner_workspace_domain:
                if client.User is None:
                    continue

                new_message_res_object = deepcopy(message_res_object)
                new_message_res_object.client_id = client.GroupClientKey.client_id
                for notify_token in client.User.tokens:
                    device_id = notify_token.device_id
                    logger.info('device_id in real loop in handle {}'.format(device_id))
                    if client.GroupClientKey.client_id == from_client_id and device_id == request.from_client_device_id:
                        continue
                    message_channel = "message/{}/{}".format(client.GroupClientKey.client_id, device_id)
                    if message_channel in client_message_queue:
                        logger.info('message channel in handle {}'.format(message_channel))
                        client_message_queue[message_channel].put(new_message_res_object)
                    else:
                        if new_message_res_object.group_type == 'peer' and new_message_res_object.client_id == from_client_id:
                            logger.info('using sender_message')
                            message_content = base64.b64encode(request.sender_message).decode('utf-8')
                        else:
                            logger.info('using message')
                            message_content = base64.b64encode(new_message_res_object.message).decode('utf-8')
                        message = {
                            'id': new_message_res_object.id,
                            'client_id': new_message_res_object.client_id,
                            'client_workspace_domain': owner_workspace_domain,
                            'created_at': new_message_res_object.created_at,
                            'from_client_id': new_message_res_object.from_client_id,
                            'from_client_workspace_domain': owner_workspace_domain,
                            'group_id': new_message_res_object.group_id,
                            'group_type': new_message_res_object.group_type,
                            'message': message_content
                        }
                        await push_service.push_text_to_client_with_device(client.GroupClientKey.client_id, device_id, title="",
                                                               body="You have a new message",
                                                               from_client_id=new_message_res_object.from_client_id,
                                                               notify_type="new_message",
                                                               data=json.dumps(message),
                                                               from_client_device_id=request.from_client_device_id)
                            # continue
            else:
                # call to other server
                logger.info('push to client {} in server {}'.format(message_res_object.client_id, client.GroupClientKey.client_workspace_domain))
                request2 = message_pb2.WorkspacePublishRequest(
                    from_client_id=message_res_object.from_client_id,
                    from_client_workspace_domain=owner_workspace_domain,
                    client_id=message_res_object.client_id,
                    group_id=client.GroupClientKey.client_workspace_group_id,
                    group_type=message_res_object.group_type,
                    message_id=message_res_object.id,
                    message=message_res_object.message,
                    created_at=message_res_object.created_at,
                    updated_at=message_res_object.updated_at,
                    from_client_device_id=request.from_client_device_id,
                    sender_message=request.sender_message
                )
                message_res_object2 = await ClientMessage(
                    client.GroupClientKey.client_workspace_domain).workspace_publish_message(request2)
                if message_res_object2 is None:
                    logger.error("send message to client failed")

        return message_res_object

    async def publish_to_group_not_owner(self, request, from_client_id, group):
        logger.info("publish_to_group_not_owner from client_id {}, group_id={}".format(from_client_id, str(group.id)))

        owner_workspace_domain = get_owner_workspace_domain()
        message_id = str(uuid.uuid4())
        created_at = datetime.now()

        MessageService().update_group_last_message(group_id=group.id, created_at=created_at, message_id=message_id)

        message_res_object = message_pb2.MessageObjectResponse(
            id=message_id,
            client_id=request.clientId,
            group_id=group.id,
            group_type=group.group_type,
            from_client_id=from_client_id,
            from_client_workspace_domain=owner_workspace_domain,
            message=request.message,
            created_at=int(created_at.timestamp() * 1000),
            sender_message=request.sender_message
        )

        # publish message to user in this server first
        lst_client = GroupService().get_clients_in_group_owner(group.owner_group_id)
        push_service = NotifyPushService()

        for client in lst_client:
            for notify_token in client.User.tokens:
                if client.User is None:
                    continue
                device_id = notify_token.device_id
                logger.info('device_id in real loop in handle {}'.format(device_id))
                if client.GroupClientKey.client_id == from_client_id and device_id == request.from_client_device_id:
                    continue
                message_channel = "message/{}/{}".format(client.GroupClientKey.client_id, device_id)

                new_message_res_object = deepcopy(message_res_object)
                new_message_res_object.group_id = client.GroupClientKey.group_id
                new_message_res_object.client_id = client.GroupClientKey.client_id

                if message_channel in client_message_queue:
                    client_message_queue[message_channel].put(new_message_res_object)
                else:
                    if new_message_res_object.group_type == 'peer' and new_message_res_object.client_id == from_client_id:
                        logger.info('using sender_message')
                        message_content = base64.b64encode(request.sender_message).decode('utf-8')
                    else:
                        logger.info('using message')
                        message_content = base64.b64encode(new_message_res_object.message).decode('utf-8')
                    message = {
                        'id': new_message_res_object.id,
                        'client_id': new_message_res_object.client_id,
                        'client_workspace_domain': owner_workspace_domain,
                        'created_at': new_message_res_object.created_at,
                        'from_client_id': new_message_res_object.from_client_id,
                        'from_client_workspace_domain': new_message_res_object.from_client_workspace_domain,
                        'group_id': client.GroupClientKey.group_id,
                        'group_type': new_message_res_object.group_type,
                        'message': message_content
                    }
                    await push_service.push_text_to_client_with_device(client.GroupClientKey.client_id, device_id, title="",
                                                           body="You have a new message",
                                                           from_client_id=new_message_res_object.from_client_id,
                                                           notify_type="new_message",
                                                           data=json.dumps(message),
                                                           from_client_device_id=request.from_client_device_id)
                    continue

        # pubish message to owner server
        request1 = message_pb2.WorkspacePublishRequest(
            from_client_id=from_client_id,
            from_client_workspace_domain=owner_workspace_domain,
            client_id=request.clientId,
            group_id=group.owner_group_id,
            group_type=group.group_type,
            message_id=message_id,
            message=request.message,
            created_at=int(created_at.timestamp() * 1000),
            sender_message=request.sender_message,
            from_client_device_id=request.from_client_device_id,
        )
        res_object = await ClientMessage(group.owner_workspace_domain).workspace_publish_message(request1)
        if res_object is None:
            logger.error("send message to client failed")
        return message_res_object

    @request_logged
    @auth_required
    async def Listen(self, request, context: grpc.aio.ServicerContext):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            user_id = introspect_token['sub']

            message_channel = "message/{}/{}".format(user_id, request.device_id)
            logger.info('user {} in device {} has listened'.format(user_id, request.device_id))
            message_response = None
            while message_channel in client_message_queue:
                try:
                    if client_message_queue[message_channel].qsize() > 0:
                        message_response = client_message_queue[message_channel].get(True)
                        await context.write(message_response)
                    await asyncio.sleep(0.5)
                except:
                    logger.info('Client {} is disconnected'.format(user_id))
                    client_message_queue[message_channel] = None
                    del client_message_queue[message_channel]
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.AUTH_USER_NOT_FOUND)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def Subscribe(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            user_id = introspect_token['sub']

            await self.service.subscribe(user_id, request.device_id)
            return message_pb2.BaseResponse()
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CLIENT_SUBCRIBE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def UnSubscribe(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            user_id = introspect_token['sub']

            self.service.un_subscribe(user_id, request.device_id)
            return message_pb2.BaseResponse()
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CLIENT_SUBCRIBE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def read_messages(self, request, context):
        try:
            client_id = request.client_id
            lst_message_id = request.lst_message_id
            self.service.read_messages(client_id, lst_message_id)

            return message_pb2.BaseResponse()
        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.MESSAGE_READ_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    @auth_required
    async def edit_message(self, request, context):
        try:
            group_id = request.groupId
            client_id = request.clientId

            # store message here
            new_message = MessageService().update_message(
                group_id=group_id,
                from_client_id=request.fromClientId,
                client_id=client_id,
                message=request.message,
                message_id=request.id
            )

            # push notification for other client
            other_clients_in_group = []
            if client_id:
                message_channel = "{}/message".format(client_id)
                if message_channel in client_message_queue:
                    client_message_queue[message_channel].put(new_message)
                else:
                    # push text notification for client
                    other_clients_in_group.append(client_id)
            else:
                # push for other people in group
                lst_client_in_groups = GroupClientKey().get_clients_in_group(group_id)
                for client in lst_client_in_groups:
                    if client.User.id != request.fromClientId:
                        message_channel = "{}/message".format(client.User.id)
                        if message_channel in client_message_queue:
                            client_message_queue[message_channel].put(new_message)
                        else:
                            other_clients_in_group.append(client.User.id)

            if len(other_clients_in_group) > 0:
                push_service = NotifyPushService()
                message = {
                    'id': new_message.id,
                    'client_id': new_message.client_id,
                    'created_at': new_message.created_at,
                    'updated_at': new_message.updated_at,
                    'from_client_id': new_message.from_client_id,
                    'group_id': new_message.group_id,
                    'group_type': new_message.group_type,
                    'message': base64.b64encode(new_message.message).decode('utf-8')
                }
                await push_service.push_text_to_clients(other_clients_in_group, title="",
                                                        body="A message has been updated",
                                                        from_client_id=request.fromClientId,
                                                        notify_type="edit_message",
                                                        data=json.dumps(message))
            return new_message

        except Exception as e:
            logger.error(e, exc_info=True)
            if not e.args or e.args[0] not in Message.msg_dict:
                errors = [Message.get_error_object(Message.CLIENT_EDIT_MESSAGE_FAILED)]
            else:
                errors = [Message.get_error_object(e.args[0])]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
