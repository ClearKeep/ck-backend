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
  serialized_pb=b'\n\x17protos/video_call.proto\x12\nvideo_call\"\x1f\n\x0c\x42\x61seResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"7\n\x10VideoCallRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x10\n\x08group_id\x18\x02 \x01(\x03\x32S\n\tVideoCall\x12\x46\n\nvideo_call\x12\x1c.video_call.VideoCallRequest\x1a\x18.video_call.BaseResponse\"\x00\x62\x06proto3'
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
  serialized_end=70,
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
  serialized_start=72,
  serialized_end=127,
)

DESCRIPTOR.message_types_by_name['BaseResponse'] = _BASERESPONSE
DESCRIPTOR.message_types_by_name['VideoCallRequest'] = _VIDEOCALLREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BaseResponse = _reflection.GeneratedProtocolMessageType('BaseResponse', (_message.Message,), {
  'DESCRIPTOR' : _BASERESPONSE,
  '__module__' : 'protos.video_call_pb2'
  # @@protoc_insertion_point(class_scope:video_call.BaseResponse)
  })
_sym_db.RegisterMessage(BaseResponse)

VideoCallRequest = _reflection.GeneratedProtocolMessageType('VideoCallRequest', (_message.Message,), {
  'DESCRIPTOR' : _VIDEOCALLREQUEST,
  '__module__' : 'protos.video_call_pb2'
  # @@protoc_insertion_point(class_scope:video_call.VideoCallRequest)
  })
_sym_db.RegisterMessage(VideoCallRequest)



_VIDEOCALL = _descriptor.ServiceDescriptor(
  name='VideoCall',
  full_name='video_call.VideoCall',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=129,
  serialized_end=212,
  methods=[
  _descriptor.MethodDescriptor(
    name='video_call',
    full_name='video_call.VideoCall.video_call',
    index=0,
    containing_service=None,
    input_type=_VIDEOCALLREQUEST,
    output_type=_BASERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_VIDEOCALL)

DESCRIPTOR.services_by_name['VideoCall'] = _VIDEOCALL

# @@protoc_insertion_point(module_scope)