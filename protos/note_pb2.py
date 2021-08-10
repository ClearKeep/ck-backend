# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/note.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protos/note.proto',
  package='note',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11protos/note.proto\x12\x04note\")\n\x08\x45rrorRes\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x03\x12\x0f\n\x07message\x18\x02 \x01(\t\"?\n\x0c\x42\x61seResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x1e\n\x06\x65rrors\x18\x02 \x01(\x0b\x32\x0e.note.ErrorRes\"F\n\x11\x43reateNoteRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\x12\x11\n\tnote_type\x18\x03 \x01(\t\"U\n\x0f\x45\x64itNoteRequest\x12\x0f\n\x07note_id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\x0c\x12\x11\n\tnote_type\x18\x04 \x01(\t\"$\n\x11\x44\x65leteNoteRequest\x12\x0f\n\x07note_id\x18\x01 \x01(\t\"\x07\n\x05\x45mpty\"e\n\x10UserNoteResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\x0c\x12\x11\n\tnote_type\x18\x04 \x01(\t\x12\x12\n\ncreated_at\x18\x05 \x01(\x03\"\x15\n\x13GetUserNotesRequest\"m\n\x14GetUserNotesResponse\x12*\n\nuser_notes\x18\x01 \x03(\x0b\x32\x16.note.UserNoteResponse\x12)\n\rbase_response\x18\x02 \x01(\x0b\x32\x12.note.BaseResponse2\x83\x02\n\x04Note\x12>\n\x0b\x63reate_note\x12\x17.note.CreateNoteRequest\x1a\x16.note.UserNoteResponse\x12\x36\n\tedit_note\x12\x15.note.EditNoteRequest\x1a\x12.note.BaseResponse\x12:\n\x0b\x64\x65lete_note\x12\x17.note.DeleteNoteRequest\x1a\x12.note.BaseResponse\x12G\n\x0eget_user_notes\x12\x19.note.GetUserNotesRequest\x1a\x1a.note.GetUserNotesResponseb\x06proto3'
)




_ERRORRES = _descriptor.Descriptor(
  name='ErrorRes',
  full_name='note.ErrorRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='note.ErrorRes.code', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='note.ErrorRes.message', index=1,
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
  serialized_start=27,
  serialized_end=68,
)


_BASERESPONSE = _descriptor.Descriptor(
  name='BaseResponse',
  full_name='note.BaseResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='note.BaseResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='errors', full_name='note.BaseResponse.errors', index=1,
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
  serialized_start=70,
  serialized_end=133,
)


_CREATENOTEREQUEST = _descriptor.Descriptor(
  name='CreateNoteRequest',
  full_name='note.CreateNoteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='note.CreateNoteRequest.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='content', full_name='note.CreateNoteRequest.content', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='note_type', full_name='note.CreateNoteRequest.note_type', index=2,
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
  serialized_start=135,
  serialized_end=205,
)


_EDITNOTEREQUEST = _descriptor.Descriptor(
  name='EditNoteRequest',
  full_name='note.EditNoteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='note_id', full_name='note.EditNoteRequest.note_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='title', full_name='note.EditNoteRequest.title', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='content', full_name='note.EditNoteRequest.content', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='note_type', full_name='note.EditNoteRequest.note_type', index=3,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_start=207,
  serialized_end=292,
)


_DELETENOTEREQUEST = _descriptor.Descriptor(
  name='DeleteNoteRequest',
  full_name='note.DeleteNoteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='note_id', full_name='note.DeleteNoteRequest.note_id', index=0,
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
  serialized_start=294,
  serialized_end=330,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='note.Empty',
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
  serialized_start=332,
  serialized_end=339,
)


_USERNOTERESPONSE = _descriptor.Descriptor(
  name='UserNoteResponse',
  full_name='note.UserNoteResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='note.UserNoteResponse.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='title', full_name='note.UserNoteResponse.title', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='content', full_name='note.UserNoteResponse.content', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='note_type', full_name='note.UserNoteResponse.note_type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='note.UserNoteResponse.created_at', index=4,
      number=5, type=3, cpp_type=2, label=1,
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
  serialized_start=341,
  serialized_end=442,
)


_GETUSERNOTESREQUEST = _descriptor.Descriptor(
  name='GetUserNotesRequest',
  full_name='note.GetUserNotesRequest',
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
  serialized_start=444,
  serialized_end=465,
)


_GETUSERNOTESRESPONSE = _descriptor.Descriptor(
  name='GetUserNotesResponse',
  full_name='note.GetUserNotesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_notes', full_name='note.GetUserNotesResponse.user_notes', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='base_response', full_name='note.GetUserNotesResponse.base_response', index=1,
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
  serialized_start=467,
  serialized_end=576,
)

