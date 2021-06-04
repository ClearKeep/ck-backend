from __future__ import print_function

import grpc

from protos import group_pb2, group_pb2_grpc


class ClientGroup:
    def __init__(self, workspace_domain):
        self.stub = self.grpc_stub(workspace_domain)

    def grpc_stub(self, workspace_domain):
        channel = grpc.insecure_channel(workspace_domain)
        return group_pb2_grpc.GroupStub(channel)

    def create_group_workspace(self, group_name, group_type, client_id, lst_client, owner_group_id, owner_workspace_domain):
        try:
            request = group_pb2.CreateGroupWorkspaceRequest(group_name=group_name, group_type=group_type,
                                                            client_id=client_id, lst_client=lst_client, owner_group_id=owner_group_id,
                                                            owner_workspace_domain=owner_workspace_domain)
            response = self.stub.create_group_workspace(request)
            return response
        except:
            return None
