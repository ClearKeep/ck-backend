# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/auth.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/auth.proto',
  package='auth',
  syntax='proto3',
  serialized_pb=_b('\n\x10proto/auth.proto\x12\x04\x61uth\"@\n\x07\x41uthReq\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x11\n\tauth_type\x18\x03 \x01(\x03\"\xc1\x01\n\x07\x41uthRes\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x12\n\nexpires_in\x18\x02 \x01(\x03\x12\x1a\n\x12refresh_expires_in\x18\x03 \x01(\x03\x12\x15\n\rrefresh_token\x18\x04 \x01(\t\x12\x12\n\ntoken_type\x18\x05 \x01(\t\x12\x15\n\rsession_state\x18\x06 \x01(\t\x12\r\n\x05scope\x18\x07 \x01(\t\x12\r\n\x05\x65mail\x18\x08 \x01(\t\x12\x10\n\x08username\x18\t \x01(\t\"S\n\x0bRegisterReq\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x11\n\tauth_type\x18\x04 \x01(\x03\"\x1e\n\x0bRegisterRes\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\x63\n\x04\x41uth\x12\'\n\x05login\x12\r.auth.AuthReq\x1a\r.auth.AuthRes\"\x00\x12\x32\n\x08register\x12\x11.auth.RegisterReq\x1a\x11.auth.RegisterRes\"\x00\x62\x06proto3')
)




_AUTHREQ = _descriptor.Descriptor(
  name='AuthReq',
  full_name='auth.AuthReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='username', full_name='auth.AuthReq.username', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='password', full_name='auth.AuthReq.password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='auth_type', full_name='auth.AuthReq.auth_type', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=26,
  serialized_end=90,
)


_AUTHRES = _descriptor.Descriptor(
  name='AuthRes',
  full_name='auth.AuthRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='access_token', full_name='auth.AuthRes.access_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='expires_in', full_name='auth.AuthRes.expires_in', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='refresh_expires_in', full_name='auth.AuthRes.refresh_expires_in', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='refresh_token', full_name='auth.AuthRes.refresh_token', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='token_type', full_name='auth.AuthRes.token_type', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='session_state', full_name='auth.AuthRes.session_state', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='scope', full_name='auth.AuthRes.scope', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='email', full_name='auth.AuthRes.email', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='username', full_name='auth.AuthRes.username', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=93,
  serialized_end=286,
)


_REGISTERREQ = _descriptor.Descriptor(
  name='RegisterReq',
  full_name='auth.RegisterReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='email', full_name='auth.RegisterReq.email', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='username', full_name='auth.RegisterReq.username', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='password', full_name='auth.RegisterReq.password', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='auth_type', full_name='auth.RegisterReq.auth_type', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=288,
  serialized_end=371,
)


_REGISTERRES = _descriptor.Descriptor(
  name='RegisterRes',
  full_name='auth.RegisterRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='auth.RegisterRes.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=373,
  serialized_end=403,
)

DESCRIPTOR.message_types_by_name['AuthReq'] = _AUTHREQ
DESCRIPTOR.message_types_by_name['AuthRes'] = _AUTHRES
DESCRIPTOR.message_types_by_name['RegisterReq'] = _REGISTERREQ
DESCRIPTOR.message_types_by_name['RegisterRes'] = _REGISTERRES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AuthReq = _reflection.GeneratedProtocolMessageType('AuthReq', (_message.Message,), dict(
  DESCRIPTOR = _AUTHREQ,
  __module__ = 'proto.auth_pb2'
  # @@protoc_insertion_point(class_scope:auth.AuthReq)
  ))
_sym_db.RegisterMessage(AuthReq)

AuthRes = _reflection.GeneratedProtocolMessageType('AuthRes', (_message.Message,), dict(
  DESCRIPTOR = _AUTHRES,
  __module__ = 'proto.auth_pb2'
  # @@protoc_insertion_point(class_scope:auth.AuthRes)
  ))
_sym_db.RegisterMessage(AuthRes)

