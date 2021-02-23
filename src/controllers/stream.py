from grpclib.server import Stream

from middlewares.request_logged import *
from protos.stream_grpc import GreeterBase
from protos.stream_pb2 import StreamRequest, StreamReply


class Greeter(GreeterBase):

    # UNARY_UNARY - simple RPC
    @request_logged
    async def UnaryUnaryGreeting(
            self,
            stream: Stream[StreamRequest, StreamReply],
    ) -> None:
        request = await stream.recv_message()
        assert request is not None
        message = f'Stream, {request.name}! anhduc'
        await stream.send_message(StreamReply(message=message))

    # UNARY_STREAM - response streaming RPC
    @request_logged
    async def UnaryStreamGreeting(
            self,
            stream: Stream[StreamRequest, StreamReply],
    ) -> None:
        request = await stream.recv_message()
        assert request is not None
        await stream.send_message(
            StreamReply(message=f'Stream, {request.name}!'))
        await stream.send_message(
            StreamReply(message=f'Goodbye, {request.name}!'))