_BASERESPONSE.fields_by_name['errors'].message_type = _ERRORRES
_GETUSERNOTESRESPONSE.fields_by_name['user_notes'].message_type = _USERNOTERESPONSE
_GETUSERNOTESRESPONSE.fields_by_name['base_response'].message_type = _BASERESPONSE
DESCRIPTOR.message_types_by_name['ErrorRes'] = _ERRORRES
DESCRIPTOR.message_types_by_name['BaseResponse'] = _BASERESPONSE
DESCRIPTOR.message_types_by_name['CreateNoteRequest'] = _CREATENOTEREQUEST
DESCRIPTOR.message_types_by_name['EditNoteRequest'] = _EDITNOTEREQUEST
DESCRIPTOR.message_types_by_name['DeleteNoteRequest'] = _DELETENOTEREQUEST
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['UserNoteResponse'] = _USERNOTERESPONSE
DESCRIPTOR.message_types_by_name['GetUserNotesRequest'] = _GETUSERNOTESREQUEST
DESCRIPTOR.message_types_by_name['GetUserNotesResponse'] = _GETUSERNOTESRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ErrorRes = _reflection.GeneratedProtocolMessageType('ErrorRes', (_message.Message,), {
  'DESCRIPTOR' : _ERRORRES,
  '__module__' : 'protos.note_pb2'
  # @@protoc_insertion_point(class_scope:note.ErrorRes)
  })
_sym_db.RegisterMessage(ErrorRes)

BaseResponse = _reflection.GeneratedProtocolMessageType('BaseResponse', (_message.Message,), {
  'DESCRIPTOR' : _BASERESPONSE,
  '__module__' : 'protos.note_pb2'
  # @@protoc_insertion_point(class_scope:note.BaseResponse)
  })
_sym_db.RegisterMessage(BaseResponse)

CreateNoteRequest = _reflection.GeneratedProtocolMessageType('CreateNoteRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATENOTEREQUEST,
  '__module__' : 'protos.note_pb2'
  # @@protoc_insertion_point(class_scope:note.CreateNoteRequest)
  })
_sym_db.RegisterMessage(CreateNoteRequest)

EditNoteRequest = _reflection.GeneratedProtocolMessageType('EditNoteRequest', (_message.Message,), {
  'DESCRIPTOR' : _EDITNOTEREQUEST,
  '__module__' : 'protos.note_pb2'
  # @@protoc_insertion_point(class_scope:note.EditNoteRequest)
  })
_sym_db.RegisterMessage(EditNoteRequest)

DeleteNoteRequest = _reflection.GeneratedProtocolMessageType('DeleteNoteRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETENOTEREQUEST,
  '__module__' : 'protos.note_pb2'
  # @@protoc_insertion_point(class_scope:note.DeleteNoteRequest)
  })
_sym_db.RegisterMessage(DeleteNoteRequest)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'protos.note_pb2'
  # @@protoc_insertion_point(class_scope:note.Empty)
  })
_sym_db.RegisterMessage(Empty)

UserNoteResponse = _reflection.GeneratedProtocolMessageType('UserNoteResponse', (_message.Message,), {
  'DESCRIPTOR' : _USERNOTERESPONSE,
  '__module__' : 'protos.note_pb2'
  # @@protoc_insertion_point(class_scope:note.UserNoteResponse)
  })
_sym_db.RegisterMessage(UserNoteResponse)

GetUserNotesRequest = _reflection.GeneratedProtocolMessageType('GetUserNotesRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERNOTESREQUEST,
  '__module__' : 'protos.note_pb2'
  # @@protoc_insertion_point(class_scope:note.GetUserNotesRequest)
  })
_sym_db.RegisterMessage(GetUserNotesRequest)

GetUserNotesResponse = _reflection.GeneratedProtocolMessageType('GetUserNotesResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERNOTESRESPONSE,
  '__module__' : 'protos.note_pb2'
  # @@protoc_insertion_point(class_scope:note.GetUserNotesResponse)
  })
_sym_db.RegisterMessage(GetUserNotesResponse)



_NOTE = _descriptor.ServiceDescriptor(
  name='Note',
  full_name='note.Note',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=579,
  serialized_end=838,
  methods=[
  _descriptor.MethodDescriptor(
    name='create_note',
    full_name='note.Note.create_note',
    index=0,
    containing_service=None,
    input_type=_CREATENOTEREQUEST,
    output_type=_USERNOTERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='edit_note',
    full_name='note.Note.edit_note',
    index=1,
    containing_service=None,
    input_type=_EDITNOTEREQUEST,
    output_type=_BASERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='delete_note',
    full_name='note.Note.delete_note',
    index=2,
    containing_service=None,
    input_type=_DELETENOTEREQUEST,
    output_type=_BASERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_user_notes',
    full_name='note.Note.get_user_notes',
    index=3,
    containing_service=None,
    input_type=_GETUSERNOTESREQUEST,
    output_type=_GETUSERNOTESRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_NOTE)

DESCRIPTOR.services_by_name['Note'] = _NOTE

# @@protoc_insertion_point(module_scope)