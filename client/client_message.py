from __future__ import print_function

import grpc

from protos import message_pb2, message_pb2_grpc


class ClientMessage:
    def __init__(self, host, port):
        self.stub = self.grpc_stub(host, port)

    def grpc_stub(self, host, port):
        channel = grpc.insecure_channel(host + ':' + str(port))
        return message_pb2_grpc.MessageStub(channel)

    def get_messages_group(self,request):
        try:
            request = message_pb2.GetMessagesInGroupRequest(group_id=request.group_id,
                                                   off_set=request.off_set,
                                                   last_message_at=request.last_message_at,
                                                   domain=request.domain)
            response = self.stub.get_messages_in_group(request)
            return response
        except Exception as e:
            print(e)
            return None