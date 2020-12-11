# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/notify.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/notify.proto',
  package='notification',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x12proto/notify.proto\x12\x0cnotification\"\xe1\x01\n\x14NotifyObjectResponse\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x11\n\tclient_id\x18\x02 \x01(\t\x12\x15\n\rref_client_id\x18\x04 \x01(\t\x12\x14\n\x0cref_group_id\x18\x05 \x01(\t\x12\x13\n\x0bnotify_type\x18\x06 \x01(\t\x12\x14\n\x0cnotify_image\x18\x07 \x01(\t\x12\x14\n\x0cnotify_title\x18\x08 \x01(\t\x12\x16\n\x0enotify_content\x18\t \x01(\t\x12\x10\n\x08read_flg\x18\x0b \x01(\x08\x12\x12\n\ncreated_at\x18\x0c \x01(\x03\"\x1f\n\x0c\x42\x61seResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x07\n\x05\x45mpty\"M\n\x13GetNotifiesResponse\x12\x36\n\nlst_notify\x18\x01 \x03(\x0b\x32\".notification.NotifyObjectResponse\"%\n\x10SubscribeRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\"\'\n\x12UnSubscribeRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\"!\n\rListenRequest\x12\x10\n\x08\x63lientId\x18\x01 \x01(\t\"&\n\x11ReadNotifyRequest\x12\x11\n\tnotify_id\x18\x01 \x01(\t2\x87\x03\n\x06Notify\x12J\n\x0bread_notify\x12\x1f.notification.ReadNotifyRequest\x1a\x1a.notification.BaseResponse\x12M\n\x13get_unread_notifies\x12\x13.notification.Empty\x1a!.notification.GetNotifiesResponse\x12G\n\tsubscribe\x12\x1e.notification.SubscribeRequest\x1a\x1a.notification.BaseResponse\x12L\n\x0cun_subscribe\x12 .notification.UnSubscribeRequest\x1a\x1a.notification.BaseResponse\x12K\n\x06listen\x12\x1b.notification.ListenRequest\x1a\".notification.NotifyObjectResponse0\x01\x62\x06proto3'
)




_NOTIFYOBJECTRESPONSE = _descriptor.Descriptor(
  name='NotifyObjectResponse',
  full_name='notification.NotifyObjectResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='notification.NotifyObjectResponse.id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='client_id', full_name='notification.NotifyObjectResponse.client_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ref_client_id', full_name='notification.NotifyObjectResponse.ref_client_id', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ref_group_id', full_name='notification.NotifyObjectResponse.ref_group_id', index=3,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='notify_type', full_name='notification.NotifyObjectResponse.notify_type', index=4,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='notify_image', full_name='notification.NotifyObjectResponse.notify_image', index=5,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='notify_title', full_name='notification.NotifyObjectResponse.notify_title', index=6,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='notify_content', full_name='notification.NotifyObjectResponse.notify_content', index=7,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='read_flg', full_name='notification.NotifyObjectResponse.read_flg', index=8,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='notification.NotifyObjectResponse.created_at', index=9,
      number=12, type=3, cpp_type=2, label=1,
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
  serialized_start=37,
  serialized_end=262,
)


_BASERESPONSE = _descriptor.Descriptor(
  name='BaseResponse',
  full_name='notification.BaseResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='notification.BaseResponse.success', index=0,
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
  serialized_start=264,
  serialized_end=295,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='notification.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=297,
  serialized_end=304,
)


_GETNOTIFIESRESPONSE = _descriptor.Descriptor(
  name='GetNotifiesResponse',
  full_name='notification.GetNotifiesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='lst_notify', full_name='notification.GetNotifiesResponse.lst_notify', index=0,
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
  serialized_start=306,
  serialized_end=383,
)


_SUBSCRIBEREQUEST = _descriptor.Descriptor(
  name='SubscribeRequest',
  full_name='notification.SubscribeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='client_id', full_name='notification.SubscribeRequest.client_id', index=0,
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
  serialized_start=385,
  serialized_end=422,
)


_UNSUBSCRIBEREQUEST = _descriptor.Descriptor(
  name='UnSubscribeRequest',
  full_name='notification.UnSubscribeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='client_id', full_name='notification.UnSubscribeRequest.client_id', index=0,
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
  serialized_start=424,
  serialized_end=463,
)


_LISTENREQUEST = _descriptor.Descriptor(
  name='ListenRequest',
  full_name='notification.ListenRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientId', full_name='notification.ListenRequest.clientId', index=0,
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
  serialized_start=465,
  serialized_end=498,
)


_READNOTIFYREQUEST = _descriptor.Descriptor(
  name='ReadNotifyRequest',
  full_name='notification.ReadNotifyRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='notify_id', full_name='notification.ReadNotifyRequest.notify_id', index=0,
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
  serialized_start=500,
  serialized_end=538,
)

