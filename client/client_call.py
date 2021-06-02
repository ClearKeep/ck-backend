from __future__ import print_function

import grpc

from protos import video_call_pb2, video_call_pb2_grpc


class ClientVideoCall:
    def __init__(self, host, port):
        self.stub = self.grpc_stub(host, port)

    def grpc_stub(self, host, port):
        channel = grpc.insecure_channel(host + ':' + str(port))
        return video_call_pb2_grpc.VideoCallStub(channel)

    def video_call(self, request):
        try:
            response = self.stub.video_call(request)
            return response
        except:
            return None

    def cancel_request_call(self, request):
        try:
            response = self.stub.cancel_request_call(request)
            return response
        except:
            return None

    def update_call(self, request):
        try:
            response = self.stub.update_call(request)
            return response
        except:
            return None