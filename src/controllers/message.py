from protos import message_pb2
from src.controllers.base import *
from middlewares.permission import *
from middlewares.request_logged import *
from src.services.message import MessageService, client_message_queue
from src.models.signal_group_key import GroupClientKey
from src.services.notify_push import NotifyPushService



class MessageController(BaseController):
    def __init__(self, *kwargs):
        self.service = MessageService()

    @request_logged
    def get_messages_in_group(self, request, context):
        try:
            group_id = request.group_id
            off_set = request.off_set
            last_message_at = request.last_message_at
            lst_message = self.service.get_message_in_group(group_id, off_set, last_message_at)
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

            # push notification for other client
            other_clients_in_group = []
            if client_id:
                message_channel = "{}/message".format(client_id)
                if message_channel in client_message_queue:
                    client_message_queue[message_channel].put(new_message)
                else:
                    #push text notification for client
                    other_clients_in_group.append(client_id)
            else:
                #push for other people in group
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
                push_service.push_text_to_clients(other_clients_in_group, title="", body="You have a new message")

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
            print(' context.is_active()=',  context.is_active())
            try:
                if message_channel in client_message_queue:
                    message_response = client_message_queue[message_channel].get()
                    if message_response is None:
                        break
                    yield message_response
            except:
                logger.info('Client {} is disconnected'.format(client_id))
                context.cancel()
                print(' context.is_active()=', context.is_active())
                print('len queue before=', len(client_message_queue))
                client_message_queue[message_channel] = None
                del client_message_queue[message_channel]
                print('len queue after=', len(client_message_queue))
                # push text notification for client
                push_service = NotifyPushService()
                push_service.push_text_to_clients(client_id, title="", body="You have a new message")

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

