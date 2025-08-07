# SPDX-FileCopyrightText: 2025-present Fabrice Brito <fabrice.brito@terradue.com>
#
# SPDX-License-Identifier: MIT

from cwl_utils.parser import (
    load_document_by_yaml,
    CommandInputParameter,
    CommandOutputParameter,
    Directory,
    EnumSchema,
    File,
    InputArraySchema,
    InputEnumSchema,
    InputParameter,
    InputRecordSchema,
    OutputArraySchema,
    OutputEnumSchema,
    OutputParameter,
    OutputRecordSchema
)
from loguru import logger
from urllib.parse import urlparse
from typing import (
    Any,
    get_args,
    get_origin,
    Union
)
import cwl_utils
import gzip
import io
import json
import yaml
import requests
import os

CommandInputEnumSchema = Union[cwl_utils.parser.cwl_v1_0.CommandInputEnumSchema,
                               cwl_utils.parser.cwl_v1_1.CommandInputEnumSchema,
                               cwl_utils.parser.cwl_v1_2.CommandInputEnumSchema]

CommandOutputEnumSchema = Union[cwl_utils.parser.cwl_v1_0.CommandOutputEnumSchema,
                                cwl_utils.parser.cwl_v1_1.CommandOutputEnumSchema,
                                cwl_utils.parser.cwl_v1_2.CommandOutputEnumSchema]

CommandInputRecordSchema = Union[cwl_utils.parser.cwl_v1_0.CommandInputRecordSchema,
                                 cwl_utils.parser.cwl_v1_1.CommandInputRecordSchema,
                                 cwl_utils.parser.cwl_v1_2.CommandInputRecordSchema]

CommandInputArraySchema = Union[cwl_utils.parser.cwl_v1_0.CommandInputArraySchema,
                                cwl_utils.parser.cwl_v1_1.CommandInputArraySchema,
                                cwl_utils.parser.cwl_v1_2.CommandInputArraySchema]

CommandOutputArraySchema = Union[cwl_utils.parser.cwl_v1_0.CommandOutputArraySchema,
                                 cwl_utils.parser.cwl_v1_1.CommandOutputArraySchema,
                                 cwl_utils.parser.cwl_v1_2.CommandOutputArraySchema]

