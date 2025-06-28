cwlVersion: v1.2

class: CommandLineTool
id: main
inputs:
  - id: color
    label: color label
    doc: color doc
    type:
      type: enum
      symbols:
      - red
      - green
      - blue
    default: "green"
  - id: color1
    label: color1 label
    doc: color1 doc
    type:
    - "null"
    - type: array
      items:
        type: enum
        symbols: [red, green, blue]
  - id: bands 
    label: bands label
    doc: bands doc
    type:
    - 'null'
    - type: array
      items:
        type: array
        items: 
          type: enum
          symbols: [red, green, blue]
  - id: input0 
    label: input0 label
    doc: input0 doc
    type: string
    inputBinding:
      position: 1
  - id: optional_string
    label: optional_string label
    doc: optional_string doc
    type: 
    - "null"
    - string
    default: "default"
  # array of strings
  - id: input1 
    label: input1 label
    doc: input1 doc
    type: string[]
    inputBinding:
      position: 2
  - id: input2 
    label: input2 label
    doc: input2 doc
    type: int[]
    inputBinding:
      position: 2
  # arrays of optional strings
  - id: input3 
    label: input3 label
    doc: input3 doc
    type:
    - type: array
      items: string
    - "null"
  - id: input4
    label: input4 label
    doc: input4 doc
    type:
    - "null"
    - type: enum
      symbols:
        - bam
        - sam
        - bam_mapped
        - sam_mapped
        - fastq
  - id: input5
    label: input5 label
    doc: input5 doc
    type:
    - type: enum
      symbols:
      - bam
      - sam
      - bam_mapped
      - sam_mapped
      - fastq
    default: bam
  - id: thresh
    label: thresh label
    doc: thresh doc
    type:
    - 'null'
    - string
    default: 1.0 mm/day
  - id: option 
    label: option label
    doc: option doc
    type: boolean
    default: true
  - id: option2
    label: option2 label
    doc: option2 doc
    type: boolean?
    default: false
  - id: array_boolean
    label: array_boolean label
    doc: array_boolean doc 
    type:
    - type: array
      items: boolean
    - "null"
outputs: {}
baseCommand: ["echo"]
arguments: [] 
