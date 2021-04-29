from __future__ import print_function

import grpc

from protos import group_pb2, group_pb2_grpc


class ClientGroup:
    def __init__(self, host, port):
        self.stub = self.grpc_stub(host, port)

    def grpc_stub(self, host, port):
        channel = grpc.insecure_channel(host + ':' + str(port))
        return group_pb2_grpc.GroupStub(channel)
