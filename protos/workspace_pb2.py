# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/workspace.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protos/workspace.proto',
  package='workspace',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16protos/workspace.proto\x12\tworkspace\")\n\x08\x45rrorRes\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x03\x12\x0f\n\x07message\x18\x02 \x01(\t\"D\n\x0c\x42\x61seResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12#\n\x06\x65rrors\x18\x02 \x01(\x0b\x32\x13.workspace.ErrorRes\"`\n\x14WorkspaceInfoRequest\x12\x18\n\x10workspace_domain\x18\x01 \x01(\t\x12.\n\rbase_response\x18\x02 \x01(\x0b\x32\x17.workspace.BaseResponse\"Q\n\x17WorkspaceObjectResponse\x12\x18\n\x10workspace_domain\x18\x01 \x01(\t\x12\x1c\n\x14is_default_workspace\x18\x02 \x01(\x08\"\x17\n\x15LeaveWorkspaceRequest2\xb4\x01\n\tWorkspace\x12W\n\x0eworkspace_info\x12\x1f.workspace.WorkspaceInfoRequest\x1a\".workspace.WorkspaceObjectResponse\"\x00\x12N\n\x0fleave_workspace\x12 .workspace.LeaveWorkspaceRequest\x1a\x17.workspace.BaseResponse\"\x00\x62\x06proto3'
)




_ERRORRES = _descriptor.Descriptor(
  name='ErrorRes',
  full_name='workspace.ErrorRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='workspace.ErrorRes.code', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='workspace.ErrorRes.message', index=1,
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
  serialized_start=37,
  serialized_end=78,
)


_BASERESPONSE = _descriptor.Descriptor(
  name='BaseResponse',
  full_name='workspace.BaseResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='workspace.BaseResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='errors', full_name='workspace.BaseResponse.errors', index=1,
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
  serialized_start=80,
  serialized_end=148,
)


_WORKSPACEINFOREQUEST = _descriptor.Descriptor(
  name='WorkspaceInfoRequest',
  full_name='workspace.WorkspaceInfoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='workspace_domain', full_name='workspace.WorkspaceInfoRequest.workspace_domain', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='base_response', full_name='workspace.WorkspaceInfoRequest.base_response', index=1,
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
  serialized_start=150,
  serialized_end=246,
)


_WORKSPACEOBJECTRESPONSE = _descriptor.Descriptor(
  name='WorkspaceObjectResponse',
  full_name='workspace.WorkspaceObjectResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='workspace_domain', full_name='workspace.WorkspaceObjectResponse.workspace_domain', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='is_default_workspace', full_name='workspace.WorkspaceObjectResponse.is_default_workspace', index=1,
      number=2, type=8, cpp_type=7, label=1,
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
  serialized_start=248,
  serialized_end=329,
)


_LEAVEWORKSPACEREQUEST = _descriptor.Descriptor(
  name='LeaveWorkspaceRequest',
  full_name='workspace.LeaveWorkspaceRequest',
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
  serialized_start=331,
  serialized_end=354,
)

_BASERESPONSE.fields_by_name['errors'].message_type = _ERRORRES
_WORKSPACEINFOREQUEST.fields_by_name['base_response'].message_type = _BASERESPONSE
DESCRIPTOR.message_types_by_name['ErrorRes'] = _ERRORRES
DESCRIPTOR.message_types_by_name['BaseResponse'] = _BASERESPONSE
DESCRIPTOR.message_types_by_name['WorkspaceInfoRequest'] = _WORKSPACEINFOREQUEST
DESCRIPTOR.message_types_by_name['WorkspaceObjectResponse'] = _WORKSPACEOBJECTRESPONSE
DESCRIPTOR.message_types_by_name['LeaveWorkspaceRequest'] = _LEAVEWORKSPACEREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ErrorRes = _reflection.GeneratedProtocolMessageType('ErrorRes', (_message.Message,), {
  'DESCRIPTOR' : _ERRORRES,
  '__module__' : 'protos.workspace_pb2'
  # @@protoc_insertion_point(class_scope:workspace.ErrorRes)
  })
_sym_db.RegisterMessage(ErrorRes)

BaseResponse = _reflection.GeneratedProtocolMessageType('BaseResponse', (_message.Message,), {
  'DESCRIPTOR' : _BASERESPONSE,
  '__module__' : 'protos.workspace_pb2'
  # @@protoc_insertion_point(class_scope:workspace.BaseResponse)
  })
_sym_db.RegisterMessage(BaseResponse)

WorkspaceInfoRequest = _reflection.GeneratedProtocolMessageType('WorkspaceInfoRequest', (_message.Message,), {
  'DESCRIPTOR' : _WORKSPACEINFOREQUEST,
  '__module__' : 'protos.workspace_pb2'
  # @@protoc_insertion_point(class_scope:workspace.WorkspaceInfoRequest)
  })
_sym_db.RegisterMessage(WorkspaceInfoRequest)

WorkspaceObjectResponse = _reflection.GeneratedProtocolMessageType('WorkspaceObjectResponse', (_message.Message,), {
  'DESCRIPTOR' : _WORKSPACEOBJECTRESPONSE,
  '__module__' : 'protos.workspace_pb2'
  # @@protoc_insertion_point(class_scope:workspace.WorkspaceObjectResponse)
  })
_sym_db.RegisterMessage(WorkspaceObjectResponse)

LeaveWorkspaceRequest = _reflection.GeneratedProtocolMessageType('LeaveWorkspaceRequest', (_message.Message,), {
  'DESCRIPTOR' : _LEAVEWORKSPACEREQUEST,
  '__module__' : 'protos.workspace_pb2'
  # @@protoc_insertion_point(class_scope:workspace.LeaveWorkspaceRequest)
  })
_sym_db.RegisterMessage(LeaveWorkspaceRequest)



_WORKSPACE = _descriptor.ServiceDescriptor(
  name='Workspace',
  full_name='workspace.Workspace',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=357,
  serialized_end=537,
  methods=[
  _descriptor.MethodDescriptor(
    name='workspace_info',
    full_name='workspace.Workspace.workspace_info',
    index=0,
    containing_service=None,
    input_type=_WORKSPACEINFOREQUEST,
    output_type=_WORKSPACEOBJECTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='leave_workspace',
    full_name='workspace.Workspace.leave_workspace',
    index=1,
    containing_service=None,
    input_type=_LEAVEWORKSPACEREQUEST,
    output_type=_BASERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_WORKSPACE)

DESCRIPTOR.services_by_name['Workspace'] = _WORKSPACE

# @@protoc_insertion_point(module_scope)
