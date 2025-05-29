#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: CommandLineTool
id: array-inputs
inputs:
  filesA:
    label: filesA label
    doc: filesA doc
    type: string[]
    inputBinding:
      prefix: -A
      position: 1

  filesB:
    label: filesB label
    doc: filesB doc
    type:
      type: array
      items: string
      inputBinding:
        prefix: -B=
        separate: false
    inputBinding:
      position: 2

  filesC:
    label: filesC label
    doc: filesC doc
    type: string[]
    inputBinding:
      prefix: -C=
      itemSeparator: ","
      separate: false
      position: 4

outputs:
  example_out:
    type: stdout
stdout: output.txt
baseCommand: echo
