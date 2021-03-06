# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/message.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protos/message.proto',
  package='message',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x14protos/message.proto\x12\x07message\"\xe1\x01\n\x15MessageObjectResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08group_id\x18\x02 \x01(\x03\x12\x12\n\ngroup_type\x18\x03 \x01(\t\x12\x16\n\x0e\x66rom_client_id\x18\x04 \x01(\t\x12\x11\n\tclient_id\x18\x05 \x01(\t\x12\x0f\n\x07message\x18\x06 \x01(\x0c\x12\x32\n\x0flst_client_read\x18\x07 \x03(\x0b\x32\x19.message.ClientReadObject\x12\x12\n\ncreated_at\x18\x08 \x01(\x03\x12\x12\n\nupdated_at\x18\t \x01(\x03\"D\n\x10\x43lientReadObject\x12\n\n\x02id\x18\x01 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x02 \x01(\t\x12\x0e\n\x06\x61vatar\x18\x03 \x01(\t\")\n\x08\x45rrorRes\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x03\x12\x0f\n\x07message\x18\x02 \x01(\t\"B\n\x0c\x42\x61seResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12!\n\x06\x65rrors\x18\x02 \x01(\x0b\x32\x11.message.ErrorRes\"W\n\x19GetMessagesInGroupRequest\x12\x10\n\x08group_id\x18\x01 \x01(\x03\x12\x0f\n\x07off_set\x18\x02 \x01(\x05\x12\x17\n\x0flast_message_at\x18\x03 \x01(\x03\"Q\n\x1aGetMessagesInGroupResponse\x12\x33\n\x0blst_message\x18\x01 \x03(\x0b\x32\x1e.message.MessageObjectResponse\"m\n\x0ePublishRequest\x12\x14\n\x0c\x66romClientId\x18\x01 \x01(\t\x12\x10\n\x08\x63lientId\x18\x02 \x01(\t\x12\x0f\n\x07groupId\x18\x03 \x01(\x03\x12\x11\n\tgroupType\x18\x04 \x01(\t\x12\x0f\n\x07message\x18\x05 \x01(\x0c\"$\n\x10SubscribeRequest\x12\x10\n\x08\x63lientId\x18\x01 \x01(\t\"&\n\x12UnSubscribeRequest\x12\x10\n\x08\x63lientId\x18\x01 \x01(\t\"!\n\rListenRequest\x12\x10\n\x08\x63lientId\x18\x01 \x01(\t\"-\n\x13ReadMessagesRequest\x12\x16\n\x0elst_message_id\x18\x04 \x03(\t2\xbd\x03\n\x07Message\x12\x62\n\x15get_messages_in_group\x12\".message.GetMessagesInGroupRequest\x1a#.message.GetMessagesInGroupResponse\"\x00\x12=\n\tSubscribe\x12\x19.message.SubscribeRequest\x1a\x15.message.BaseResponse\x12\x41\n\x0bUnSubscribe\x12\x1b.message.UnSubscribeRequest\x1a\x15.message.BaseResponse\x12\x42\n\x06Listen\x12\x16.message.ListenRequest\x1a\x1e.message.MessageObjectResponse0\x01\x12\x42\n\x07Publish\x12\x17.message.PublishRequest\x1a\x1e.message.MessageObjectResponse\x12\x44\n\rread_messages\x12\x1c.message.ReadMessagesRequest\x1a\x15.message.BaseResponseb\x06proto3'
)




_MESSAGEOBJECTRESPONSE = _descriptor.Descriptor(
  name='MessageObjectResponse',
  full_name='message.MessageObjectResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='message.MessageObjectResponse.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='group_id', full_name='message.MessageObjectResponse.group_id', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='group_type', full_name='message.MessageObjectResponse.group_type', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='from_client_id', full_name='message.MessageObjectResponse.from_client_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='client_id', full_name='message.MessageObjectResponse.client_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='message.MessageObjectResponse.message', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lst_client_read', full_name='message.MessageObjectResponse.lst_client_read', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='message.MessageObjectResponse.created_at', index=7,
      number=8, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='updated_at', full_name='message.MessageObjectResponse.updated_at', index=8,
      number=9, type=3, cpp_type=2, label=1,
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
  serialized_start=34,
  serialized_end=259,
)


_CLIENTREADOBJECT = _descriptor.Descriptor(
  name='ClientReadObject',
  full_name='message.ClientReadObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='message.ClientReadObject.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='display_name', full_name='message.ClientReadObject.display_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='avatar', full_name='message.ClientReadObject.avatar', index=2,
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
  serialized_start=261,
  serialized_end=329,
)


_ERRORRES = _descriptor.Descriptor(
  name='ErrorRes',
  full_name='message.ErrorRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='message.ErrorRes.code', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='message.ErrorRes.message', index=1,
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
  serialized_start=331,
  serialized_end=372,
)


