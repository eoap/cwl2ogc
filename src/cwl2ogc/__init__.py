# SPDX-FileCopyrightText: 2025-present Fabrice Brito <fabrice.brito@terradue.com>
#
# SPDX-License-Identifier: MIT

from cwl_utils.parser import load_document_by_yaml
from loguru import logger
from urllib.parse import urlparse
from typing import Any
import cwl_utils
import gzip
import io
import json
import yaml
import requests
import os

class CWLtypes2OGCConverter:

    def on_enum(input):
        pass

    def on_enum_schema(input):
        pass

    def on_array(input):
        pass

    def on_input_array_schema(input):
        pass

    def on_input_parameter(input):
        pass

    def on_input_parameter(input):
        pass

    def on_input(input):
        pass

    def on_list(input):
        pass

    def on_record(input):
        pass

    def on_record_schema(input):
        pass

class BaseCWLtypes2OGCConverter(CWLtypes2OGCConverter):

    STRING_FORMAT_URL = 'https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml'

    STRING_FORMATS = {
        'Date': "date",
        'DateTime': "date-time",
        'Duration': "duration",
        'Email': "email",
        'Hostname': "hostname",
        'IDNEmail': "idn-email",
        'IDNHostname': "idn-hostname",
        'IPv4': "ipv4",
        'IPv6': "ipv6",
        'IRI': "iri",
        'IRIReference': "iri-reference",
        'JsonPointer': "json-pointer",
        'Password': "password",
        'RelativeJsonPointer': "relative-json-pointer",
        'UUID': "uuid",
        'URI': "uri",
        'URIReference': "uri-reference",
        'URITemplate': "uri-template",
        'Time': "time"
    }

    CWL_TYPES = {}

    def __init__(self, cwl):
        self.cwl = cwl

        self.CWL_TYPES["int"] = lambda input : { "type": "integer" }
        self.CWL_TYPES["double"] = lambda input : { "type": "number", "format": "double" }
        self.CWL_TYPES["float"] = lambda input : { "type": "number", "format": "float" }
        self.CWL_TYPES["boolean"] = lambda input : { "type": "boolean" }
        self.CWL_TYPES["string"] = lambda input : { "type": "string" }
        self.CWL_TYPES["stdout"] = self.CWL_TYPES["string"]

        for typ in ["File",
                    cwl_utils.parser.cwl_v1_0.File,
                    cwl_utils.parser.cwl_v1_1.File,
                    cwl_utils.parser.cwl_v1_2.File,
                    "Directory",
                    cwl_utils.parser.cwl_v1_0.Directory,
                    cwl_utils.parser.cwl_v1_1.Directory,
                    cwl_utils.parser.cwl_v1_2.Directory]:
            self.CWL_TYPES[typ] = lambda input : { "type": "string", "format": "uri" }

        # these are not correctly interpreted as CWL types
        self.CWL_TYPES["record"] = self.on_record
        self.CWL_TYPES["enum"] = self.on_enum
        self.CWL_TYPES["array"] = self.on_array

        self.CWL_TYPES[list] = self.on_list

        for typ in [cwl_utils.parser.cwl_v1_0.CommandInputEnumSchema,
                    cwl_utils.parser.cwl_v1_1.CommandInputEnumSchema,
                    cwl_utils.parser.cwl_v1_2.CommandInputEnumSchema]:
            self.CWL_TYPES[typ] = self.on_enum_schema

        for typ in [cwl_utils.parser.cwl_v1_0.CommandInputParameter,
                    cwl_utils.parser.cwl_v1_1.CommandInputParameter,
                    cwl_utils.parser.cwl_v1_2.CommandInputParameter]:
            self.CWL_TYPES[typ] = self.on_input_parameter

        for typ in [cwl_utils.parser.cwl_v1_0.InputArraySchema,
                    cwl_utils.parser.cwl_v1_1.InputArraySchema,
                    cwl_utils.parser.cwl_v1_2.InputArraySchema,
                    cwl_utils.parser.cwl_v1_0.OutputArraySchema,
                    cwl_utils.parser.cwl_v1_1.OutputArraySchema,
                    cwl_utils.parser.cwl_v1_2.OutputArraySchema,
                    cwl_utils.parser.cwl_v1_0.CommandInputArraySchema,
                    cwl_utils.parser.cwl_v1_1.CommandInputArraySchema,
                    cwl_utils.parser.cwl_v1_2.CommandInputArraySchema,
                    cwl_utils.parser.cwl_v1_0.CommandOutputArraySchema,
                    cwl_utils.parser.cwl_v1_1.CommandOutputArraySchema,
                    cwl_utils.parser.cwl_v1_2.CommandOutputArraySchema]:
            self.CWL_TYPES[typ] = self.on_input_array_schema

        for typ in [cwl_utils.parser.cwl_v1_0.CommandInputRecordSchema,
                    cwl_utils.parser.cwl_v1_1.CommandInputRecordSchema,
                    cwl_utils.parser.cwl_v1_2.CommandInputRecordSchema]:
            self.CWL_TYPES[typ] = self.on_record_schema

    def clean_name(self, name: str) -> str:
        return name[name.rfind('/') + 1:]

    def is_nullable(self, input):
        return hasattr(input, "type_") and  isinstance(input.type_, list) and "null" in input.type_

    # enum

    def on_enum_internal(self, symbols):
        return {
            "type": "string",
            "enum": list(map(lambda symbol : self.clean_name(symbol), symbols))
        }

    def on_enum_schema(self, input):
        return self.on_enum_internal(input.type_.symbols)

    def on_enum(self, input):
        return self.on_enum_internal(input.symbols)

    def on_array_internal(self, items):
        return {
            "type": "array",
            "items": self.on_input(items)
        }

    def on_array(self, input):
        return self.on_array_internal(input.items)

    def on_input_array_schema(self, input):
        return self.on_array_internal(input.type_.items)

    def on_input_parameter(self, input):
        logger.warning(f"input_parameter not supported yet: {input}")
        return {}

    def _warn_unsupported_type(self, typ: Any):
        supported_types = '\n * '.join([str(k) for k in list(self.CWL_TYPES.keys())])
        logger.warning(f"{typ} not supported yet, currently supporting only:\n * {supported_types}")

    def search_type_in_dictionary(self, expected):
        for requirement in self.cwl.requirements:
            if ("SchemaDefRequirement" == requirement.class_):
                for type in requirement.types:
                    if (expected == type.name):
                        return self.on_input(type)

        self._warn_unsupported_type(expected)
        return {}

    def on_input(self, input):
        type = {}

        if isinstance(input, str):
            if input in self.CWL_TYPES:
                type = self.CWL_TYPES.get(input)(input)
            else:
                type = self.search_type_in_dictionary(input)
        elif hasattr(input, "type_"):
            if isinstance(input.type_, str):
                if input.type_ in self.CWL_TYPES:
                    type = self.CWL_TYPES.get(input.type_)(input)
                else:
                    type = self.search_type_in_dictionary(input.type_)
            elif input.type_.__class__ in self.CWL_TYPES:
                type = self.CWL_TYPES.get(input.type_.__class__)(input)
            else:
                self._warn_unsupported_type(input.type_)
        else:
            logger.warning(f"I still don't know what to do for {input}")

        if hasattr(input, "default") and input.default:
            type["default"] = input.default

        return type

    def on_list(self, input):
        nullable = self.is_nullable(input)

        input_list = {
            "nullable": nullable
        }

        if nullable and 2 == len(input.type_):
            for item in input.type_:
                if "null" != item:
                    input_list.update(self.on_input(item))
        else:
            input_list["anyOf"] = []
            for item in input.type_:
                if "null" != item:
                    input_list["anyOf"].append(self.on_input(item))

        return input_list

    # record

    def on_record_internal(self, record, fields):
        record_name = ''
        if hasattr(record, "name"):
            record_name = record.name
        elif hasattr(record, "id"):
            record_name = record.id
        else:
            logger.warning(f"Impossible to detect {record.__dict__}, skipping name check...")

        if self.STRING_FORMAT_URL in record_name:
            return { "type": "string", "format": self.STRING_FORMATS.get(record.name.split('#')[-1]) }

        record = {
            "type": "object",
            "properties": {},
            "required": []
        }

        for field in fields:
            field_id = self.clean_name(field.name)
            record["properties"][field_id] = self.on_input(field)

            if not self.is_nullable(field):
                record["required"].append(field_id)

        return record

    def on_record_schema(self, input):
        return self.on_record_internal(input, input.type_.fields)

    def on_record(self, input):
        return self.on_record_internal(input, input.fields)

    def _to_ogc(self, params):
        ogc_map = {}

        for param in params:
            schema = { "schema": self.on_input(param) }

            if param.label:
                schema["title"] = param.label

            if param.doc:
                schema["description"] = param.doc

            ogc_map[self.clean_name(param.id)] = schema

        return ogc_map

    def get_inputs(self):
        return self._to_ogc(self.cwl.inputs)

    def get_outputs(self):
        return self._to_ogc(self.cwl.outputs)

    def _dump(self, data: dict, stream: Any):
        json.dump(data, stream, indent=2)

    def dump_inputs(self, stream: Any):
        self._dump(data=self.get_inputs(), stream=stream)

    def dump_outputs(self, stream: Any):
        self._dump(data=self.get_outputs(), stream=stream)        