CommandOutputRecordSchema = Union[cwl_utils.parser.cwl_v1_0.CommandOutputRecordSchema,
                                  cwl_utils.parser.cwl_v1_1.CommandOutputRecordSchema,
                                  cwl_utils.parser.cwl_v1_2.CommandOutputRecordSchema]

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

        def _map_type(type_: Any, map_function: Any) -> None:
            if isinstance(type_, list):
                for typ in type_:
                    _map_type(typ, map_function)
            elif get_origin(type_) is Union:
                for typ in get_args(type_):
                    _map_type(typ, map_function)
            else:
               self.CWL_TYPES[type_] = map_function
            
        _map_type("int", lambda input : { "type": "integer", "format": "int32" })
        _map_type("long", lambda input : { "type": "integer", "format": "int64" })
        _map_type("double", lambda input : { "type": "number", "format": "double" })
        _map_type("float", lambda input : { "type": "number", "format": "float" })
        _map_type("boolean", lambda input : { "type": "boolean" })
        _map_type(["string", "stdout"], lambda input : { "type": "string" })

        _map_type(["File", File, "Directory", Directory], lambda input : { "type": "string", "format": "uri" })

        # these are not correctly interpreted as CWL types
        _map_type("record", self.on_record)
        _map_type("enum", self.on_enum)
        _map_type("array", self.on_array)

        _map_type(list, self.on_list)

        _map_type([CommandInputEnumSchema,
                   CommandOutputEnumSchema,
                   EnumSchema,
                   InputEnumSchema,
                   OutputEnumSchema], self.on_enum_schema)

        _map_type([CommandInputParameter,
                   CommandOutputParameter,
                   InputParameter,
                   OutputParameter], self.on_input_parameter)

        _map_type([CommandInputArraySchema,
                   CommandOutputArraySchema,
                   InputArraySchema,
                   OutputArraySchema], self.on_input_array_schema)

        _map_type([CommandInputRecordSchema,
                   CommandOutputRecordSchema,
                   InputRecordSchema,
                   OutputRecordSchema], self.on_record_schema)

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
        for requirement in getattr(self.cwl, "requirements", []):
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
        input_list = {
            "nullable": self.is_nullable(input)
        }

        inputs_schema = list(
            map(
                lambda item: self.on_input(item),
                filter(
                    lambda current: "null" != current,
                    input.type_
                )
            )
        )

        if 1 == len(inputs_schema):
            input_list.update(inputs_schema[0])
        else:
            input_list["anyOf"] = inputs_schema

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

    def _type_to_string(self, typ: Any) -> str:
        if get_origin(typ) is Union:
            return " or ".join([self._type_to_string(inner_type) for inner_type in get_args(typ)])

        if isinstance(typ, list):
            return f"[ {', '.join([self._type_to_string(t) for t in typ])} ]"

        if hasattr(typ, "items"):
            return f"{self._type_to_string(typ.items)}[]"

        if hasattr(typ, "symbols"):
             return f"enum[ {', '.join([s.split('/')[-1] for s in typ.symbols])} ]"

        if hasattr(typ, 'type_'):
            return self._type_to_string(typ.type_)

        if isinstance(typ, str):
            return typ
        
        return typ.__name__

    def _to_ogc(self, params, is_input: bool = False):
        ogc_map = {}

        for param in params:
            schema = {
                "schema": self.on_input(param),
                "metadata": [ { "title": "cwl:type", "value": f"{self._type_to_string(param.type_)}" } ]
            }

            if is_input:
                schema["minOccurs"] = 0 if self.is_nullable(param) else 1
                schema["maxOccurs"] = 1
                schema["valuePassing"] = "byValue"

            if param.label:
                schema["title"] = param.label

            if param.doc:
                schema["description"] = param.doc

            ogc_map[self.clean_name(param.id)] = schema

        return ogc_map

    def get_inputs(self):
        return self._to_ogc(params=self.cwl.inputs, is_input=True)

    def get_outputs(self):
        return self._to_ogc(params=self.cwl.outputs)
    
    def _to_json_schema(self, parameters: dict, label: str) -> dict:
        id = self.cwl.id.split('#')[-1]

        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"https://eoap.github.io/cwl2ogc/{id}/{label}.yaml",
            "description": f"The schema to represent a {id} {label} definition",
            "type": "object",
            "required": [],
            "properties": {},
            "additionalProperties": False,
            "$defs": {}
        }

        for k, v in parameters.items():
            schema["properties"][k] = { "$ref": f"#/$defs/{k}" }

            property_schema = v["schema"]
            schema["$defs"][k] = property_schema

            if "nullable" not in property_schema or not property_schema["nullable"]:
                schema["required"].append(k)

        return schema

    def get_inputs_json_schema(self) -> dict:
        return self._to_json_schema(self.get_inputs(), "inputs")
    
    def get_outputs_json_schema(self) -> dict:
        return self._to_json_schema(self.get_outputs(), "outputs")

    def _dump(self, data: dict, stream: Any, pretty_print: bool):
        json.dump(data, stream, indent=2 if pretty_print else None)

    def dump_inputs(self, stream: Any, pretty_print: bool = False):
        self._dump(data=self.get_inputs(), stream=stream, pretty_print=pretty_print)

    def dump_outputs(self, stream: Any, pretty_print: bool = False):
        self._dump(data=self.get_outputs(), stream=stream, pretty_print=pretty_print)

    def dump_inputs_json_schema(self, stream: Any, pretty_print: bool = False):
        self._dump(data=self.get_inputs_json_schema(), stream=stream, pretty_print=pretty_print)

    def dump_outputs_json_schema(self, stream: Any, pretty_print: bool = False):
        self._dump(data=self.get_outputs_json_schema(), stream=stream, pretty_print=pretty_print)

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