RegisterReq = _reflection.GeneratedProtocolMessageType('RegisterReq', (_message.Message,), dict(
  DESCRIPTOR = _REGISTERREQ,
  __module__ = 'proto.auth_pb2'
  # @@protoc_insertion_point(class_scope:auth.RegisterReq)
  ))
_sym_db.RegisterMessage(RegisterReq)

RegisterRes = _reflection.GeneratedProtocolMessageType('RegisterRes', (_message.Message,), dict(
  DESCRIPTOR = _REGISTERRES,
  __module__ = 'proto.auth_pb2'
  # @@protoc_insertion_point(class_scope:auth.RegisterRes)
  ))
_sym_db.RegisterMessage(RegisterRes)



_AUTH = _descriptor.ServiceDescriptor(
  name='Auth',
  full_name='auth.Auth',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=405,
  serialized_end=504,
  methods=[
  _descriptor.MethodDescriptor(
    name='login',
    full_name='auth.Auth.login',
    index=0,
    containing_service=None,
    input_type=_AUTHREQ,
    output_type=_AUTHRES,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='register',
    full_name='auth.Auth.register',
    index=1,
    containing_service=None,
    input_type=_REGISTERREQ,
    output_type=_REGISTERRES,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_AUTH)

DESCRIPTOR.services_by_name['Auth'] = _AUTH

try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities


  class AuthStub(object):
    # missing associated documentation comment in .proto file
    pass

    def __init__(self, channel):
      """Constructor.

      Args:
        channel: A grpc.Channel.
      """
      self.login = channel.unary_unary(
          '/auth.Auth/login',
          request_serializer=AuthReq.SerializeToString,
          response_deserializer=AuthRes.FromString,
          )
      self.register = channel.unary_unary(
          '/auth.Auth/register',
          request_serializer=RegisterReq.SerializeToString,
          response_deserializer=RegisterRes.FromString,
          )


  class AuthServicer(object):
    # missing associated documentation comment in .proto file
    pass

    def login(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')

    def register(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')


  def add_AuthServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'login': grpc.unary_unary_rpc_method_handler(
            servicer.login,
            request_deserializer=AuthReq.FromString,
            response_serializer=AuthRes.SerializeToString,
        ),
        'register': grpc.unary_unary_rpc_method_handler(
            servicer.register,
            request_deserializer=RegisterReq.FromString,
            response_serializer=RegisterRes.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'auth.Auth', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


  class BetaAuthServicer(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    # missing associated documentation comment in .proto file
    pass
    def login(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def register(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


  class BetaAuthStub(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    # missing associated documentation comment in .proto file
    pass
    def login(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      # missing associated documentation comment in .proto file
      pass
      raise NotImplementedError()
    login.future = None
    def register(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      # missing associated documentation comment in .proto file
      pass
      raise NotImplementedError()
    register.future = None


  def beta_create_Auth_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_deserializers = {
      ('auth.Auth', 'login'): AuthReq.FromString,
      ('auth.Auth', 'register'): RegisterReq.FromString,
    }
    response_serializers = {
      ('auth.Auth', 'login'): AuthRes.SerializeToString,
      ('auth.Auth', 'register'): RegisterRes.SerializeToString,
    }
    method_implementations = {
      ('auth.Auth', 'login'): face_utilities.unary_unary_inline(servicer.login),
      ('auth.Auth', 'register'): face_utilities.unary_unary_inline(servicer.register),
    }
    server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
    return beta_implementations.server(method_implementations, options=server_options)


  def beta_create_Auth_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_serializers = {
      ('auth.Auth', 'login'): AuthReq.SerializeToString,
      ('auth.Auth', 'register'): RegisterReq.SerializeToString,
    }
    response_deserializers = {
      ('auth.Auth', 'login'): AuthRes.FromString,
      ('auth.Auth', 'register'): RegisterRes.FromString,
    }
    cardinalities = {
      'login': cardinality.Cardinality.UNARY_UNARY,
      'register': cardinality.Cardinality.UNARY_UNARY,
    }
    stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
    return beta_implementations.dynamic_stub(channel, 'auth.Auth', cardinalities, options=stub_options)
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
