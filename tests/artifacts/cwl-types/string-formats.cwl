cwlVersion: v1.2
class: CommandLineTool
id: main
label: "Echo OGC BBox"
baseCommand: echo

requirements:
  InlineJavascriptRequirement: {}
  SchemaDefRequirement:
    types:
    - $import: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml

inputs:

  date_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Date
    label: 'Expected schema serialization: { "type": "string", "format": ""date" }'

  date-time_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#DateTime
    label: 'Expected schema serialization: { "type": "string", "format": "date-time" }'

  duration_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Duration
    label: 'Expected schema serialization: { "type": "string", "format": "duration" }'

  email_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Email
    label: 'Expected schema serialization: { "type": "string", "format": "email" }'

  hostname_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Hostname
    label: 'Expected schema serialization: { "type": "string", "format": "hostname" }'

  idn-email_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IDNEmail
    label: 'Expected schema serialization: { "type": "string", "format": "idn-email" }'

  idn-hostname_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IDNHostname
    label: 'Expected schema serialization: { "type": "string", "format": "idn-hostname" }'

  ipv4_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IPv4
    label: 'Expected schema serialization: { "type": "string", "format": "ipv4" }'

  ipv6_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IPv6
    label: 'Expected schema serialization: { "type": "string", "format": "ipv6" }'

  iri_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IRI
    label: 'Expected schema serialization: { "type": "string", "format": "iri" }'

  iri-reference_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IRIReference
    label: 'Expected schema serialization: { "type": "string", "format": "iri-reference" }'

  json-pointer_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#JsonPointer
    label: 'Expected schema serialization: { "type": "string", "format": "json-pointer" }'
  
  password_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Password
    label: 'Expected schema serialization: { "type": "string", "format": "password" }'

  relative-json-pointer_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#RelativeJsonPointer
    label: 'Expected schema serialization: { "type": "string", "format": "relative-json-pointer" }'

  uuid_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#UUID
    label: 'Expected schema serialization: { "type": "string", "format": "uuid" }'

  uri_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
    label: 'Expected schema serialization: { "type": "string", "format": "uri" }'

  uri-reference_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference
    label: 'Expected schema serialization: { "type": "string", "format": "uri-reference" }'

  uri-template_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate
    label: 'Expected schema serialization: { "type": "string", "format": "uri-template" }'

  time_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time
    label: 'Expected schema serialization: { "type": "string", "format": "time" }'

outputs:
  echo_output:
    type: stdout

stdout: echo_output.txt
