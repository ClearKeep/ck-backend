from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.message import MessageService, client_message_queue
from src.services.group import GroupService
from src.models.signal_group_key import GroupClientKey
from src.services.notify_push import NotifyPushService
from protos import message_pb2
from client.client_message import *
import grpc
from grpc import aio
import asyncio
import base64
import uuid
from datetime import datetime
from copy import copy, deepcopy



class MessageController(BaseController):
    def __init__(self, *kwargs):
        self.service = MessageService()

    @request_logged
    async def get_messages_in_group(self, request, context):
        try:
            group_id = request.group_id
            off_set = request.off_set
            last_message_at = request.last_message_at

            owner_workspace_domain = "{}:{}".format(get_system_config()['server_domain'],
                                                    get_system_config()['grpc_port'])

            group = GroupService().get_group_info(group_id)
            if group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain:
                request.group_id = group.owner_group_id
                lst_message = ClientMessage(group.owner_workspace_domain).get_messages_in_group(request)
                if lst_message:
                    return lst_message
                else:
                    raise
            else:
                lst_message = self.service.get_message_in_group(group_id, off_set, last_message_at)
                return lst_message
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CREATE_GROUP_CHAT_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def Publish(self, request, context):
        print("Publish")
        try:
            owner_workspace_domain = "{}:{}".format(get_system_config()['server_domain'],
                                                    get_system_config()['grpc_port'])
            group = GroupService().get_group_info(request.groupId)

            if group.owner_workspace_domain and group.owner_workspace_domain != owner_workspace_domain:
                res_obj = await self.publish_to_group_not_owner(request, group)
                return res_obj
            else:
                res_obj = await self.publish_to_group_owner(request, group)
                return res_obj
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_PUBLISH_MESSAGE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def workspace_publish(self, request, context):
        print("workspace_publish")
        try:
            owner_workspace_domain = "{}:{}".format(get_system_config()['server_domain'],
                                                    get_system_config()['grpc_port'])
            group = GroupService().get_group_info(request.group_id)
            if group.owner_workspace_domain is None or group.owner_workspace_domain == owner_workspace_domain:
                # store message here
                MessageService().store_message(
                    message_id=request.message_id,
                    created_at=datetime.now(),
                    group_id=request.group_id,
                    group_type=request.group_type,
                    from_client_id=request.from_client_id,
                    client_id=request.client_id,
                    message=request.message
                )

            new_message = message_pb2.MessageObjectResponse(
                id=request.message_id,
                client_id=request.client_id,
                group_id=request.group_id,
                group_type=request.group_type,
                from_client_id=request.from_client_id,
                message=request.message,
                created_at=request.created_at,
                updated_at=request.updated_at
            )
            # push notification for other client
            other_clients_in_group = []
            lst_client = GroupService().get_clients_in_group(request.group_id)

            for client in lst_client:
                if client.GroupClientKey.client_workspace_domain != request.from_client_workspace_domain:
                    if client.GroupClientKey.client_workspace_domain is None or client.GroupClientKey.client_workspace_domain == owner_workspace_domain:
                        message_channel = "{}/message".format(client.GroupClientKey.client_id)
                        if message_channel in client_message_queue:
                            client_message_queue[message_channel].put(new_message)
                        else:
                            push_service = NotifyPushService()
                            message = {
                                'id': new_message.id,
                                'client_id': new_message.client_id,
                                'created_at': new_message.created_at,
                                'from_client_id': new_message.from_client_id,
                                'group_id': new_message.group_id,
                                'group_type': request.group_type,
                                'message': base64.b64encode(new_message.message).decode('utf-8')
                            }
                            await push_service.push_text_to_client(client.GroupClientKey.client_id, title="",
                                                                   body="You have a new message",
                                                                   from_client_id=new_message.from_client_id,
                                                                   notify_type="new_message",
                                                                   data=json.dumps(message))
                    else:
                        # call to other server
                        request.group_id = client.GroupClientKey.client_workspace_group_id
                        res_object = ClientMessage(
                            client.GroupClientKey.client_workspace_domain).workspace_publish_message(request)
                        if res_object is None:
                            logger.error("send message to client failed")
            return new_message

        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_PUBLISH_MESSAGE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    async def publish_to_group_owner(self, request, group):
        # store message here
        message_id = str(uuid.uuid4())
        created_at = datetime.now()
        message_res_object = MessageService().store_message(
            message_id=message_id,
            created_at=created_at,
            group_id=group.id,
            group_type=group.group_type,
            from_client_id=request.fromClientId,
            client_id=request.clientId,
            message=request.message
        )
        lst_client = GroupService().get_clients_in_group(group.id)
        push_service = NotifyPushService()

        owner_workspace_domain = "{}:{}".format(get_system_config()['server_domain'],
                                                get_system_config()['grpc_port'])

        for client in lst_client:
            if client.GroupClientKey.client_id != request.fromClientId:
                if client.GroupClientKey.client_workspace_domain is None or client.GroupClientKey.client_workspace_domain == owner_workspace_domain:
                    message_channel = "{}/message".format(client.GroupClientKey.client_id)
                    if message_channel in client_message_queue:
                        client_message_queue[message_channel].put(message_res_object)
                    else:
                        message = {
                            'id': message_res_object.id,
                            'client_id': message_res_object.client_id,
                            'created_at': message_res_object.created_at,
                            'from_client_id': message_res_object.from_client_id,
                            'group_id': message_res_object.group_id,
                            'group_type': message_res_object.group_type,
                            'message': base64.b64encode(message_res_object.message).decode('utf-8')
                        }
                        await push_service.push_text_to_client(client.GroupClientKey.client_id, title="",
                                                               body="You have a new message",
                                                               from_client_id=message_res_object.from_client_id,
                                                               notify_type="new_message",
                                                               data=json.dumps(message))
                else:
                    # call to other server
                    request2 = message_pb2.WorkspacePublishRequest(
                        from_client_id=message_res_object.from_client_id,
                        from_client_workspace_domain=client.GroupClientKey.client_workspace_domain,
                        client_id=message_res_object.client_id,
                        group_id=client.GroupClientKey.client_workspace_group_id,
                        group_type=message_res_object.group_type,
                        message_id=message_res_object.id,
                        message=message_res_object.message,
                        created_at=message_res_object.created_at,
                        updated_at=message_res_object.updated_at,
                    )
                    message_res_object2 = ClientMessage(
                        client.GroupClientKey.client_workspace_domain).workspace_publish_message(request2)
                    if message_res_object2 is None:
                        logger.error("send message to client failed")
        return message_res_object

    async def publish_to_group_not_owner(self, request, group):
        message_id = str(uuid.uuid4())
        created_at = datetime.now()

        message_res_object = message_pb2.MessageObjectResponse(
            id=message_id,
            client_id=request.clientId,
            group_id=group.id,
            group_type=group.group_type,
            from_client_id=request.fromClientId,
            message=request.message,
            created_at=int(created_at.timestamp() * 1000),
        )

        # publish message to user in this server first
        lst_client = GroupService().get_clients_in_group_owner(group.owner_group_id)
        push_service = NotifyPushService()

        for client in lst_client:
            if client.GroupClientKey.client_id != request.fromClientId:
                message_channel = "{}/message".format(client.GroupClientKey.client_id)
                new_message_res_object = deepcopy(message_res_object)
                new_message_res_object.group_id = client.GroupClientKey.group_id
                if message_channel in client_message_queue:
                    client_message_queue[message_channel].put(new_message_res_object)
                else:
                    message = {
                        'id': message_res_object.id,
                        'client_id': message_res_object.client_id,
                        'created_at': message_res_object.created_at,
                        'from_client_id': message_res_object.from_client_id,
                        'group_id': client.GroupClientKey.group_id,
                        'group_type': message_res_object.group_type,
                        'message': base64.b64encode(message_res_object.message).decode('utf-8')
                    }
                    await push_service.push_text_to_client(client.GroupClientKey.client_id, title="",
                                                    body="You have a new message",
                                                    from_client_id=message_res_object.from_client_id,
                                                    notify_type="new_message",
                                                    data=json.dumps(message))

        #pubish message to owner server
        owner_workspace_domain = "{}:{}".format(get_system_config()['server_domain'],
                                                get_system_config()['grpc_port'])
        request1 = message_pb2.WorkspacePublishRequest(
            from_client_id=request.fromClientId,
            from_client_workspace_domain=owner_workspace_domain,
            client_id=request.clientId,
            group_id=group.owner_group_id,
            group_type=group.group_type,
            message_id=message_id,
            message=request.message,
            created_at=int(created_at.timestamp() * 1000)
        )
        res_object = ClientMessage(group.owner_workspace_domain).workspace_publish_message(request1)
        if res_object is None:
            logger.error("send message to client failed")

        #message_res_object.group_id = group.id
        return message_res_object

    # @request_logged
    async def Listen(self, request, context: grpc.aio.ServicerContext):
        client_id = request.clientId
        message_channel = "{}/message".format(client_id)
        message_response = None
        while message_channel in client_message_queue:
            print('client listening=', client_id)
            try:
                if client_message_queue[message_channel].qsize() > 0:
                    message_response = client_message_queue[message_channel].get(True)
                    await context.write(message_response)
                await asyncio.sleep(0.5)
            except:
                logger.info('Client {} is disconnected'.format(client_id))
                client_message_queue[message_channel] = None
                del client_message_queue[message_channel]
                print('len queue after=', len(client_message_queue))
                # push text notification for client
                push_service = NotifyPushService()
                if message_response:
                    message = {
                        'id': message_response.id,
                        'client_id': message_response.client_id,
                        'created_at': message_response.created_at,
                        'from_client_id': message_response.from_client_id,
                        'group_id': message_response.group_id,
                        'group_type': message_response.group_type,
                        'message': base64.b64encode(message_response.message).decode('utf-8')
                    }
                    await push_service.push_text_to_clients(
                        [client_id], title="", body="You have a new message",
                        from_client_id=client_id, notify_type="new_message", data=json.dumps(message))

    @request_logged
    async def Subscribe(self, request, context):
        print("message Subscribe api")
        try:
            await self.service.subscribe(request.clientId)
            return message_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_SUBCRIBE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def UnSubscribe(self, request, context):
        try:
            self.service.un_subscribe(request.clientId)
            return message_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_SUBCRIBE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def read_messages(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']
            lst_message_id = request.lst_message_id
            self.service.read_messages(client_id, lst_message_id)

            return message_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_SUBCRIBE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
