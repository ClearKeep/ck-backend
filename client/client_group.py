from __future__ import print_function

import grpc

from protos import group_pb2, group_pb2_grpc


class ClientGroup:
    def __init__(self, host, port):
        self.stub = self.grpc_stub(host, port)

    def grpc_stub(self, host, port):
        channel = grpc.insecure_channel(host + ':' + str(port))
        return group_pb2_grpc.GroupStub(channel)

    def add_group(self,new_group,lst_client,ref_domain):
        try:
            request = group_pb2.CreateGroupRequest(group_name=new_group.group_name,
                                                   group_type=new_group.group_type,
                                                   created_by_client_id=new_group.created_by_client_id,
                                                   lst_client=lst_client,
                                                   ref_group_id=new_group.group_id,
                                                   ref_domain=ref_domain)
            response = self.stub.create_group(request)
            return response
        except Exception as e:
            print(e)
            return None