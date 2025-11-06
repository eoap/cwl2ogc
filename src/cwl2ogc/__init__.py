# Copyright 2025 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .stac_item import STAC_ITEM_SCHEMA
from .stac_collection import STAC_COLLECTION_SCHEMA
from abc import (
    ABC,
    abstractmethod
)
from cwl_utils.parser import (
    cwl_v1_0,
    cwl_v1_1,
    cwl_v1_2,
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
    OutputRecordSchema,
    Process
)
from io import IOBase
from loguru import logger
from typing import (
    Any,
    get_args,
    get_origin,
    List,
    Mapping,
    MutableMapping,
    TextIO,
    Union
)
import cwl_utils
import json

__CommandInputEnumSchema__ = Union[cwl_v1_0.CommandInputEnumSchema,
                                   cwl_v1_1.CommandInputEnumSchema,
                                   cwl_v1_2.CommandInputEnumSchema]

__CommandOutputEnumSchema__ = Union[cwl_v1_0.CommandOutputEnumSchema,
                                    cwl_v1_1.CommandOutputEnumSchema,
                                    cwl_v1_2.CommandOutputEnumSchema]

__CommandInputRecordSchema__ = Union[cwl_v1_0.CommandInputRecordSchema,
                                     cwl_v1_1.CommandInputRecordSchema,
                                     cwl_v1_2.CommandInputRecordSchema]

__CommandInputArraySchema__ = Union[cwl_v1_0.CommandInputArraySchema,
                                    cwl_v1_1.CommandInputArraySchema,
                                    cwl_v1_2.CommandInputArraySchema]

__CommandOutputArraySchema__ = Union[cwl_v1_0.CommandOutputArraySchema,
                                     cwl_v1_1.CommandOutputArraySchema,
                                     cwl_v1_2.CommandOutputArraySchema]

__CommandOutputRecordSchema__ = Union[cwl_v1_0.CommandOutputRecordSchema,
                                      cwl_v1_1.CommandOutputRecordSchema,
                                      cwl_v1_2.CommandOutputRecordSchema]

__STRING_FORMAT_URL__ = 'https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml'