_BASERESPONSE = _descriptor.Descriptor(
  name='BaseResponse',
  full_name='message.BaseResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='message.BaseResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='errors', full_name='message.BaseResponse.errors', index=1,
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
  serialized_start=374,
  serialized_end=440,
)


_GETMESSAGESINGROUPREQUEST = _descriptor.Descriptor(
  name='GetMessagesInGroupRequest',
  full_name='message.GetMessagesInGroupRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='group_id', full_name='message.GetMessagesInGroupRequest.group_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='off_set', full_name='message.GetMessagesInGroupRequest.off_set', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='last_message_at', full_name='message.GetMessagesInGroupRequest.last_message_at', index=2,
      number=3, type=3, cpp_type=2, label=1,
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
  serialized_start=442,
  serialized_end=529,
)


_GETMESSAGESINGROUPRESPONSE = _descriptor.Descriptor(
  name='GetMessagesInGroupResponse',
  full_name='message.GetMessagesInGroupResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='lst_message', full_name='message.GetMessagesInGroupResponse.lst_message', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=531,
  serialized_end=612,
)


_PUBLISHREQUEST = _descriptor.Descriptor(
  name='PublishRequest',
  full_name='message.PublishRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='fromClientId', full_name='message.PublishRequest.fromClientId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='clientId', full_name='message.PublishRequest.clientId', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='groupId', full_name='message.PublishRequest.groupId', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='groupType', full_name='message.PublishRequest.groupType', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='message.PublishRequest.message', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  serialized_start=614,
  serialized_end=723,
)


_SUBSCRIBEREQUEST = _descriptor.Descriptor(
  name='SubscribeRequest',
  full_name='message.SubscribeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientId', full_name='message.SubscribeRequest.clientId', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=725,
  serialized_end=761,
)


_UNSUBSCRIBEREQUEST = _descriptor.Descriptor(
  name='UnSubscribeRequest',
  full_name='message.UnSubscribeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientId', full_name='message.UnSubscribeRequest.clientId', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=763,
  serialized_end=801,
)


_LISTENREQUEST = _descriptor.Descriptor(
  name='ListenRequest',
  full_name='message.ListenRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientId', full_name='message.ListenRequest.clientId', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=803,
  serialized_end=836,
)


_READMESSAGESREQUEST = _descriptor.Descriptor(
  name='ReadMessagesRequest',
  full_name='message.ReadMessagesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='lst_message_id', full_name='message.ReadMessagesRequest.lst_message_id', index=0,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=838,
  serialized_end=883,
)

_MESSAGEOBJECTRESPONSE.fields_by_name['lst_client_read'].message_type = _CLIENTREADOBJECT
_BASERESPONSE.fields_by_name['errors'].message_type = _ERRORRES
_GETMESSAGESINGROUPRESPONSE.fields_by_name['lst_message'].message_type = _MESSAGEOBJECTRESPONSE
DESCRIPTOR.message_types_by_name['MessageObjectResponse'] = _MESSAGEOBJECTRESPONSE
DESCRIPTOR.message_types_by_name['ClientReadObject'] = _CLIENTREADOBJECT
DESCRIPTOR.message_types_by_name['ErrorRes'] = _ERRORRES
DESCRIPTOR.message_types_by_name['BaseResponse'] = _BASERESPONSE
DESCRIPTOR.message_types_by_name['GetMessagesInGroupRequest'] = _GETMESSAGESINGROUPREQUEST
DESCRIPTOR.message_types_by_name['GetMessagesInGroupResponse'] = _GETMESSAGESINGROUPRESPONSE
DESCRIPTOR.message_types_by_name['PublishRequest'] = _PUBLISHREQUEST
DESCRIPTOR.message_types_by_name['SubscribeRequest'] = _SUBSCRIBEREQUEST
DESCRIPTOR.message_types_by_name['UnSubscribeRequest'] = _UNSUBSCRIBEREQUEST
DESCRIPTOR.message_types_by_name['ListenRequest'] = _LISTENREQUEST
DESCRIPTOR.message_types_by_name['ReadMessagesRequest'] = _READMESSAGESREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MessageObjectResponse = _reflection.GeneratedProtocolMessageType('MessageObjectResponse', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGEOBJECTRESPONSE,
  '__module__' : 'protos.message_pb2'
  # @@protoc_insertion_point(class_scope:message.MessageObjectResponse)
  })
_sym_db.RegisterMessage(MessageObjectResponse)

ClientReadObject = _reflection.GeneratedProtocolMessageType('ClientReadObject', (_message.Message,), {
  'DESCRIPTOR' : _CLIENTREADOBJECT,
  '__module__' : 'protos.message_pb2'
  # @@protoc_insertion_point(class_scope:message.ClientReadObject)
  })
_sym_db.RegisterMessage(ClientReadObject)

