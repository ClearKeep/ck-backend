# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/upload_file.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protos/upload_file.proto',
  package='upload_file',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x18protos/upload_file.proto\x12\x0bupload_file\")\n\x08\x45rrorRes\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x03\x12\x0f\n\x07message\x18\x02 \x01(\t\"F\n\x0c\x42\x61seResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12%\n\x06\x65rrors\x18\x02 \x01(\x0b\x32\x15.upload_file.ErrorRes\"g\n\x11\x46ileUploadRequest\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x19\n\x11\x66ile_content_type\x18\x02 \x01(\t\x12\x11\n\tfile_data\x18\x03 \x01(\x0c\x12\x11\n\tfile_hash\x18\x04 \x01(\t\"\x8e\x01\n\x14\x46ileDataBlockRequest\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x19\n\x11\x66ile_content_type\x18\x02 \x01(\t\x12\x17\n\x0f\x66ile_data_block\x18\x03 \x01(\x0c\x12\x1c\n\x14\x66ile_data_block_hash\x18\x04 \x01(\t\x12\x11\n\tfile_hash\x18\x05 \x01(\t\"\'\n\x13UploadFilesResponse\x12\x10\n\x08\x66ile_url\x18\x01 \x01(\t2\x93\x02\n\nUploadFile\x12R\n\x0cupload_image\x12\x1e.upload_file.FileUploadRequest\x1a .upload_file.UploadFilesResponse\"\x00\x12Q\n\x0bupload_file\x12\x1e.upload_file.FileUploadRequest\x1a .upload_file.UploadFilesResponse\"\x00\x12^\n\x13upload_chunked_file\x12!.upload_file.FileDataBlockRequest\x1a .upload_file.UploadFilesResponse\"\x00(\x01\x62\x06proto3'
)




_ERRORRES = _descriptor.Descriptor(
  name='ErrorRes',
  full_name='upload_file.ErrorRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='upload_file.ErrorRes.code', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='upload_file.ErrorRes.message', index=1,
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
  serialized_start=41,
  serialized_end=82,
)


_BASERESPONSE = _descriptor.Descriptor(
  name='BaseResponse',
  full_name='upload_file.BaseResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='upload_file.BaseResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='errors', full_name='upload_file.BaseResponse.errors', index=1,
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
  serialized_start=84,
  serialized_end=154,
)


_FILEUPLOADREQUEST = _descriptor.Descriptor(
  name='FileUploadRequest',
  full_name='upload_file.FileUploadRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_name', full_name='upload_file.FileUploadRequest.file_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file_content_type', full_name='upload_file.FileUploadRequest.file_content_type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file_data', full_name='upload_file.FileUploadRequest.file_data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file_hash', full_name='upload_file.FileUploadRequest.file_hash', index=3,
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
  serialized_start=156,
  serialized_end=259,
)


_FILEDATABLOCKREQUEST = _descriptor.Descriptor(
  name='FileDataBlockRequest',
  full_name='upload_file.FileDataBlockRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_name', full_name='upload_file.FileDataBlockRequest.file_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file_content_type', full_name='upload_file.FileDataBlockRequest.file_content_type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file_data_block', full_name='upload_file.FileDataBlockRequest.file_data_block', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file_data_block_hash', full_name='upload_file.FileDataBlockRequest.file_data_block_hash', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file_hash', full_name='upload_file.FileDataBlockRequest.file_hash', index=4,
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
  serialized_start=262,
  serialized_end=404,
)


_UPLOADFILESRESPONSE = _descriptor.Descriptor(
  name='UploadFilesResponse',
  full_name='upload_file.UploadFilesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_url', full_name='upload_file.UploadFilesResponse.file_url', index=0,
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
  serialized_start=406,
  serialized_end=445,
)

_BASERESPONSE.fields_by_name['errors'].message_type = _ERRORRES
DESCRIPTOR.message_types_by_name['ErrorRes'] = _ERRORRES
DESCRIPTOR.message_types_by_name['BaseResponse'] = _BASERESPONSE
DESCRIPTOR.message_types_by_name['FileUploadRequest'] = _FILEUPLOADREQUEST
DESCRIPTOR.message_types_by_name['FileDataBlockRequest'] = _FILEDATABLOCKREQUEST
DESCRIPTOR.message_types_by_name['UploadFilesResponse'] = _UPLOADFILESRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ErrorRes = _reflection.GeneratedProtocolMessageType('ErrorRes', (_message.Message,), {
  'DESCRIPTOR' : _ERRORRES,
  '__module__' : 'protos.upload_file_pb2'
  # @@protoc_insertion_point(class_scope:upload_file.ErrorRes)
  })
_sym_db.RegisterMessage(ErrorRes)

BaseResponse = _reflection.GeneratedProtocolMessageType('BaseResponse', (_message.Message,), {
  'DESCRIPTOR' : _BASERESPONSE,
  '__module__' : 'protos.upload_file_pb2'
  # @@protoc_insertion_point(class_scope:upload_file.BaseResponse)
  })
_sym_db.RegisterMessage(BaseResponse)

FileUploadRequest = _reflection.GeneratedProtocolMessageType('FileUploadRequest', (_message.Message,), {
  'DESCRIPTOR' : _FILEUPLOADREQUEST,
  '__module__' : 'protos.upload_file_pb2'
  # @@protoc_insertion_point(class_scope:upload_file.FileUploadRequest)
  })
_sym_db.RegisterMessage(FileUploadRequest)

FileDataBlockRequest = _reflection.GeneratedProtocolMessageType('FileDataBlockRequest', (_message.Message,), {
  'DESCRIPTOR' : _FILEDATABLOCKREQUEST,
  '__module__' : 'protos.upload_file_pb2'
  # @@protoc_insertion_point(class_scope:upload_file.FileDataBlockRequest)
  })
_sym_db.RegisterMessage(FileDataBlockRequest)

UploadFilesResponse = _reflection.GeneratedProtocolMessageType('UploadFilesResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPLOADFILESRESPONSE,
  '__module__' : 'protos.upload_file_pb2'
  # @@protoc_insertion_point(class_scope:upload_file.UploadFilesResponse)
  })
_sym_db.RegisterMessage(UploadFilesResponse)



_UPLOADFILE = _descriptor.ServiceDescriptor(
  name='UploadFile',
  full_name='upload_file.UploadFile',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=448,
  serialized_end=723,
  methods=[
  _descriptor.MethodDescriptor(
    name='upload_image',
    full_name='upload_file.UploadFile.upload_image',
    index=0,
    containing_service=None,
    input_type=_FILEUPLOADREQUEST,
    output_type=_UPLOADFILESRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='upload_file',
    full_name='upload_file.UploadFile.upload_file',
    index=1,
    containing_service=None,
    input_type=_FILEUPLOADREQUEST,
    output_type=_UPLOADFILESRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='upload_chunked_file',
    full_name='upload_file.UploadFile.upload_chunked_file',
    index=2,
    containing_service=None,
    input_type=_FILEDATABLOCKREQUEST,
    output_type=_UPLOADFILESRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_UPLOADFILE)

DESCRIPTOR.services_by_name['UploadFile'] = _UPLOADFILE

# @@protoc_insertion_point(module_scope)