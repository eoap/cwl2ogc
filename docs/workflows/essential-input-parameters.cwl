#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: CommandLineTool
id: inp
baseCommand: echo
inputs:
  example_flag:
    label: example_flag label
    doc: example_flag doc
    type: boolean
    inputBinding:
      position: 1
      prefix: -f

  example_string:
    label: example_string label
    doc: example_string doc
    type: string
    inputBinding:
      position: 3
      prefix: --example-string

  example_int:
    label: example_int label
    doc: example_int doc
    type: int
    inputBinding:
      position: 2
      prefix: -i
      separate: false

  example_file:
    label: example_file label
    doc: example_file doc
    type: File?
    inputBinding:
      prefix: --file=
      separate: false
      position: 4

  example_enum:
    label: example_enum label
    doc: example_enum doc
    type:
      type: enum
      symbols:
      - auto
      - fasta
      - fastq
      - fasta.gz
      - fastq.gz
    default: auto
    inputBinding:
      prefix: --format
      separate: false
      position: 5

outputs: []
