# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/video_call.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protos/video_call.proto',
  package='video_call',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17protos/video_call.proto\x12\nvideo_call\")\n\x08\x45rrorRes\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x03\x12\x0f\n\x07message\x18\x02 \x01(\t\"E\n\x0c\x42\x61seResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12$\n\x06\x65rrors\x18\x02 \x01(\x0b\x32\x14.video_call.ErrorRes\"\x83\x01\n\x0eServerResponse\x12+\n\x0bstun_server\x18\x01 \x01(\x0b\x32\x16.video_call.StunServer\x12+\n\x0bturn_server\x18\x02 \x01(\x0b\x32\x16.video_call.TurnServer\x12\x17\n\x0fgroup_rtc_token\x18\x03 \x01(\t\"*\n\nStunServer\x12\x0e\n\x06server\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x03\"S\n\nTurnServer\x12\x0e\n\x06server\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x03\x12\x0c\n\x04type\x18\x03 \x01(\t\x12\x0c\n\x04user\x18\x04 \x01(\t\x12\x0b\n\x03pwd\x18\x05 \x01(\t\"J\n\x10VideoCallRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x10\n\x08group_id\x18\x02 \x01(\x03\x12\x11\n\tcall_type\x18\x03 \x01(\t\"\xc7\x01\n\x19WorkspaceVideoCallRequest\x12\x16\n\x0e\x66rom_client_id\x18\x01 \x01(\t\x12\x18\n\x10\x66rom_client_name\x18\x02 \x01(\t\x12\x1a\n\x12\x66rom_client_avatar\x18\x03 \x01(\t\x12$\n\x1c\x66rom_client_workspace_domain\x18\x04 \x01(\t\x12\x11\n\tclient_id\x18\x05 \x01(\t\x12\x10\n\x08group_id\x18\x06 \x01(\x03\x12\x11\n\tcall_type\x18\x07 \x01(\t\":\n\x11UpdateCallRequest\x12\x10\n\x08group_id\x18\x01 \x01(\x03\x12\x13\n\x0bupdate_type\x18\x02 \x01(\t2\xcb\x02\n\tVideoCall\x12H\n\nvideo_call\x12\x1c.video_call.VideoCallRequest\x1a\x1a.video_call.ServerResponse\"\x00\x12O\n\x13\x63\x61ncel_request_call\x12\x1c.video_call.VideoCallRequest\x1a\x18.video_call.BaseResponse\"\x00\x12H\n\x0bupdate_call\x12\x1d.video_call.UpdateCallRequest\x1a\x18.video_call.BaseResponse\"\x00\x12Y\n\x14workspace_video_call\x12%.video_call.WorkspaceVideoCallRequest\x1a\x1a.video_call.ServerResponseb\x06proto3'
)




_ERRORRES = _descriptor.Descriptor(
  name='ErrorRes',
  full_name='video_call.ErrorRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='video_call.ErrorRes.code', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='video_call.ErrorRes.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=39,
  serialized_end=80,
)


_BASERESPONSE = _descriptor.Descriptor(
  name='BaseResponse',
  full_name='video_call.BaseResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='video_call.BaseResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='errors', full_name='video_call.BaseResponse.errors', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=82,
  serialized_end=151,
)


_SERVERRESPONSE = _descriptor.Descriptor(
  name='ServerResponse',
  full_name='video_call.ServerResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='stun_server', full_name='video_call.ServerResponse.stun_server', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='turn_server', full_name='video_call.ServerResponse.turn_server', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='group_rtc_token', full_name='video_call.ServerResponse.group_rtc_token', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=154,
  serialized_end=285,
)


_STUNSERVER = _descriptor.Descriptor(
  name='StunServer',
  full_name='video_call.StunServer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='server', full_name='video_call.StunServer.server', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='video_call.StunServer.port', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=287,
  serialized_end=329,
)


_TURNSERVER = _descriptor.Descriptor(
  name='TurnServer',
  full_name='video_call.TurnServer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='server', full_name='video_call.TurnServer.server', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='video_call.TurnServer.port', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='video_call.TurnServer.type', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user', full_name='video_call.TurnServer.user', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pwd', full_name='video_call.TurnServer.pwd', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=331,
  serialized_end=414,
)


_VIDEOCALLREQUEST = _descriptor.Descriptor(
  name='VideoCallRequest',
  full_name='video_call.VideoCallRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='client_id', full_name='video_call.VideoCallRequest.client_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='group_id', full_name='video_call.VideoCallRequest.group_id', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='call_type', full_name='video_call.VideoCallRequest.call_type', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=416,
  serialized_end=490,
)


_WORKSPACEVIDEOCALLREQUEST = _descriptor.Descriptor(
  name='WorkspaceVideoCallRequest',
  full_name='video_call.WorkspaceVideoCallRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='from_client_id', full_name='video_call.WorkspaceVideoCallRequest.from_client_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='from_client_name', full_name='video_call.WorkspaceVideoCallRequest.from_client_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='from_client_avatar', full_name='video_call.WorkspaceVideoCallRequest.from_client_avatar', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='from_client_workspace_domain', full_name='video_call.WorkspaceVideoCallRequest.from_client_workspace_domain', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='client_id', full_name='video_call.WorkspaceVideoCallRequest.client_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='group_id', full_name='video_call.WorkspaceVideoCallRequest.group_id', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='call_type', full_name='video_call.WorkspaceVideoCallRequest.call_type', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=493,
  serialized_end=692,
)


