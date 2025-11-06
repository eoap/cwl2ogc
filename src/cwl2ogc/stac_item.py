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

STAC_ITEM_SCHEMA = {
    "title": "STAC Item",
    "description": "This object represents the metadata for an item in a SpatioTemporal Asset Catalog.",
    "$id": "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json#",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": [
        "assets",
        "geometry",
        "id",
        "links",
        "properties",
        "stac_version",
        "type",
    ],
    "properties": {
        "type": {"type": "string", "enum": ["Feature"]},
        "properties": {
            "title": "Basic Descriptive Fields",
            "$id": "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/basics.json#",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "title": {
                    "title": "Item Title",
                    "description": "A human-readable title describing the Item.",
                    "type": "string",
                },
                "description": {
                    "title": "Item Description",
                    "description": "Detailed multi-line description to fully explain the Item.",
                    "type": "string",
                },
                "constellation": {"title": "Constellation", "type": "string"},
                "created": {
                    "title": "Creation Time",
                    "type": "string",
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
                "datetime": {
                    "title": "Date and Time",
                    "description": "The searchable date/time of the assets, in UTC (Formatted in RFC 3339) ",
                    "type": ["string", "null"],
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
                "end_datetime": {
                    "title": "End Date and Time",
                    "description": "The searchable end date/time of the assets, in UTC (Formatted in RFC 3339) ",
                    "type": "string",
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
                "gsd": {
                    "title": "Ground Sample Distance",
                    "type": "number",
                    "exclusiveMinimum": 0,
                },
                "instruments": {
                    "title": "Instruments",
                    "type": "array",
                    "items": {"type": "string"},
                },
                "license": {"type": "string", "pattern": "^[\\w\\-\\.\\+]+$"},
                "mission": {"title": "Mission", "type": "string"},
                "platform": {"title": "Platform", "type": "string"},
                "providers": {
                    "title": "Providers",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name"],
                        "properties": {
                            "description": {
                                "title": "Organization description",
                                "type": "string",
                            },
                            "name": {
                                "title": "Organization name",
                                "type": "string",
                                "minLength": 1,
                            },
                            "roles": {
                                "title": "Organization roles",
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": [
                                        "producer",
                                        "licensor",
                                        "processor",
                                        "host",
                                    ],
                                },
                            },
                            "url": {
                                "title": "Organization homepage",
                                "type": "string",
                                "format": "iri",
                            },
                        },
                    },
                },
                "start_datetime": {
                    "title": "Start Date and Time",
                    "description": "The searchable start date/time of the assets, in UTC (Formatted in RFC 3339) ",
                    "type": "string",
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
                "updated": {
                    "title": "Last Update Time",
                    "type": "string",
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
            },
            "anyOf": [
                {
                    "required": ["datetime"],
                    "properties": {"datetime": {"not": {"anyOf": [{"type": "null"}]}}},
                },
                {"required": ["datetime", "start_datetime", "end_datetime"]},
            ],
            "dependencies": {
                "end_datetime": {"required": ["start_datetime"]},
                "start_datetime": {"required": ["end_datetime"]},
            },
            "oneOf": [{"type": "null"}, {"type": "object"}],
        },
        "assets": {
            "title": "Asset links",
            "description": "Links to assets",
            "type": "object",
            "additionalProperties": {
                "title": "Basic Descriptive Fields",
                "$id": "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/basics.json#",
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "required": ["href"],
                "properties": {
                    "title": {
                        "title": "Asset title",
                        "description": "A human-readable title describing the Item.",
                        "type": "string",
                    },
                    "description": {
                        "title": "Asset description",
                        "description": "Detailed multi-line description to fully explain the Item.",
                        "type": "string",
                    },
                    "type": {"title": "Asset type", "type": "string"},
                    "constellation": {"title": "Constellation", "type": "string"},
                    "created": {
                        "title": "Creation Time",
                        "type": "string",
                        "format": "date-time",
                        "pattern": "(\\+00:00|Z)$",
                    },
                    "datetime": {
                        "title": "Date and Time",
                        "description": "The searchable date/time of the assets, in UTC (Formatted in RFC 3339) ",
                        "type": ["string", "null"],
                        "format": "date-time",
                        "pattern": "(\\+00:00|Z)$",
                    },
                    "end_datetime": {
                        "title": "End Date and Time",
                        "description": "The searchable end date/time of the assets, in UTC (Formatted in RFC 3339) ",
                        "type": "string",
                        "format": "date-time",
                        "pattern": "(\\+00:00|Z)$",
                    },
                    "gsd": {
                        "title": "Ground Sample Distance",
                        "type": "number",
                        "exclusiveMinimum": 0,
                    },
                    "href": {
                        "title": "Asset reference",
                        "type": "string",
                        "format": "iri-reference",
                        "minLength": 1,
                    },
                    "instruments": {
                        "title": "Instruments",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "license": {"type": "string", "pattern": "^[\\w\\-\\.\\+]+$"},
                    "mission": {"title": "Mission", "type": "string"},
                    "platform": {"title": "Platform", "type": "string"},
                    "providers": {
                        "title": "Providers",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["name"],
                            "properties": {
                                "description": {
                                    "title": "Organization description",
                                    "type": "string",
                                },
                                "name": {
                                    "title": "Organization name",
                                    "type": "string",
                                    "minLength": 1,
                                },
                                "roles": {
                                    "title": "Organization roles",
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "enum": [
                                            "producer",
                                            "licensor",
                                            "processor",
                                            "host",
                                        ],
                                    },
                                },
                                "url": {
                                    "title": "Organization homepage",
                                    "type": "string",
                                    "format": "iri",
                                },
                            },
                        },
                    },
                    "roles": {
                        "title": "Asset roles",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "start_datetime": {
                        "title": "Start Date and Time",
                        "description": "The searchable start date/time of the assets, in UTC (Formatted in RFC 3339) ",
                        "type": "string",
                        "format": "date-time",
                        "pattern": "(\\+00:00|Z)$",
                    },
                    "updated": {
                        "title": "Last Update Time",
                        "type": "string",
                        "format": "date-time",
                        "pattern": "(\\+00:00|Z)$",
                    },
                },
                "dependencies": {
                    "end_datetime": {"required": ["start_datetime"]},
                    "start_datetime": {"required": ["end_datetime"]},
                },
            },
        },
        "bbox": {"type": "array", "items": {"type": "number"}, "minItems": 4},
        "geometry": {
            "oneOf": [
                {"type": "null"},
                {
                    "title": "GeoJSON Point",
                    "type": "object",
                    "required": ["type", "coordinates"],
                    "properties": {
                        "type": {"type": "string", "enum": ["Point"]},
                        "bbox": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 4,
                        },
                        "coordinates": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 2,
                        },
                    },
                },
                {
                    "title": "GeoJSON LineString",
                    "type": "object",
                    "required": ["type", "coordinates"],
                    "properties": {
                        "type": {"type": "string", "enum": ["LineString"]},
                        "bbox": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 4,
                        },
                        "coordinates": {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "items": {"type": "number"},
                                "minItems": 2,
                            },
                            "minItems": 2,
                        },
                    },
                },
                {
                    "title": "GeoJSON Polygon",
                    "type": "object",
                    "required": ["type", "coordinates"],
                    "properties": {
                        "type": {"type": "string", "enum": ["Polygon"]},
                        "bbox": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 4,
                        },
                        "coordinates": {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 2,
                                },
                                "minItems": 4,
                            },
                        },
                    },
                },
                {
                    "title": "GeoJSON MultiPoint",
                    "type": "object",
                    "required": ["type", "coordinates"],
                    "properties": {
                        "type": {"type": "string", "enum": ["MultiPoint"]},
                        "bbox": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 4,
                        },
                        "coordinates": {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "items": {"type": "number"},
                                "minItems": 2,
                            },
                        },
                    },
                },
                {
                    "title": "GeoJSON MultiLineString",
                    "type": "object",
                    "required": ["type", "coordinates"],
                    "properties": {
                        "type": {"type": "string", "enum": ["MultiLineString"]},
                        "bbox": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 4,
                        },
                        "coordinates": {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 2,
                                },
                                "minItems": 2,
                            },
                        },
                    },
                },
                {
                    "title": "GeoJSON MultiPolygon",
                    "type": "object",
                    "required": ["type", "coordinates"],
                    "properties": {
                        "type": {"type": "string", "enum": ["MultiPolygon"]},
                        "bbox": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 4,
                        },
                        "coordinates": {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {"type": "number"},
                                        "minItems": 2,
                                    },
                                    "minItems": 4,
                                },
                            },
                        },
                    },
                },
                {
                    "title": "GeoJSON GeometryCollection",
                    "type": "object",
                    "required": ["type", "geometries"],
                    "properties": {
                        "type": {"type": "string", "enum": ["GeometryCollection"]},
                        "bbox": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 4,
                        },
                        "geometries": {
                            "type": "array",
                            "items": {
                                "oneOf": [
                                    {
                                        "title": "GeoJSON Point",
                                        "type": "object",
                                        "required": ["type", "coordinates"],
                                        "properties": {
                                            "type": {
                                                "type": "string",
                                                "enum": ["Point"],
                                            },
                                            "bbox": {
                                                "type": "array",
                                                "items": {"type": "number"},
                                                "minItems": 4,
                                            },
                                            "coordinates": {
                                                "type": "array",
                                                "items": {"type": "number"},
                                                "minItems": 2,
                                            },
                                        },
                                    },
                                    {
                                        "title": "GeoJSON LineString",
                                        "type": "object",
                                        "required": ["type", "coordinates"],
                                        "properties": {
                                            "type": {
                                                "type": "string",
                                                "enum": ["LineString"],
                                            },
                                            "bbox": {
                                                "type": "array",
                                                "items": {"type": "number"},
                                                "minItems": 4,
                                            },
                                            "coordinates": {
                                                "type": "array",
                                                "items": {
                                                    "type": "array",
                                                    "items": {"type": "number"},
                                                    "minItems": 2,
                                                },
                                                "minItems": 2,
                                            },
                                        },
                                    },
                                    {
                                        "title": "GeoJSON Polygon",
                                        "type": "object",
                                        "required": ["type", "coordinates"],
                                        "properties": {
                                            "type": {
                                                "type": "string",
                                                "enum": ["Polygon"],
                                            },
                                            "bbox": {
                                                "type": "array",
                                                "items": {"type": "number"},
                                                "minItems": 4,
                                            },
                                            "coordinates": {
                                                "type": "array",
                                                "items": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "array",
                                                        "items": {"type": "number"},
                                                        "minItems": 2,
                                                    },
                                                    "minItems": 4,
                                                },
                                            },
                                        },
                                    },
                                    {
                                        "title": "GeoJSON MultiPoint",
                                        "type": "object",
                                        "required": ["type", "coordinates"],
                                        "properties": {
                                            "type": {
                                                "type": "string",
                                                "enum": ["MultiPoint"],
                                            },
                                            "bbox": {
                                                "type": "array",
                                                "items": {"type": "number"},
                                                "minItems": 4,
                                            },
                                            "coordinates": {
                                                "type": "array",
                                                "items": {
                                                    "type": "array",
                                                    "items": {"type": "number"},
                                                    "minItems": 2,
                                                },
                                            },
                                        },
                                    },
                                    {
                                        "title": "GeoJSON MultiLineString",
                                        "type": "object",
                                        "required": ["type", "coordinates"],
                                        "properties": {
                                            "type": {
                                                "type": "string",
                                                "enum": ["MultiLineString"],
                                            },
                                            "bbox": {
                                                "type": "array",
                                                "items": {"type": "number"},
                                                "minItems": 4,
                                            },
                                            "coordinates": {
                                                "type": "array",
                                                "items": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "array",
                                                        "items": {"type": "number"},
                                                        "minItems": 2,
                                                    },
                                                    "minItems": 2,
                                                },
                                            },
                                        },
                                    },
                                    {
                                        "title": "GeoJSON MultiPolygon",
                                        "type": "object",
                                        "required": ["type", "coordinates"],
                                        "properties": {
                                            "type": {
                                                "type": "string",
                                                "enum": ["MultiPolygon"],
                                            },
                                            "bbox": {
                                                "type": "array",
                                                "items": {"type": "number"},
                                                "minItems": 4,
                                            },
                                            "coordinates": {
                                                "type": "array",
                                                "items": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "array",
                                                            "items": {"type": "number"},
                                                            "minItems": 2,
                                                        },
                                                        "minItems": 4,
                                                    },
                                                },
                                            },
                                        },
                                    },
                                ]
                            },
                        },
                    },
                },
            ]
        },
        "id": {
            "title": "Provider ID",
            "description": "Provider item ID",
            "type": "string",
            "minLength": 1,
            "oneOf": [{"type": "number"}, {"type": "string"}],
        },
        "links": {
            "title": "Item links",
            "description": "Links to item relations",
            "type": "array",
            "items": {
                "type": "object",
                "required": ["rel", "href"],
                "properties": {
                    "title": {"title": "Link title", "type": "string"},
                    "type": {"title": "Link type", "type": "string"},
                    "href": {
                        "title": "Link reference",
                        "type": "string",
                        "format": "iri-reference",
                        "minLength": 1,
                    },
                    "rel": {
                        "title": "Link relation type",
                        "type": "string",
                        "minLength": 1,
                    },
                },
            },
        },
        "stac_extensions": {
            "title": "STAC extensions",
            "type": "array",
            "items": {
                "title": "Reference to a JSON Schema",
                "type": "string",
                "format": "iri",
            },
            "uniqueItems": True,
        },
        "stac_version": {"title": "STAC version", "type": "string", "const": "1.0.0"},
    },
    "definitions": {
        "asset": {
            "title": "Basic Descriptive Fields",
            "$id": "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/basics.json#",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["href"],
            "properties": {
                "title": {
                    "title": "Asset title",
                    "description": "A human-readable title describing the Item.",
                    "type": "string",
                },
                "description": {
                    "title": "Asset description",
                    "description": "Detailed multi-line description to fully explain the Item.",
                    "type": "string",
                },
                "type": {"title": "Asset type", "type": "string"},
                "constellation": {"title": "Constellation", "type": "string"},
                "created": {
                    "title": "Creation Time",
                    "type": "string",
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
                "datetime": {
                    "title": "Date and Time",
                    "description": "The searchable date/time of the assets, in UTC (Formatted in RFC 3339) ",
                    "type": ["string", "null"],
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
                "end_datetime": {
                    "title": "End Date and Time",
                    "description": "The searchable end date/time of the assets, in UTC (Formatted in RFC 3339) ",
                    "type": "string",
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
                "gsd": {
                    "title": "Ground Sample Distance",
                    "type": "number",
                    "exclusiveMinimum": 0,
                },
                "href": {
                    "title": "Asset reference",
                    "type": "string",
                    "format": "iri-reference",
                    "minLength": 1,
                },
                "instruments": {
                    "title": "Instruments",
                    "type": "array",
                    "items": {"type": "string"},
                },
                "license": {"type": "string", "pattern": "^[\\w\\-\\.\\+]+$"},
                "mission": {"title": "Mission", "type": "string"},
                "platform": {"title": "Platform", "type": "string"},
                "providers": {
                    "title": "Providers",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name"],
                        "properties": {
                            "description": {
                                "title": "Organization description",
                                "type": "string",
                            },
                            "name": {
                                "title": "Organization name",
                                "type": "string",
                                "minLength": 1,
                            },
                            "roles": {
                                "title": "Organization roles",
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": [
                                        "producer",
                                        "licensor",
                                        "processor",
                                        "host",
                                    ],
                                },
                            },
                            "url": {
                                "title": "Organization homepage",
                                "type": "string",
                                "format": "iri",
                            },
                        },
                    },
                },
                "roles": {
                    "title": "Asset roles",
                    "type": "array",
                    "items": {"type": "string"},
                },
                "start_datetime": {
                    "title": "Start Date and Time",
                    "description": "The searchable start date/time of the assets, in UTC (Formatted in RFC 3339) ",
                    "type": "string",
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
                "updated": {
                    "title": "Last Update Time",
                    "type": "string",
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
            },
            "dependencies": {
                "end_datetime": {"required": ["start_datetime"]},
                "start_datetime": {"required": ["end_datetime"]},
            },
        },
        "assets": {
            "title": "Asset links",
            "description": "Links to assets",
            "type": "object",
            "additionalProperties": {
                "title": "Basic Descriptive Fields",
                "$id": "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/basics.json#",
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "required": ["href"],
                "properties": {
                    "title": {
                        "title": "Asset title",
                        "description": "A human-readable title describing the Item.",
                        "type": "string",
                    },
                    "description": {
                        "title": "Asset description",
                        "description": "Detailed multi-line description to fully explain the Item.",
                        "type": "string",
                    },
                    "type": {"title": "Asset type", "type": "string"},
                    "constellation": {"title": "Constellation", "type": "string"},
                    "created": {
                        "title": "Creation Time",
                        "type": "string",
                        "format": "date-time",
                        "pattern": "(\\+00:00|Z)$",
                    },
                    "datetime": {
                        "title": "Date and Time",
                        "description": "The searchable date/time of the assets, in UTC (Formatted in RFC 3339) ",
                        "type": ["string", "null"],
                        "format": "date-time",
                        "pattern": "(\\+00:00|Z)$",
                    },
                    "end_datetime": {
                        "title": "End Date and Time",
                        "description": "The searchable end date/time of the assets, in UTC (Formatted in RFC 3339) ",
                        "type": "string",
                        "format": "date-time",
                        "pattern": "(\\+00:00|Z)$",
                    },
                    "gsd": {
                        "title": "Ground Sample Distance",
                        "type": "number",
                        "exclusiveMinimum": 0,
                    },
                    "href": {
                        "title": "Asset reference",
                        "type": "string",
                        "format": "iri-reference",
                        "minLength": 1,
                    },
                    "instruments": {
                        "title": "Instruments",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "license": {"type": "string", "pattern": "^[\\w\\-\\.\\+]+$"},
                    "mission": {"title": "Mission", "type": "string"},
                    "platform": {"title": "Platform", "type": "string"},
                    "providers": {
                        "title": "Providers",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["name"],
                            "properties": {
                                "description": {
                                    "title": "Organization description",
                                    "type": "string",
                                },
                                "name": {
                                    "title": "Organization name",
                                    "type": "string",
                                    "minLength": 1,
                                },
                                "roles": {
                                    "title": "Organization roles",
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "enum": [
                                            "producer",
                                            "licensor",
                                            "processor",
                                            "host",
                                        ],
                                    },
                                },
                                "url": {
                                    "title": "Organization homepage",
                                    "type": "string",
                                    "format": "iri",
                                },
                            },
                        },
                    },
                    "roles": {
                        "title": "Asset roles",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "start_datetime": {
                        "title": "Start Date and Time",
                        "description": "The searchable start date/time of the assets, in UTC (Formatted in RFC 3339) ",
                        "type": "string",
                        "format": "date-time",
                        "pattern": "(\\+00:00|Z)$",
                    },
                    "updated": {
                        "title": "Last Update Time",
                        "type": "string",
                        "format": "date-time",
                        "pattern": "(\\+00:00|Z)$",
                    },
                },
                "dependencies": {
                    "end_datetime": {"required": ["start_datetime"]},
                    "start_datetime": {"required": ["end_datetime"]},
                },
            },
        },
        "common_metadata": {
            "title": "Basic Descriptive Fields",
            "$id": "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/basics.json#",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "title": {
                    "title": "Item Title",
                    "description": "A human-readable title describing the Item.",
                    "type": "string",
                },
                "description": {
                    "title": "Item Description",
                    "description": "Detailed multi-line description to fully explain the Item.",
                    "type": "string",
                },
                "constellation": {"title": "Constellation", "type": "string"},
                "created": {
                    "title": "Creation Time",
                    "type": "string",
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
                "datetime": {
                    "title": "Date and Time",
                    "description": "The searchable date/time of the assets, in UTC (Formatted in RFC 3339) ",
                    "type": ["string", "null"],
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
                "end_datetime": {
                    "title": "End Date and Time",
                    "description": "The searchable end date/time of the assets, in UTC (Formatted in RFC 3339) ",
                    "type": "string",
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
                "gsd": {
                    "title": "Ground Sample Distance",
                    "type": "number",
                    "exclusiveMinimum": 0,
                },
                "instruments": {
                    "title": "Instruments",
                    "type": "array",
                    "items": {"type": "string"},
                },
                "license": {"type": "string", "pattern": "^[\\w\\-\\.\\+]+$"},
                "mission": {"title": "Mission", "type": "string"},
                "platform": {"title": "Platform", "type": "string"},
                "providers": {
                    "title": "Providers",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name"],
                        "properties": {
                            "description": {
                                "title": "Organization description",
                                "type": "string",
                            },
                            "name": {
                                "title": "Organization name",
                                "type": "string",
                                "minLength": 1,
                            },
                            "roles": {
                                "title": "Organization roles",
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": [
                                        "producer",
                                        "licensor",
                                        "processor",
                                        "host",
                                    ],
                                },
                            },
                            "url": {
                                "title": "Organization homepage",
                                "type": "string",
                                "format": "iri",
                            },
                        },
                    },
                },
                "start_datetime": {
                    "title": "Start Date and Time",
                    "description": "The searchable start date/time of the assets, in UTC (Formatted in RFC 3339) ",
                    "type": "string",
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
                "updated": {
                    "title": "Last Update Time",
                    "type": "string",
                    "format": "date-time",
                    "pattern": "(\\+00:00|Z)$",
                },
            },
            "dependencies": {
                "end_datetime": {"required": ["start_datetime"]},
                "start_datetime": {"required": ["end_datetime"]},
            },
        },
        "core": {
            "title": "GeoJSON Feature",
            "$id": "https://geojson.org/schema/Feature.json",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": [
                "assets",
                "geometry",
                "id",
                "links",
                "properties",
                "stac_version",
                "type",
            ],
            "properties": {
                "type": {"type": "string", "enum": ["Feature"]},
                "properties": {
                    "title": "Basic Descriptive Fields",
                    "$id": "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/basics.json#",
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "type": "object",
                    "properties": {
                        "title": {
                            "title": "Item Title",
                            "description": "A human-readable title describing the Item.",
                            "type": "string",
                        },
                        "description": {
                            "title": "Item Description",
                            "description": "Detailed multi-line description to fully explain the Item.",
                            "type": "string",
                        },
                        "constellation": {"title": "Constellation", "type": "string"},
                        "created": {
                            "title": "Creation Time",
                            "type": "string",
                            "format": "date-time",
                            "pattern": "(\\+00:00|Z)$",
                        },
                        "datetime": {
                            "title": "Date and Time",
                            "description": "The searchable date/time of the assets, in UTC (Formatted in RFC 3339) ",
                            "type": ["string", "null"],
                            "format": "date-time",
                            "pattern": "(\\+00:00|Z)$",
                        },
                        "end_datetime": {
                            "title": "End Date and Time",
                            "description": "The searchable end date/time of the assets, in UTC (Formatted in RFC 3339) ",
                            "type": "string",
                            "format": "date-time",
                            "pattern": "(\\+00:00|Z)$",
                        },
                        "gsd": {
                            "title": "Ground Sample Distance",
                            "type": "number",
                            "exclusiveMinimum": 0,
                        },
                        "instruments": {
                            "title": "Instruments",
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "license": {"type": "string", "pattern": "^[\\w\\-\\.\\+]+$"},
                        "mission": {"title": "Mission", "type": "string"},
                        "platform": {"title": "Platform", "type": "string"},
                        "providers": {
                            "title": "Providers",
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["name"],
                                "properties": {
                                    "description": {
                                        "title": "Organization description",
                                        "type": "string",
                                    },
                                    "name": {
                                        "title": "Organization name",
                                        "type": "string",
                                        "minLength": 1,
                                    },
                                    "roles": {
                                        "title": "Organization roles",
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "enum": [
                                                "producer",
                                                "licensor",
                                                "processor",
                                                "host",
                                            ],
                                        },
                                    },
                                    "url": {
                                        "title": "Organization homepage",
                                        "type": "string",
                                        "format": "iri",
                                    },
                                },
                            },
                        },
                        "start_datetime": {
                            "title": "Start Date and Time",
                            "description": "The searchable start date/time of the assets, in UTC (Formatted in RFC 3339) ",
                            "type": "string",
                            "format": "date-time",
                            "pattern": "(\\+00:00|Z)$",
                        },
                        "updated": {
                            "title": "Last Update Time",
                            "type": "string",
                            "format": "date-time",
                            "pattern": "(\\+00:00|Z)$",
                        },
                    },
                    "anyOf": [
                        {
                            "required": ["datetime"],
                            "properties": {
                                "datetime": {"not": {"anyOf": [{"type": "null"}]}}
                            },
                        },
                        {"required": ["datetime", "start_datetime", "end_datetime"]},
                    ],
                    "dependencies": {
                        "end_datetime": {"required": ["start_datetime"]},
                        "start_datetime": {"required": ["end_datetime"]},
                    },
                    "oneOf": [{"type": "null"}, {"type": "object"}],
                },
                "assets": {
                    "title": "Asset links",
                    "description": "Links to assets",
                    "type": "object",
                    "additionalProperties": {
                        "title": "Basic Descriptive Fields",
                        "$id": "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/basics.json#",
                        "$schema": "http://json-schema.org/draft-07/schema#",
                        "type": "object",
                        "required": ["href"],
                        "properties": {
                            "title": {
                                "title": "Asset title",
                                "description": "A human-readable title describing the Item.",
                                "type": "string",
                            },
                            "description": {
                                "title": "Asset description",
                                "description": "Detailed multi-line description to fully explain the Item.",
                                "type": "string",
                            },
                            "type": {"title": "Asset type", "type": "string"},
                            "constellation": {
                                "title": "Constellation",
                                "type": "string",
                            },
                            "created": {
                                "title": "Creation Time",
                                "type": "string",
                                "format": "date-time",
                                "pattern": "(\\+00:00|Z)$",
                            },
                            "datetime": {
                                "title": "Date and Time",
                                "description": "The searchable date/time of the assets, in UTC (Formatted in RFC 3339) ",
                                "type": ["string", "null"],
                                "format": "date-time",
                                "pattern": "(\\+00:00|Z)$",
                            },
                            "end_datetime": {
                                "title": "End Date and Time",
                                "description": "The searchable end date/time of the assets, in UTC (Formatted in RFC 3339) ",
                                "type": "string",
                                "format": "date-time",
                                "pattern": "(\\+00:00|Z)$",
                            },
                            "gsd": {
                                "title": "Ground Sample Distance",
                                "type": "number",
                                "exclusiveMinimum": 0,
                            },
                            "href": {
                                "title": "Asset reference",
                                "type": "string",
                                "format": "iri-reference",
                                "minLength": 1,
                            },
                            "instruments": {
                                "title": "Instruments",
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "license": {
                                "type": "string",
                                "pattern": "^[\\w\\-\\.\\+]+$",
                            },
                            "mission": {"title": "Mission", "type": "string"},
                            "platform": {"title": "Platform", "type": "string"},
                            "providers": {
                                "title": "Providers",
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["name"],
                                    "properties": {
                                        "description": {
                                            "title": "Organization description",
                                            "type": "string",
                                        },
                                        "name": {
                                            "title": "Organization name",
                                            "type": "string",
                                            "minLength": 1,
                                        },
                                        "roles": {
                                            "title": "Organization roles",
                                            "type": "array",
                                            "items": {
                                                "type": "string",
                                                "enum": [
                                                    "producer",
                                                    "licensor",
                                                    "processor",
                                                    "host",
                                                ],
                                            },
                                        },
                                        "url": {
                                            "title": "Organization homepage",
                                            "type": "string",
                                            "format": "iri",
                                        },
                                    },
                                },
                            },
                            "roles": {
                                "title": "Asset roles",
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "start_datetime": {
                                "title": "Start Date and Time",
                                "description": "The searchable start date/time of the assets, in UTC (Formatted in RFC 3339) ",
                                "type": "string",
                                "format": "date-time",
                                "pattern": "(\\+00:00|Z)$",
                            },
                            "updated": {
                                "title": "Last Update Time",
                                "type": "string",
                                "format": "date-time",
                                "pattern": "(\\+00:00|Z)$",
                            },
                        },
                        "dependencies": {
                            "end_datetime": {"required": ["start_datetime"]},
                            "start_datetime": {"required": ["end_datetime"]},
                        },
                    },
                },
                "bbox": {"type": "array", "items": {"type": "number"}, "minItems": 4},
                "geometry": {
                    "oneOf": [
                        {"type": "null"},
                        {
                            "title": "GeoJSON Point",
                            "type": "object",
                            "required": ["type", "coordinates"],
                            "properties": {
                                "type": {"type": "string", "enum": ["Point"]},
                                "bbox": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 4,
                                },
                                "coordinates": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 2,
                                },
                            },
                        },
                        {
                            "title": "GeoJSON LineString",
                            "type": "object",
                            "required": ["type", "coordinates"],
                            "properties": {
                                "type": {"type": "string", "enum": ["LineString"]},
                                "bbox": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 4,
                                },
                                "coordinates": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {"type": "number"},
                                        "minItems": 2,
                                    },
                                    "minItems": 2,
                                },
                            },
                        },
                        {
                            "title": "GeoJSON Polygon",
                            "type": "object",
                            "required": ["type", "coordinates"],
                            "properties": {
                                "type": {"type": "string", "enum": ["Polygon"]},
                                "bbox": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 4,
                                },
                                "coordinates": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 2,
                                        },
                                        "minItems": 4,
                                    },
                                },
                            },
                        },
                        {
                            "title": "GeoJSON MultiPoint",
                            "type": "object",
                            "required": ["type", "coordinates"],
                            "properties": {
                                "type": {"type": "string", "enum": ["MultiPoint"]},
                                "bbox": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 4,
                                },
                                "coordinates": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {"type": "number"},
                                        "minItems": 2,
                                    },
                                },
                            },
                        },
                        {
                            "title": "GeoJSON MultiLineString",
                            "type": "object",
                            "required": ["type", "coordinates"],
                            "properties": {
                                "type": {"type": "string", "enum": ["MultiLineString"]},
                                "bbox": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 4,
                                },
                                "coordinates": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 2,
                                        },
                                        "minItems": 2,
                                    },
                                },
                            },
                        },
                        {
                            "title": "GeoJSON MultiPolygon",
                            "type": "object",
                            "required": ["type", "coordinates"],
                            "properties": {
                                "type": {"type": "string", "enum": ["MultiPolygon"]},
                                "bbox": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 4,
                                },
                                "coordinates": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {
                                            "type": "array",
                                            "items": {
                                                "type": "array",
                                                "items": {"type": "number"},
                                                "minItems": 2,
                                            },
                                            "minItems": 4,
                                        },
                                    },
                                },
                            },
                        },
                        {
                            "title": "GeoJSON GeometryCollection",
                            "type": "object",
                            "required": ["type", "geometries"],
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "enum": ["GeometryCollection"],
                                },
                                "bbox": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 4,
                                },
                                "geometries": {
                                    "type": "array",
                                    "items": {
                                        "oneOf": [
                                            {
                                                "title": "GeoJSON Point",
                                                "type": "object",
                                                "required": ["type", "coordinates"],
                                                "properties": {
                                                    "type": {
                                                        "type": "string",
                                                        "enum": ["Point"],
                                                    },
                                                    "bbox": {
                                                        "type": "array",
                                                        "items": {"type": "number"},
                                                        "minItems": 4,
                                                    },
                                                    "coordinates": {
                                                        "type": "array",
                                                        "items": {"type": "number"},
                                                        "minItems": 2,
                                                    },
                                                },
                                            },
                                            {
                                                "title": "GeoJSON LineString",
                                                "type": "object",
                                                "required": ["type", "coordinates"],
                                                "properties": {
                                                    "type": {
                                                        "type": "string",
                                                        "enum": ["LineString"],
                                                    },
                                                    "bbox": {
                                                        "type": "array",
                                                        "items": {"type": "number"},
                                                        "minItems": 4,
                                                    },
                                                    "coordinates": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "array",
                                                            "items": {"type": "number"},
                                                            "minItems": 2,
                                                        },
                                                        "minItems": 2,
                                                    },
                                                },
                                            },
                                            {
                                                "title": "GeoJSON Polygon",
                                                "type": "object",
                                                "required": ["type", "coordinates"],
                                                "properties": {
                                                    "type": {
                                                        "type": "string",
                                                        "enum": ["Polygon"],
                                                    },
                                                    "bbox": {
                                                        "type": "array",
                                                        "items": {"type": "number"},
                                                        "minItems": 4,
                                                    },
                                                    "coordinates": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "array",
                                                                "items": {
                                                                    "type": "number"
                                                                },
                                                                "minItems": 2,
                                                            },
                                                            "minItems": 4,
                                                        },
                                                    },
                                                },
                                            },
                                            {
                                                "title": "GeoJSON MultiPoint",
                                                "type": "object",
                                                "required": ["type", "coordinates"],
                                                "properties": {
                                                    "type": {
                                                        "type": "string",
                                                        "enum": ["MultiPoint"],
                                                    },
                                                    "bbox": {
                                                        "type": "array",
                                                        "items": {"type": "number"},
                                                        "minItems": 4,
                                                    },
                                                    "coordinates": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "array",
                                                            "items": {"type": "number"},
                                                            "minItems": 2,
                                                        },
                                                    },
                                                },
                                            },
                                            {
                                                "title": "GeoJSON MultiLineString",
                                                "type": "object",
                                                "required": ["type", "coordinates"],
                                                "properties": {
                                                    "type": {
                                                        "type": "string",
                                                        "enum": ["MultiLineString"],
                                                    },
                                                    "bbox": {
                                                        "type": "array",
                                                        "items": {"type": "number"},
                                                        "minItems": 4,
                                                    },
                                                    "coordinates": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "array",
                                                                "items": {
                                                                    "type": "number"
                                                                },
                                                                "minItems": 2,
                                                            },
                                                            "minItems": 2,
                                                        },
                                                    },
                                                },
                                            },
                                            {
                                                "title": "GeoJSON MultiPolygon",
                                                "type": "object",
                                                "required": ["type", "coordinates"],
                                                "properties": {
                                                    "type": {
                                                        "type": "string",
                                                        "enum": ["MultiPolygon"],
                                                    },
                                                    "bbox": {
                                                        "type": "array",
                                                        "items": {"type": "number"},
                                                        "minItems": 4,
                                                    },
                                                    "coordinates": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "array",
                                                                "items": {
                                                                    "type": "array",
                                                                    "items": {
                                                                        "type": "number"
                                                                    },
                                                                    "minItems": 2,
                                                                },
                                                                "minItems": 4,
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        ]
                                    },
                                },
                            },
                        },
                    ]
                },
                "id": {
                    "title": "Provider ID",
                    "description": "Provider item ID",
                    "type": "string",
                    "minLength": 1,
                    "oneOf": [{"type": "number"}, {"type": "string"}],
                },
                "links": {
                    "title": "Item links",
                    "description": "Links to item relations",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["rel", "href"],
                        "properties": {
                            "title": {"title": "Link title", "type": "string"},
                            "type": {"title": "Link type", "type": "string"},
                            "href": {
                                "title": "Link reference",
                                "type": "string",
                                "format": "iri-reference",
                                "minLength": 1,
                            },
                            "rel": {
                                "title": "Link relation type",
                                "type": "string",
                                "minLength": 1,
                            },
                        },
                    },
                },
                "stac_extensions": {
                    "title": "STAC extensions",
                    "type": "array",
                    "items": {
                        "title": "Reference to a JSON Schema",
                        "type": "string",
                        "format": "iri",
                    },
                    "uniqueItems": True,
                },
                "stac_version": {
                    "title": "STAC version",
                    "type": "string",
                    "const": "1.0.0",
                },
            },
            "else": {"properties": {"collection": {"not": {}}}},
            "if": {
                "properties": {
                    "links": {
                        "contains": {
                            "required": ["rel"],
                            "properties": {"rel": {"const": "collection"}},
                        }
                    }
                }
            },
            "oneOf": [
                {
                    "type": "object",
                    "required": ["geometry", "bbox"],
                    "properties": {
                        "bbox": {
                            "type": "array",
                            "items": {"type": "number"},
                            "oneOf": [
                                {"maxItems": 4, "minItems": 4},
                                {"maxItems": 6, "minItems": 6},
                            ],
                        },
                        "geometry": {
                            "title": "GeoJSON Geometry",
                            "$id": "https://geojson.org/schema/Geometry.json",
                            "$schema": "http://json-schema.org/draft-07/schema#",
                            "oneOf": [
                                {
                                    "title": "GeoJSON Point",
                                    "type": "object",
                                    "required": ["type", "coordinates"],
                                    "properties": {
                                        "type": {"type": "string", "enum": ["Point"]},
                                        "bbox": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 4,
                                        },
                                        "coordinates": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 2,
                                        },
                                    },
                                },
                                {
                                    "title": "GeoJSON LineString",
                                    "type": "object",
                                    "required": ["type", "coordinates"],
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": ["LineString"],
                                        },
                                        "bbox": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 4,
                                        },
                                        "coordinates": {
                                            "type": "array",
                                            "items": {
                                                "type": "array",
                                                "items": {"type": "number"},
                                                "minItems": 2,
                                            },
                                            "minItems": 2,
                                        },
                                    },
                                },
                                {
                                    "title": "GeoJSON Polygon",
                                    "type": "object",
                                    "required": ["type", "coordinates"],
                                    "properties": {
                                        "type": {"type": "string", "enum": ["Polygon"]},
                                        "bbox": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 4,
                                        },
                                        "coordinates": {
                                            "type": "array",
                                            "items": {
                                                "type": "array",
                                                "items": {
                                                    "type": "array",
                                                    "items": {"type": "number"},
                                                    "minItems": 2,
                                                },
                                                "minItems": 4,
                                            },
                                        },
                                    },
                                },
                                {
                                    "title": "GeoJSON MultiPoint",
                                    "type": "object",
                                    "required": ["type", "coordinates"],
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": ["MultiPoint"],
                                        },
                                        "bbox": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 4,
                                        },
                                        "coordinates": {
                                            "type": "array",
                                            "items": {
                                                "type": "array",
                                                "items": {"type": "number"},
                                                "minItems": 2,
                                            },
                                        },
                                    },
                                },
                                {
                                    "title": "GeoJSON MultiLineString",
                                    "type": "object",
                                    "required": ["type", "coordinates"],
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": ["MultiLineString"],
                                        },
                                        "bbox": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 4,
                                        },
                                        "coordinates": {
                                            "type": "array",
                                            "items": {
                                                "type": "array",
                                                "items": {
                                                    "type": "array",
                                                    "items": {"type": "number"},
                                                    "minItems": 2,
                                                },
                                                "minItems": 2,
                                            },
                                        },
                                    },
                                },
                                {
                                    "title": "GeoJSON MultiPolygon",
                                    "type": "object",
                                    "required": ["type", "coordinates"],
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": ["MultiPolygon"],
                                        },
                                        "bbox": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 4,
                                        },
                                        "coordinates": {
                                            "type": "array",
                                            "items": {
                                                "type": "array",
                                                "items": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "array",
                                                        "items": {"type": "number"},
                                                        "minItems": 2,
                                                    },
                                                    "minItems": 4,
                                                },
                                            },
                                        },
                                    },
                                },
                            ],
                        },
                    },
                },
                {
                    "type": "object",
                    "required": ["geometry"],
                    "properties": {
                        "bbox": {"not": {"anyOf": [{}]}},
                        "geometry": {"type": "null"},
                    },
                },
            ],
            "then": {
                "required": ["collection"],
                "properties": {
                    "collection": {
                        "title": "Collection ID",
                        "description": "The ID of the STAC Collection this Item references to.",
                        "type": "string",
                        "minLength": 1,
                    }
                },
            },
        },
        "link": {
            "type": "object",
            "required": ["rel", "href"],
            "properties": {
                "title": {"title": "Link title", "type": "string"},
                "type": {"title": "Link type", "type": "string"},
                "href": {
                    "title": "Link reference",
                    "type": "string",
                    "format": "iri-reference",
                    "minLength": 1,
                },
                "rel": {
                    "title": "Link relation type",
                    "type": "string",
                    "minLength": 1,
                },
            },
        },
    },
    "else": {"properties": {"collection": {"not": {}}}},
    "if": {
        "properties": {
            "links": {
                "contains": {
                    "required": ["rel"],
                    "properties": {"rel": {"const": "collection"}},
                }
            }
        }
    },
    "oneOf": [
        {
            "type": "object",
            "required": ["geometry", "bbox"],
            "properties": {
                "bbox": {
                    "type": "array",
                    "items": {"type": "number"},
                    "oneOf": [
                        {"maxItems": 4, "minItems": 4},
                        {"maxItems": 6, "minItems": 6},
                    ],
                },
                "geometry": {
                    "title": "GeoJSON Geometry",
                    "$id": "https://geojson.org/schema/Geometry.json",
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "oneOf": [
                        {
                            "title": "GeoJSON Point",
                            "type": "object",
                            "required": ["type", "coordinates"],
                            "properties": {
                                "type": {"type": "string", "enum": ["Point"]},
                                "bbox": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 4,
                                },
                                "coordinates": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 2,
                                },
                            },
                        },
                        {
                            "title": "GeoJSON LineString",
                            "type": "object",
                            "required": ["type", "coordinates"],
                            "properties": {
                                "type": {"type": "string", "enum": ["LineString"]},
                                "bbox": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 4,
                                },
                                "coordinates": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {"type": "number"},
                                        "minItems": 2,
                                    },
                                    "minItems": 2,
                                },
                            },
                        },
                        {
                            "title": "GeoJSON Polygon",
                            "type": "object",
                            "required": ["type", "coordinates"],
                            "properties": {
                                "type": {"type": "string", "enum": ["Polygon"]},
                                "bbox": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 4,
                                },
                                "coordinates": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 2,
                                        },
                                        "minItems": 4,
                                    },
                                },
                            },
                        },
                        {
                            "title": "GeoJSON MultiPoint",
                            "type": "object",
                            "required": ["type", "coordinates"],
                            "properties": {
                                "type": {"type": "string", "enum": ["MultiPoint"]},
                                "bbox": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 4,
                                },
                                "coordinates": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {"type": "number"},
                                        "minItems": 2,
                                    },
                                },
                            },
                        },
                        {
                            "title": "GeoJSON MultiLineString",
                            "type": "object",
                            "required": ["type", "coordinates"],
                            "properties": {
                                "type": {"type": "string", "enum": ["MultiLineString"]},
                                "bbox": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 4,
                                },
                                "coordinates": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 2,
                                        },
                                        "minItems": 2,
                                    },
                                },
                            },
                        },
                        {
                            "title": "GeoJSON MultiPolygon",
                            "type": "object",
                            "required": ["type", "coordinates"],
                            "properties": {
                                "type": {"type": "string", "enum": ["MultiPolygon"]},
                                "bbox": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 4,
                                },
                                "coordinates": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {
                                            "type": "array",
                                            "items": {
                                                "type": "array",
                                                "items": {"type": "number"},
                                                "minItems": 2,
                                            },
                                            "minItems": 4,
                                        },
                                    },
                                },
                            },
                        },
                    ],
                },
            },
        },
        {
            "type": "object",
            "required": ["geometry"],
            "properties": {
                "bbox": {"not": {"anyOf": [{}]}},
                "geometry": {"type": "null"},
            },
        },
    ],
    "then": {
        "required": ["collection"],
        "properties": {
            "collection": {
                "title": "Collection ID",
                "description": "The ID of the STAC Collection this Item references to.",
                "type": "string",
                "minLength": 1,
            }
        },
    },
}