ErrorRes = _reflection.GeneratedProtocolMessageType('ErrorRes', (_message.Message,), {
  'DESCRIPTOR' : _ERRORRES,
  '__module__' : 'protos.message_pb2'
  # @@protoc_insertion_point(class_scope:message.ErrorRes)
  })
_sym_db.RegisterMessage(ErrorRes)

BaseResponse = _reflection.GeneratedProtocolMessageType('BaseResponse', (_message.Message,), {
  'DESCRIPTOR' : _BASERESPONSE,
  '__module__' : 'protos.message_pb2'
  # @@protoc_insertion_point(class_scope:message.BaseResponse)
  })
_sym_db.RegisterMessage(BaseResponse)

GetMessagesInGroupRequest = _reflection.GeneratedProtocolMessageType('GetMessagesInGroupRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETMESSAGESINGROUPREQUEST,
  '__module__' : 'protos.message_pb2'
  # @@protoc_insertion_point(class_scope:message.GetMessagesInGroupRequest)
  })
_sym_db.RegisterMessage(GetMessagesInGroupRequest)

GetMessagesInGroupResponse = _reflection.GeneratedProtocolMessageType('GetMessagesInGroupResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETMESSAGESINGROUPRESPONSE,
  '__module__' : 'protos.message_pb2'
  # @@protoc_insertion_point(class_scope:message.GetMessagesInGroupResponse)
  })
_sym_db.RegisterMessage(GetMessagesInGroupResponse)

PublishRequest = _reflection.GeneratedProtocolMessageType('PublishRequest', (_message.Message,), {
  'DESCRIPTOR' : _PUBLISHREQUEST,
  '__module__' : 'protos.message_pb2'
  # @@protoc_insertion_point(class_scope:message.PublishRequest)
  })
_sym_db.RegisterMessage(PublishRequest)

SubscribeRequest = _reflection.GeneratedProtocolMessageType('SubscribeRequest', (_message.Message,), {
  'DESCRIPTOR' : _SUBSCRIBEREQUEST,
  '__module__' : 'protos.message_pb2'
  # @@protoc_insertion_point(class_scope:message.SubscribeRequest)
  })
_sym_db.RegisterMessage(SubscribeRequest)

UnSubscribeRequest = _reflection.GeneratedProtocolMessageType('UnSubscribeRequest', (_message.Message,), {
  'DESCRIPTOR' : _UNSUBSCRIBEREQUEST,
  '__module__' : 'protos.message_pb2'
  # @@protoc_insertion_point(class_scope:message.UnSubscribeRequest)
  })
_sym_db.RegisterMessage(UnSubscribeRequest)

ListenRequest = _reflection.GeneratedProtocolMessageType('ListenRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTENREQUEST,
  '__module__' : 'protos.message_pb2'
  # @@protoc_insertion_point(class_scope:message.ListenRequest)
  })
_sym_db.RegisterMessage(ListenRequest)

ReadMessagesRequest = _reflection.GeneratedProtocolMessageType('ReadMessagesRequest', (_message.Message,), {
  'DESCRIPTOR' : _READMESSAGESREQUEST,
  '__module__' : 'protos.message_pb2'
  # @@protoc_insertion_point(class_scope:message.ReadMessagesRequest)
  })
_sym_db.RegisterMessage(ReadMessagesRequest)



_MESSAGE = _descriptor.ServiceDescriptor(
  name='Message',
  full_name='message.Message',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=886,
  serialized_end=1331,
  methods=[
  _descriptor.MethodDescriptor(
    name='get_messages_in_group',
    full_name='message.Message.get_messages_in_group',
    index=0,
    containing_service=None,
    input_type=_GETMESSAGESINGROUPREQUEST,
    output_type=_GETMESSAGESINGROUPRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Subscribe',
    full_name='message.Message.Subscribe',
    index=1,
    containing_service=None,
    input_type=_SUBSCRIBEREQUEST,
    output_type=_BASERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='UnSubscribe',
    full_name='message.Message.UnSubscribe',
    index=2,
    containing_service=None,
    input_type=_UNSUBSCRIBEREQUEST,
    output_type=_BASERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Listen',
    full_name='message.Message.Listen',
    index=3,
    containing_service=None,
    input_type=_LISTENREQUEST,
    output_type=_MESSAGEOBJECTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Publish',
    full_name='message.Message.Publish',
    index=4,
    containing_service=None,
    input_type=_PUBLISHREQUEST,
    output_type=_MESSAGEOBJECTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='read_messages',
    full_name='message.Message.read_messages',
    index=5,
    containing_service=None,
    input_type=_READMESSAGESREQUEST,
    output_type=_BASERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_MESSAGE)

DESCRIPTOR.services_by_name['Message'] = _MESSAGE

# @@protoc_insertion_point(module_scope)
