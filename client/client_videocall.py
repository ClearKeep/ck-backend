from __future__ import print_function

import grpc

from protos import video_call_pb2, video_call_pb2_grpc


class ClientVideoCall:
    def __init__(self, host, port):
        self.stub = self.grpc_stub(host, port)

    def grpc_stub(self, host, port):
        channel = grpc.insecure_channel(host + ':' + str(port))
        return video_call_pb2_grpc.VideoCallStub(channel)

    def videocall_notify(self,client_id,group_id,domain_client,rtc_client):
        try:
            request = video_call_pb2.VideoCallRequest(client_id=client_id,
                                                   group_id=group_id,
                                                   domain_client=domain_client,
                                                   rtc_client = rtc_client)
            response = self.stub.video_call(request)
            return response
        except Exception as e:
            print(e)
            return None