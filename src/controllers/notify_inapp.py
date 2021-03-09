import asyncio

from protos import notify_pb2
from src.controllers.base import *
from middlewares.permission import *
from utils.logger import *
from middlewares.request_logged import *
from src.services.notify_inapp import NotifyInAppService, client_notify_queue


class NotifyInAppController(BaseController):
    def __init__(self, *kwargs):
        self.service = NotifyInAppService()

    @request_logged
    async def get_unread_notifies(self, request, context):
        try:
            header_data = dict(context.invocation_metadata())
            introspect_token = KeyCloakUtils.introspect_token(header_data['access_token'])
            client_id = introspect_token['sub']

            lst_notify = self.service.get_unread_notifies(client_id)
            return lst_notify
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.GET_CLIENT_NOTIFIES_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    # @request_logged
    async def listen(self, request, context):
        client_id = request.client_id
        notify_channel = "{}/notify".format(client_id)
        listening = True
        while listening:
            try:
                if notify_channel in client_notify_queue:
                    if client_notify_queue[notify_channel].qsize() > 0:
                        notify_response = client_notify_queue[notify_channel].get(True)
                        notify_stream_response = notify_pb2.NotifyObjectResponse(
                            id=notify_response.id,
                            client_id=notify_response.client_id,
                            ref_client_id=notify_response.ref_client_id,
                            ref_group_id=notify_response.ref_group_id,
                            notify_type=notify_response.notify_type,
                            notify_image=notify_response.notify_image,
                            notify_title=notify_response.notify_title,
                            notify_content=notify_response.notify_content,
                            read_flg=notify_response.read_flg,
                            created_at=int(notify_response.created_at.timestamp() * 1000)
                        )
                    await context.write(notify_stream_response)
                await asyncio.sleep(1)
            except:
                logger.info('Client notify {} is disconnected'.format(client_id))
                listening = False
                client_notify_queue[notify_channel] = None
                del client_notify_queue[notify_channel]

    @request_logged
    async def subscribe(self, request, context):
        print("notify_inapp subscribe api")
        try:
            self.service.subscribe(request.client_id)
            return notify_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_SUBCRIBE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def un_subscribe(self, request, context):
        print("notify_inapp un_subscribe api")
        try:
            self.service.un_subscribe(request.clientId)
            return notify_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_SUBCRIBE_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)

    @request_logged
    async def read_notify(self, request, context):
        try:
            notify_id = request.notify_id
            self.service.read_notify(notify_id)
            return notify_pb2.BaseResponse(success=True)
        except Exception as e:
            logger.error(e)
            errors = [Message.get_error_object(Message.CLIENT_READ_NOTIFY_FAILED)]
            context.set_details(json.dumps(
                errors, default=lambda x: x.__dict__))
            context.set_code(grpc.StatusCode.INTERNAL)