__STRING_FORMATS__ = {
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

class __CWLtypes2OGCConverter__(ABC):

    @abstractmethod
    def _on_enum(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def _on_enum_schema(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def _on_array(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def _on_input_array_schema(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def _on_input_parameter(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def _on_input(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def _on_list(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def _on_record(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def _on_record_schema(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        pass

class BaseCWLtypes2OGCConverter(__CWLtypes2OGCConverter__):
    '''
    A helper class to automate the conversion of CWL input/output definitions into OGC API - Processes and JSON Schemas.
    '''

    def __init__(
        self,
        cwl: Process
    ):
        '''
        Initializes the converter, given the CWL document where extracting informations from.

        Args:
            `cwl` (`Process`): The CWL document object model

        Returns:
            `None`: none.
        '''
        self.cwl = cwl
        self._CWL_TYPES__ = {}

        def _map_type(
            type_: Any,
            map_function: Any
        ) -> None:
            if isinstance(type_, list):
                for typ in type_:
                    _map_type(typ, map_function)
            elif get_origin(type_) is Union:
                for typ in get_args(type_):
                    _map_type(typ, map_function)
            else:
               self._CWL_TYPES__[type_] = map_function

        _map_type("int", lambda input : { "type": "integer", "format": "int32" })
        _map_type("long", lambda input : { "type": "integer", "format": "int64" })
        _map_type("double", lambda input : { "type": "number", "format": "double" })
        _map_type("float", lambda input : { "type": "number", "format": "float" })
        _map_type("boolean", lambda input : { "type": "boolean" })
        _map_type(["string", "stdout"], lambda input : { "type": "string" })

        _map_type(["File", File], lambda input : {
                                                    "oneOf": [
                                                        { "type": "string", "format": "uri" },
                                                        STAC_ITEM_SCHEMA
                                                    ]
                                                })
        _map_type(["Directory", Directory], lambda input : {
                                                            "oneOf": [
                                                                { "type": "string", "format": "uri" },
                                                                STAC_ITEM_SCHEMA,
                                                                STAC_COLLECTION_SCHEMA
                                                            ]
                                                        })
        

        # these are not correctly interpreted as CWL types
        _map_type("record", self._on_record)
        _map_type("enum", self._on_enum)
        _map_type("array", self._on_array)

        _map_type(list, self._on_list)

        _map_type([__CommandInputEnumSchema__,
                   __CommandOutputEnumSchema__,
                   EnumSchema,
                   InputEnumSchema,
                   OutputEnumSchema], self._on_enum_schema)

        _map_type([CommandInputParameter,
                   CommandOutputParameter,
                   InputParameter,
                   OutputParameter], self._on_input_parameter)

        _map_type([__CommandInputArraySchema__,
                   __CommandOutputArraySchema__,
                   InputArraySchema,
                   OutputArraySchema], self._on_input_array_schema)

        _map_type([__CommandInputRecordSchema__,
                   __CommandOutputRecordSchema__,
                   InputRecordSchema,
                   OutputRecordSchema], self._on_record_schema)

    def _clean_name(
        self,
        name: str
    ) -> str:
        return name[name.rfind('/') + 1:]

    def _is_nullable(
        self,
        input: Any
    ) -> bool:
        return hasattr(input, "type_") and  isinstance(input.type_, list) and "null" in input.type_

    # enum

    def _on_enum_internal(
        self,
        symbols: Any
    ) -> Mapping[str, Any]:
        return {
            "type": "string",
            "enum": list(map(lambda symbol : self._clean_name(symbol), symbols))
        }

    def _on_enum_schema(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        return self._on_enum_internal(input.type_.symbols)

    def _on_enum(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        return self._on_enum_internal(input.symbols)

    def _on_array_internal(
        self,
        items: Any
    ) -> Mapping[str, Any]:
        return {
            "type": "array",
            "items": self._on_input(items)
        }

    def _on_array(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        return self._on_array_internal(input.items)

    def _on_input_array_schema(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        return self._on_array_internal(input.type_.items)

    def _on_input_parameter(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        logger.warning(f"input_parameter not supported yet: {input}")
        return {}

    def _warn_unsupported_type(
        self,
        typ: Any
    ):
        supported_types = '\n * '.join([str(k) for k in list(self._CWL_TYPES__.keys())])
        logger.warning(f"{typ} not supported yet, currently supporting only:\n * {supported_types}")

    def _search_type_in_dictionary(
        self,
        expected: Any
    ) -> Mapping[str, Any]:
        for requirement in getattr(self.cwl, "requirements", []):
            if ("SchemaDefRequirement" == requirement.class_):
                for type in requirement.types:
                    if (expected == type.name):
                        return self._on_input(type)

        self._warn_unsupported_type(expected)
        return {}

    def _on_input(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        type: MutableMapping[str, Any] = {}

        if isinstance(input, str):
            if input in self._CWL_TYPES__:
                type.update(self._CWL_TYPES__[input](input))
            else:
                type.update(self._search_type_in_dictionary(input))
        elif hasattr(input, "type_"):
            if isinstance(input.type_, str):
                if input.type_ in self._CWL_TYPES__:
                    type.update(self._CWL_TYPES__[input.type_](input))
                else:
                    type.update(self._search_type_in_dictionary(input.type_))
            elif input.type_.__class__ in self._CWL_TYPES__:
                type.update(self._CWL_TYPES__[input.type_.__class__](input))
            else:
                self._warn_unsupported_type(input.type_)
        else:
            logger.warning(f"I still don't know what to do for {input}")

        default_value = getattr(input, "default", None)
        if default_value:
            type["default"] = default_value

        return type

    def _on_list(self, input) -> Mapping[str, Any]:
        input_list: MutableMapping[str, Any] = {
            "nullable": self._is_nullable(input)
        }

        inputs_schema = list(
            map(
                lambda item: self._on_input(item),
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

    def _on_record_internal(
        self,
        record: Any,
        fields: List[Any]
    ) -> Mapping[str, Any]:
        record_name = ''
        if hasattr(record, "name"):
            record_name = record.name
        elif hasattr(record, "id"):
            record_name = record.id
        else:
            logger.warning(f"Impossible to detect {record.__dict__}, skipping name check...")

        if __STRING_FORMAT_URL__ in record_name:
            return { "type": "string", "format": __STRING_FORMATS__.get(record.name.split('#')[-1]) }

        record = {
            "type": "object",
            "properties": {},
            "required": []
        }

        for field in fields:
            field_id = self._clean_name(field.name)
            record["properties"][field_id] = self._on_input(field)

            if not self._is_nullable(field):
                record["required"].append(field_id)

        return record

    def _on_record_schema(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        return self._on_record_internal(input, input.type_.fields)

    def _on_record(
        self,
        input: Any
    ) -> Mapping[str, Any]:
        return self._on_record_internal(input, input.fields)

    def _type_to_string(
        self,
        typ: Any
    ) -> str:
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

    def _to_ogc(
        self,
        params,
        is_input: bool = False
    ) -> Mapping[str, Any]:
        ogc_map = {}

        for param in params:
            schema = {
                "schema": self._on_input(param),
                "metadata": [ { "title": "cwl:type", "value": f"{self._type_to_string(param.type_)}" } ]
            }

            if is_input:
                schema["minOccurs"] = 0 if self._is_nullable(param) else 1
                schema["maxOccurs"] = 1
                schema["valuePassing"] = "byValue"

            if param.label:
                schema["title"] = param.label

            if param.doc:
                schema["description"] = param.doc

            ogc_map[self._clean_name(param.id)] = schema

        return ogc_map

    def get_inputs(self) -> Mapping[str, Any]:
        '''
        Returns a dictionary representing OGC API - Processes inputs in-memory structure.

        Returns:
            `dict`: The generated dictionary representing OGC API - Processes inputs in-memory structure.
        '''
        return self._to_ogc(params=self.cwl.inputs, is_input=True)

    def get_outputs(self) -> Mapping[str, Any]:
        '''
        Returns a dictionary representing OGC API - Processes outputs in-memory structure.

        Returns:
            `dict`: The generated dictionary representing OGC API - Processes inputs in-memory structure.
        '''
        return self._to_ogc(params=self.cwl.outputs)

    def _to_json_schema(
        self,
        parameters: Mapping[str, Any],
        label: str
    ) -> Mapping[str, Any]:
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

    def get_inputs_json_schema(self) -> Mapping[str, Any]:
        '''
        Returns a dictionary representing the inputs JSON Schema in-memory structure.

        Returns:
            `dict`: The generated dictionary the inputs JSON Schema in-memory structure.
        '''
        return self._to_json_schema(self.get_inputs(), "inputs")
    
    def get_outputs_json_schema(self) -> Mapping[str, Any]:
        '''
        Returns a dictionary representing the outputs JSON Schema in-memory structure.

        Returns:
            `dict`: The generated dictionary representing the outputs JSON Schema in-memory structure.
        '''
        return self._to_json_schema(self.get_outputs(), "outputs")

    def _dump(
        self,
        data: Mapping[str, Any],
        stream: TextIO,
        pretty_print: bool
    ):
        json.dump(data, stream, indent=2 if pretty_print else None)

    def dump_inputs(
        self,
        stream: TextIO,
        pretty_print: bool = False
    ):
        '''
        Dumps the OGC API - Processes inputs schema to its JSON representation.

        Args:
            `stream` (`TextIO`): The stream where serializing the JSON representation
            `pretty_print` (`bool`): formats the output if `True`, in a single line otherwise. Default is `False`

        Returns:
            `None`: none.
        '''
        self._dump(
            data=self.get_inputs(),
            stream=stream,
            pretty_print=pretty_print
        )

    def dump_outputs(
        self,
        stream: TextIO,
        pretty_print: bool = False
    ):
        '''
        Dumps the OGC API - Processes outputs schema to its JSON representation.

        Args:
            `stream` (`TextIO`): The stream where serializing the JSON representation
            `pretty_print` (`bool`): formats the output if `True`, in a single line otherwise. Default is `False`

        Returns:
            `None`: none.
        '''
        self._dump(
            data=self.get_outputs(),
            stream=stream,
            pretty_print=pretty_print
        )

    def dump_inputs_json_schema(
        self,
        stream: TextIO,
        pretty_print: bool = False
    ):
        '''
        Dumps the inputs JSON Schema to its JSON representation.

        Args:
            `stream` (`TextIO`): The stream where serializing the JSON representation
            `pretty_print` (`bool`): formats the output if `True`, in a single line otherwise. Default is `False`

        Returns:
            `None`: none.
        '''
        self._dump(
            data=self.get_inputs_json_schema(),
            stream=stream,
            pretty_print=pretty_print
        )

    def dump_outputs_json_schema(
        self,
        stream: TextIO,
        pretty_print: bool = False
    ):
        '''
        Dumps the outputs JSON Schema to its JSON representation.

        Args:
            `stream` (`TextIO`): The stream where serializing the JSON representation
            `pretty_print` (`bool`): formats the output if `True`, in a single line otherwise. Default is `False`

        Returns:
            `None`: none.
        '''
        self._dump(
            data=self.get_outputs_json_schema(),
            stream=stream,
            pretty_print=pretty_print
        )
