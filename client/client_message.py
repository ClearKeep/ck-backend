from __future__ import print_function

import grpc

from protos import message_pb2, message_pb2_grpc


class ClientMessage:
    def __init__(self, host, port):
        self.stub = self.grpc_stub(host, port)



    def grpc_stub(self, host, port):
        channel = grpc.insecure_channel(host + ':' + str(port))
        return message_pb2_grpc.MessageStub(channel)
