from protos import message_pb2
from src.controllers.base import *
from middlewares.permission import *
from utils.logger import *
from middlewares.request_logged import *
from src.services.message import MessageService, client_message_queue
from src.services.signal import SignalService
from queue import Empty
from src.models.user import User
from src.models.signal_group_key import GroupClientKey
from utils.const import DeviceType
from kalyke.payload import PayloadAlert
from src.services.notify_push import NotifyPushService
from firebase_admin import messaging


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

            ios_tokens = []
            android_tokens = []

            # put for other client
            if client_id:
                message_channel = "{}/message".format(client_id)
                if message_channel in client_message_queue:
                    client_message_queue[message_channel].put(new_message)
                else:
                    #push text notification for client
                    client = User().get_client_id_with_push_token(client_id)
                    for client_token in client.User.tokens:
                        if client_token.device_type == DeviceType.android:
                            android_tokens.append(client_token.push_token)
                        elif client_token.device_type == DeviceType.ios:
                            arr_token = client_token.push_token.split(',')
                            ios_tokens.append(arr_token[-1])

            else:
                #push for other people in group
                lst_client_in_groups = GroupClientKey().get_clients_in_group_with_push_token(group_id)
                for client in lst_client_in_groups:
                    if client.User.id != request.fromClientId:
                        message_channel = "{}/message".format(client.User.id)
                        if message_channel in client_message_queue:
                            client_message_queue[message_channel].put(new_message)
                        else:
                            for client_token in client.User.tokens:
                                if client_token.device_type == DeviceType.android:
                                    android_tokens.append(client_token.push_token)
                                elif client_token.device_type == DeviceType.ios:
                                    arr_token = client_token.push_token.split(',')
                                    ios_tokens.append(arr_token[-1])

            push_service = NotifyPushService()
            if len(android_tokens) > 0:
                notification = messaging.Notification(
                    title='',
                    body='You have a new message',
                )
                push_service.android_text_notifications(android_tokens, notification)
            if len(ios_tokens) > 0:
                payload_alert = PayloadAlert(title="ClearKeep", body="You have a new message")
                push_service.ios_text_notifications(ios_tokens, payload_alert)

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
                    yield message_response #print(message_response)
            except:
                logger.info('Client {} is disconnected'.format(client_id))
                context.cancel()
                print(' context.is_active()=', context.is_active())
                print('len queue before=', len(client_message_queue))
                client_message_queue[message_channel] = None
                del client_message_queue[message_channel]
                print('len queue after=', len(client_message_queue))
                #need push notify here

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

