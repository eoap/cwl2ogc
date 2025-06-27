# SPDX-FileCopyrightText: 2025-present Fabrice Brito <fabrice.brito@terradue.com>
#
# SPDX-License-Identifier: MIT

import cwl_utils
from loguru import logger

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
        self.CWL_TYPES["File"] = lambda input : { "type": "string", "format": "uri" }
        self.CWL_TYPES["Directory"] = self.CWL_TYPES["File"]

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
                    cwl_utils.parser.cwl_v1_0.CommandInputArraySchema,
                    cwl_utils.parser.cwl_v1_1.CommandInputArraySchema,
                    cwl_utils.parser.cwl_v1_2.CommandInputArraySchema]:
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

    def search_type_in_dictionary(self, expected):
        for requirement in self.cwl.requirements:
            if ("SchemaDefRequirement" == requirement.class_):
                for type in requirement.types:
                    if (expected == type.name):
                        return self.on_input(type)

        logger.warning(f"{expected} not supported yet, currently supporting only: {list(self.CWL_TYPES.keys())}")
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
                logger.warning(f"{input.type_} not supported yet, currently supporting only: {list(self.CWL_TYPES.keys())}")
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

    def to_ogc(self, params):
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
        return self.to_ogc(self.cwl.inputs)

    def get_outputs(self):
        return self.to_ogc(self.cwl.outputs)
