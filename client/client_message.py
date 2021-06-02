from __future__ import print_function

import grpc

from protos import message_pb2, message_pb2_grpc


class ClientMessage:
    def __init__(self, host, port):
        self.stub = self.grpc_stub(host, port)

    def grpc_stub(self, host, port):
        channel = grpc.insecure_channel(host + ':' + str(port))
        return message_pb2_grpc.MessageStub(channel)

    def publish_message(self, request):
        # from_client_id, from_client_workspace_domain, client_id, client_workspace_domain,
        # group_id, group_type, message
        try:
            # request = message_pb2.PublishRequest(
            #     fromClientId=from_client_id,
            #     fromClientWorkspaceDomain=from_client_workspace_domain,
            #     clientId=client_id,
            #     clientWorkspaceDomain=client_workspace_domain,
            #     groupId=group_id,
            #     groupType=group_type,
            #     message=message
            # )
            response = self.stub.Publish(request)
            return response
        except:
            return None
