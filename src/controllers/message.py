from protos import message_pb2
from src.controllers.base import *
from middlewares.permission import *
from utils.logger import *
from middlewares.request_logged import *
from src.services.message import MessageService, client_message_queue
from src.services.signal import SignalService
from client.client_message import *
from utils.config import get_system_domain, get_ip_domain

class MessageController(BaseController):
    def __init__(self, *kwargs):
        self.service = MessageService()

    @request_logged
    def get_messages_in_group(self, request, context):
        try:
            domain_local = get_system_domain()
            domain_client = request.domain
            group_id = request.group_id
            off_set = request.off_set
            last_message_at = request.last_message_at
            if domain_client == domain_local:
                lst_message = self.service.get_message_in_group(group_id, off_set, last_message_at)
            else:
                server_ip = get_ip_domain(domain_client)
                client = ClientMessage(server_ip, get_system_config()['port'])
                lst_message = client.get_messages_group(request)

            return lst_message
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CREATE_GROUP_CHAT_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    def Publish(self, request, context):
        try:
            group_id = request.groupId
            client_id = request.clientId

            # store message here
            new_message = MessageService().store_message(
                group_id=group_id,
                from_client_id=request.fromClientId,
                client_id=client_id,
                message=request.message
            )

            # put for other client
            if client_id:
                message_channel = "{}/message".format(client_id)
                if message_channel in client_message_queue:
                    client_message_queue[message_channel].put(new_message)
                # else:
                #     logger.error("client queue not found")
                #     errors = [Message.get_error_object(Message.CLIENT_QUEUE_NOT_FOUND)]
                #     context.set_details(json.dumps(
                #         errors, default=lambda x: x.__dict__))
                #     context.set_code(grpc.StatusCode.INTERNAL)
            else:
                lst_client = SignalService().group_get_all_client_key(group_id)
                for client in lst_client:
                    if client.client_id != request.fromClientId:
                        message_channel = "{}/message".format(client.client_id)
                        if message_channel in client_message_queue:
                            client_message_queue[message_channel].put(new_message)

            return new_message

        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_PUBLISH_MESSAGE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    def Listen(self, request, context):
        client_id = request.clientId
        message_channel = "{}/message".format(client_id)
        while context.is_active():
            try:
                if message_channel in client_message_queue:
                    message_response = client_message_queue[message_channel].get()
                    if not context.is_active():
                        break
                    yield message_response #print(message_response)
            except Exception as e:
                logger.error(e) # print(ex)
                context.cancel()
                client_message_queue[message_channel] = None
                del client_message_queue[message_channel]

    @request_logged
    def Subscribe(self, request, context):
        try:
            self.service.subscribe(request.clientId)
            return message_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_SUBCRIBE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    def UnSubscribe(self, request, context):
        try:
            self.service.un_subscribe(request.clientId)
            return message_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_SUBCRIBE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
