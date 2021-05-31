from __future__ import print_function

import grpc

from protos import notify_push_pb2, notify_push_pb2_grpc


class ClientPush:
    def __init__(self, host, port):
        self.stub = self.grpc_stub(host, port)

    def grpc_stub(self, host, port):
        channel = grpc.insecure_channel(host + ':' + str(port))
        return notify_push_pb2_grpc.NotifyPushStub(channel)

    def push_text(self, request):
        try:
            response = self.stub.push_text(request)
            return response
        except:
            return None

    def push_voip(self, to_client_id, payload, from_client_id):
        try:
            request = notify_push_pb2.PushVoipRequest(
                from_client_id=from_client_id,
                payload=payload,
                to_client_id=to_client_id
            )
            response = self.stub.push_voip(request)
            return response
        except:
            return None

    def update_call(self, request):
        try:
            response = self.stub.update_call(request)
            return response
        except:
            return None
