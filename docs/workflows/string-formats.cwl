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

  date-time_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#DateTime

  duration_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Duration

  email_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Email

  hostname_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Hostname

  idn-email_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IDNEmail

  idn-hostname_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IDNHostname

  ipv4_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IPv4

  ipv6_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IPv6

  iri_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IRI

  iri-reference_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IRIReference

  json-pointer_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#JsonPointer
  
  password_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Password

  relative-json-pointer_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#RelativeJsonPointer

  uuid_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#UUID

  uri_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI

  uri-reference_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference

  uri-template_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate

  time_input:
    type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time

outputs:
  echo_output:
    type: stdout

stdout: echo_output.txt