_UPDATECALLREQUEST = _descriptor.Descriptor(
  name='UpdateCallRequest',
  full_name='video_call.UpdateCallRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='group_id', full_name='video_call.UpdateCallRequest.group_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='update_type', full_name='video_call.UpdateCallRequest.update_type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=694,
  serialized_end=752,
)

_BASERESPONSE.fields_by_name['errors'].message_type = _ERRORRES
_SERVERRESPONSE.fields_by_name['stun_server'].message_type = _STUNSERVER
_SERVERRESPONSE.fields_by_name['turn_server'].message_type = _TURNSERVER
DESCRIPTOR.message_types_by_name['ErrorRes'] = _ERRORRES
DESCRIPTOR.message_types_by_name['BaseResponse'] = _BASERESPONSE
DESCRIPTOR.message_types_by_name['ServerResponse'] = _SERVERRESPONSE
DESCRIPTOR.message_types_by_name['StunServer'] = _STUNSERVER
DESCRIPTOR.message_types_by_name['TurnServer'] = _TURNSERVER
DESCRIPTOR.message_types_by_name['VideoCallRequest'] = _VIDEOCALLREQUEST
DESCRIPTOR.message_types_by_name['WorkspaceVideoCallRequest'] = _WORKSPACEVIDEOCALLREQUEST
DESCRIPTOR.message_types_by_name['UpdateCallRequest'] = _UPDATECALLREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ErrorRes = _reflection.GeneratedProtocolMessageType('ErrorRes', (_message.Message,), {
  'DESCRIPTOR' : _ERRORRES,
  '__module__' : 'protos.video_call_pb2'
  # @@protoc_insertion_point(class_scope:video_call.ErrorRes)
  })
_sym_db.RegisterMessage(ErrorRes)

BaseResponse = _reflection.GeneratedProtocolMessageType('BaseResponse', (_message.Message,), {
  'DESCRIPTOR' : _BASERESPONSE,
  '__module__' : 'protos.video_call_pb2'
  # @@protoc_insertion_point(class_scope:video_call.BaseResponse)
  })
_sym_db.RegisterMessage(BaseResponse)

ServerResponse = _reflection.GeneratedProtocolMessageType('ServerResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERRESPONSE,
  '__module__' : 'protos.video_call_pb2'
  # @@protoc_insertion_point(class_scope:video_call.ServerResponse)
  })
_sym_db.RegisterMessage(ServerResponse)

StunServer = _reflection.GeneratedProtocolMessageType('StunServer', (_message.Message,), {
  'DESCRIPTOR' : _STUNSERVER,
  '__module__' : 'protos.video_call_pb2'
  # @@protoc_insertion_point(class_scope:video_call.StunServer)
  })
_sym_db.RegisterMessage(StunServer)

TurnServer = _reflection.GeneratedProtocolMessageType('TurnServer', (_message.Message,), {
  'DESCRIPTOR' : _TURNSERVER,
  '__module__' : 'protos.video_call_pb2'
  # @@protoc_insertion_point(class_scope:video_call.TurnServer)
  })
_sym_db.RegisterMessage(TurnServer)

VideoCallRequest = _reflection.GeneratedProtocolMessageType('VideoCallRequest', (_message.Message,), {
  'DESCRIPTOR' : _VIDEOCALLREQUEST,
  '__module__' : 'protos.video_call_pb2'
  # @@protoc_insertion_point(class_scope:video_call.VideoCallRequest)
  })
_sym_db.RegisterMessage(VideoCallRequest)

WorkspaceVideoCallRequest = _reflection.GeneratedProtocolMessageType('WorkspaceVideoCallRequest', (_message.Message,), {
  'DESCRIPTOR' : _WORKSPACEVIDEOCALLREQUEST,
  '__module__' : 'protos.video_call_pb2'
  # @@protoc_insertion_point(class_scope:video_call.WorkspaceVideoCallRequest)
  })
_sym_db.RegisterMessage(WorkspaceVideoCallRequest)

UpdateCallRequest = _reflection.GeneratedProtocolMessageType('UpdateCallRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATECALLREQUEST,
  '__module__' : 'protos.video_call_pb2'
  # @@protoc_insertion_point(class_scope:video_call.UpdateCallRequest)
  })
_sym_db.RegisterMessage(UpdateCallRequest)



_VIDEOCALL = _descriptor.ServiceDescriptor(
  name='VideoCall',
  full_name='video_call.VideoCall',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=755,
  serialized_end=1086,
  methods=[
  _descriptor.MethodDescriptor(
    name='video_call',
    full_name='video_call.VideoCall.video_call',
    index=0,
    containing_service=None,
    input_type=_VIDEOCALLREQUEST,
    output_type=_SERVERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='cancel_request_call',
    full_name='video_call.VideoCall.cancel_request_call',
    index=1,
    containing_service=None,
    input_type=_VIDEOCALLREQUEST,
    output_type=_BASERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='update_call',
    full_name='video_call.VideoCall.update_call',
    index=2,
    containing_service=None,
    input_type=_UPDATECALLREQUEST,
    output_type=_BASERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='workspace_video_call',
    full_name='video_call.VideoCall.workspace_video_call',
    index=3,
    containing_service=None,
    input_type=_WORKSPACEVIDEOCALLREQUEST,
    output_type=_SERVERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_VIDEOCALL)

DESCRIPTOR.services_by_name['VideoCall'] = _VIDEOCALL

# @@protoc_insertion_point(module_scope)
