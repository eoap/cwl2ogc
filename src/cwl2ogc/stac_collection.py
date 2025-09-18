"""
CWL2OGC (c) 2025

CWL2OGC is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

STAC_COLLECTION_SCHEMA = {
    "title": "STAC Collection Specification",
    "description": "This object represents Collections in a SpatioTemporal Asset Catalog.",
    "$id": "https://schemas.stacspec.org/v1.0.0/collection-spec/json-schema/collection.json#",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": [
        "stac_version",
        "type",
        "id",
        "description",
        "license",
        "extent",
        "links",
    ],
    "properties": {
        "title": {"title": "Title", "type": "string"},
        "description": {"title": "Description", "type": "string", "minLength": 1},
        "type": {"title": "Type of STAC entity", "const": "Collection"},
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
        "extent": {
            "title": "Extents",
            "type": "object",
            "required": ["spatial", "temporal"],
            "properties": {
                "spatial": {
                    "title": "Spatial extent object",
                    "type": "object",
                    "required": ["bbox"],
                    "properties": {
                        "bbox": {
                            "title": "Spatial extents",
                            "type": "array",
                            "items": {
                                "title": "Spatial extent",
                                "type": "array",
                                "items": {"type": "number"},
                                "oneOf": [
                                    {"maxItems": 4, "minItems": 4},
                                    {"maxItems": 6, "minItems": 6},
                                ],
                            },
                            "minItems": 1,
                        }
                    },
                },
                "temporal": {
                    "title": "Temporal extent object",
                    "type": "object",
                    "required": ["interval"],
                    "properties": {
                        "interval": {
                            "title": "Temporal extents",
                            "type": "array",
                            "items": {
                                "title": "Temporal extent",
                                "type": "array",
                                "items": {
                                    "type": ["string", "null"],
                                    "format": "date-time",
                                    "pattern": "(\\+00:00|Z)$",
                                },
                                "maxItems": 2,
                                "minItems": 2,
                            },
                            "minItems": 1,
                        }
                    },
                },
            },
        },
        "id": {"title": "Identifier", "type": "string", "minLength": 1},
        "keywords": {"title": "Keywords", "type": "array", "items": {"type": "string"}},
        "license": {
            "title": "Collection License Name",
            "type": "string",
            "pattern": "^[\\w\\-\\.\\+]+$",
        },
        "links": {
            "title": "Links",
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
        "providers": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name"],
                "properties": {
                    "description": {
                        "title": "Organization description",
                        "type": "string",
                    },
                    "name": {"title": "Organization name", "type": "string"},
                    "roles": {
                        "title": "Organization roles",
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["producer", "licensor", "processor", "host"],
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
        "summaries": {
            "type": "object",
            "additionalProperties": {
                "anyOf": [
                    {
                        "title": "JSON Schema",
                        "type": "object",
                        "minProperties": 1,
                        "allOf": {"$ref": "http://json-schema.org/draft-07/schema"},
                    },
                    {
                        "title": "Range",
                        "type": "object",
                        "required": ["minimum", "maximum"],
                        "properties": {
                            "maximum": {
                                "title": "Maximum value",
                                "type": ["number", "string"],
                            },
                            "minimum": {
                                "title": "Minimum value",
                                "type": ["number", "string"],
                            },
                        },
                    },
                    {
                        "title": "Set of values",
                        "type": "array",
                        "items": {
                            "description": "For each field only the original data type of the property can occur (except for arrays), but we can't validate that in JSON Schema yet. See the sumamry description in the STAC specification for details."
                        },
                        "minItems": 1,
                    },
                ]
            },
        },
    },
    "definitions": {
        "collection": {
            "title": "STAC Collection",
            "description": "These are the fields specific to a STAC Collection. All other fields are inherited from STAC Catalog.",
            "type": "object",
            "required": [
                "stac_version",
                "type",
                "id",
                "description",
                "license",
                "extent",
                "links",
            ],
            "properties": {
                "title": {"title": "Title", "type": "string"},
                "description": {
                    "title": "Description",
                    "type": "string",
                    "minLength": 1,
                },
                "type": {"title": "Type of STAC entity", "const": "Collection"},
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
                "extent": {
                    "title": "Extents",
                    "type": "object",
                    "required": ["spatial", "temporal"],
                    "properties": {
                        "spatial": {
                            "title": "Spatial extent object",
                            "type": "object",
                            "required": ["bbox"],
                            "properties": {
                                "bbox": {
                                    "title": "Spatial extents",
                                    "type": "array",
                                    "items": {
                                        "title": "Spatial extent",
                                        "type": "array",
                                        "items": {"type": "number"},
                                        "oneOf": [
                                            {"maxItems": 4, "minItems": 4},
                                            {"maxItems": 6, "minItems": 6},
                                        ],
                                    },
                                    "minItems": 1,
                                }
                            },
                        },
                        "temporal": {
                            "title": "Temporal extent object",
                            "type": "object",
                            "required": ["interval"],
                            "properties": {
                                "interval": {
                                    "title": "Temporal extents",
                                    "type": "array",
                                    "items": {
                                        "title": "Temporal extent",
                                        "type": "array",
                                        "items": {
                                            "type": ["string", "null"],
                                            "format": "date-time",
                                            "pattern": "(\\+00:00|Z)$",
                                        },
                                        "maxItems": 2,
                                        "minItems": 2,
                                    },
                                    "minItems": 1,
                                }
                            },
                        },
                    },
                },
                "id": {"title": "Identifier", "type": "string", "minLength": 1},
                "keywords": {
                    "title": "Keywords",
                    "type": "array",
                    "items": {"type": "string"},
                },
                "license": {
                    "title": "Collection License Name",
                    "type": "string",
                    "pattern": "^[\\w\\-\\.\\+]+$",
                },
                "links": {
                    "title": "Links",
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
                "providers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name"],
                        "properties": {
                            "description": {
                                "title": "Organization description",
                                "type": "string",
                            },
                            "name": {"title": "Organization name", "type": "string"},
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
                "summaries": {
                    "type": "object",
                    "additionalProperties": {
                        "anyOf": [
                            {
                                "title": "JSON Schema",
                                "type": "object",
                                "minProperties": 1,
                            },
                            {
                                "title": "Range",
                                "type": "object",
                                "required": ["minimum", "maximum"],
                                "properties": {
                                    "maximum": {
                                        "title": "Maximum value",
                                        "type": ["number", "string"],
                                    },
                                    "minimum": {
                                        "title": "Minimum value",
                                        "type": ["number", "string"],
                                    },
                                },
                            },
                            {
                                "title": "Set of values",
                                "type": "array",
                                "items": {
                                    "description": "For each field only the original data type of the property can occur (except for arrays), but we can't validate that in JSON Schema yet. See the sumamry description in the STAC specification for details."
                                },
                                "minItems": 1,
                            },
                        ]
                    },
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
        "summaries": {
            "type": "object",
            "additionalProperties": {
                "anyOf": [
                    {"title": "JSON Schema", "type": "object", "minProperties": 1},
                    {
                        "title": "Range",
                        "type": "object",
                        "required": ["minimum", "maximum"],
                        "properties": {
                            "maximum": {
                                "title": "Maximum value",
                                "type": ["number", "string"],
                            },
                            "minimum": {
                                "title": "Minimum value",
                                "type": ["number", "string"],
                            },
                        },
                    },
                    {
                        "title": "Set of values",
                        "type": "array",
                        "items": {
                            "description": "For each field only the original data type of the property can occur (except for arrays), but we can't validate that in JSON Schema yet. See the sumamry description in the STAC specification for details."
                        },
                        "minItems": 1,
                    },
                ]
            },
        },
    },
}