_GETNOTIFIESRESPONSE.fields_by_name['lst_notify'].message_type = _NOTIFYOBJECTRESPONSE
DESCRIPTOR.message_types_by_name['NotifyObjectResponse'] = _NOTIFYOBJECTRESPONSE
DESCRIPTOR.message_types_by_name['BaseResponse'] = _BASERESPONSE
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['GetNotifiesResponse'] = _GETNOTIFIESRESPONSE
DESCRIPTOR.message_types_by_name['SubscribeRequest'] = _SUBSCRIBEREQUEST
DESCRIPTOR.message_types_by_name['UnSubscribeRequest'] = _UNSUBSCRIBEREQUEST
DESCRIPTOR.message_types_by_name['ListenRequest'] = _LISTENREQUEST
DESCRIPTOR.message_types_by_name['ReadNotifyRequest'] = _READNOTIFYREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NotifyObjectResponse = _reflection.GeneratedProtocolMessageType('NotifyObjectResponse', (_message.Message,), {
  'DESCRIPTOR' : _NOTIFYOBJECTRESPONSE,
  '__module__' : 'proto.notify_pb2'
  # @@protoc_insertion_point(class_scope:notification.NotifyObjectResponse)
  })
_sym_db.RegisterMessage(NotifyObjectResponse)

BaseResponse = _reflection.GeneratedProtocolMessageType('BaseResponse', (_message.Message,), {
  'DESCRIPTOR' : _BASERESPONSE,
  '__module__' : 'proto.notify_pb2'
  # @@protoc_insertion_point(class_scope:notification.BaseResponse)
  })
_sym_db.RegisterMessage(BaseResponse)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'proto.notify_pb2'
  # @@protoc_insertion_point(class_scope:notification.Empty)
  })
_sym_db.RegisterMessage(Empty)

GetNotifiesResponse = _reflection.GeneratedProtocolMessageType('GetNotifiesResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETNOTIFIESRESPONSE,
  '__module__' : 'proto.notify_pb2'
  # @@protoc_insertion_point(class_scope:notification.GetNotifiesResponse)
  })
_sym_db.RegisterMessage(GetNotifiesResponse)

SubscribeRequest = _reflection.GeneratedProtocolMessageType('SubscribeRequest', (_message.Message,), {
  'DESCRIPTOR' : _SUBSCRIBEREQUEST,
  '__module__' : 'proto.notify_pb2'
  # @@protoc_insertion_point(class_scope:notification.SubscribeRequest)
  })
_sym_db.RegisterMessage(SubscribeRequest)

UnSubscribeRequest = _reflection.GeneratedProtocolMessageType('UnSubscribeRequest', (_message.Message,), {
  'DESCRIPTOR' : _UNSUBSCRIBEREQUEST,
  '__module__' : 'proto.notify_pb2'
  # @@protoc_insertion_point(class_scope:notification.UnSubscribeRequest)
  })
_sym_db.RegisterMessage(UnSubscribeRequest)

ListenRequest = _reflection.GeneratedProtocolMessageType('ListenRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTENREQUEST,
  '__module__' : 'proto.notify_pb2'
  # @@protoc_insertion_point(class_scope:notification.ListenRequest)
  })
_sym_db.RegisterMessage(ListenRequest)

ReadNotifyRequest = _reflection.GeneratedProtocolMessageType('ReadNotifyRequest', (_message.Message,), {
  'DESCRIPTOR' : _READNOTIFYREQUEST,
  '__module__' : 'proto.notify_pb2'
  # @@protoc_insertion_point(class_scope:notification.ReadNotifyRequest)
  })
_sym_db.RegisterMessage(ReadNotifyRequest)



_NOTIFY = _descriptor.ServiceDescriptor(
  name='Notify',
  full_name='notification.Notify',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=541,
  serialized_end=932,
  methods=[
  _descriptor.MethodDescriptor(
    name='read_notify',
    full_name='notification.Notify.read_notify',
    index=0,
    containing_service=None,
    input_type=_READNOTIFYREQUEST,
    output_type=_BASERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_unread_notifies',
    full_name='notification.Notify.get_unread_notifies',
    index=1,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_GETNOTIFIESRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='subscribe',
    full_name='notification.Notify.subscribe',
    index=2,
    containing_service=None,
    input_type=_SUBSCRIBEREQUEST,
    output_type=_BASERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='un_subscribe',
    full_name='notification.Notify.un_subscribe',
    index=3,
    containing_service=None,
    input_type=_UNSUBSCRIBEREQUEST,
    output_type=_BASERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='listen',
    full_name='notification.Notify.listen',
    index=4,
    containing_service=None,
    input_type=_LISTENREQUEST,
    output_type=_NOTIFYOBJECTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_NOTIFY)

DESCRIPTOR.services_by_name['Notify'] = _NOTIFY

# @@protoc_insertion_point(module_scope)