def _is_url(path_or_url: str) -> bool:
    try:
        result = urlparse(path_or_url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except Exception:
        return False

def load_converter_from_location(path_or_url: str) -> BaseCWLtypes2OGCConverter:
    if _is_url(path_or_url):
        response = requests.get(path_or_url, stream=True)
        response.raise_for_status()

        # Read first 2 bytes to check for gzip
        magic = response.raw.read(2)
        remaining = response.raw.read()  # Read rest of the stream
        combined = io.BytesIO(magic + remaining)

        if magic == b'\x1f\x8b':
            decompressed = gzip.GzipFile(fileobj=combined)
            text_stream = io.TextIOWrapper(decompressed, encoding='utf-8')
        else:
            text_stream = io.TextIOWrapper(combined, encoding='utf-8')

        return load_converter_from_stream(text_stream)
    elif os.path.exists(path_or_url):
        with open(path_or_url, 'r', encoding='utf-8') as f:
            return load_converter_from_stream(f)
    else:
        raise ValueError(f"Invalid source {path_or_url}: not a URL or existing file path")

def load_converter_from_string_content(content: str) -> BaseCWLtypes2OGCConverter:
    return load_converter_from_stream(io.StringIO(content))

def load_converter_from_stream(content: io.TextIOWrapper) -> BaseCWLtypes2OGCConverter:
    cwl_content = yaml.safe_load(content)
    return load_converter_from_yaml(cwl_content)

def load_converter_from_yaml(cwl_content: dict) -> BaseCWLtypes2OGCConverter:
    cwl = load_document_by_yaml(yaml=cwl_content, uri="io://", load_all=True)

    if isinstance(cwl, list):
        return [BaseCWLtypes2OGCConverter(cwl=swf) for swf in cwl]

    return BaseCWLtypes2OGCConverter(cwl=cwl)
