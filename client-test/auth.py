import grpc
import protos.auth_pb2_grpc as auth_service
import protos.auth_pb2 as auth_message

def auth_test():
    channel = grpc.insecure_channel("0.0.0.0:5000")
    client = auth_service.AuthStub(channel)
    response = client.login(auth_message.AuthReq(username='admin', password='admin'), metadata=(
                ('access_token', 'client access token'),
            ))
    if response:
        print( "Auth Response=", response)
        # print( "Name: {}".format(response.name))
        # print( "Gender: {}".format(response.gender))
        # print( "DOB: {}".format(response.birth.ToDatetime()))

if __name__ == '__main__':
    auth_test()