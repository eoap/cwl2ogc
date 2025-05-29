#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: CommandLineTool
id: record
inputs:
  dependent_parameters:
    label: dependent_parameters label
    doc: dependent_parameters doc
    type:
      type: record
      name: dependent_parameters
      fields:
        itemA:
          type: string
          inputBinding:
            prefix: -A
        itemB:
          type: string
          inputBinding:
            prefix: -B
  exclusive_parameters:
    label: dependent_parameters label
    doc: dependent_parameters doc
    type:
      - type: record
        name: itemC
        fields:
          itemC:
            type: string
            inputBinding:
              prefix: -C
      - type: record
        name: itemD
        fields:
          itemD:
            type: string
            inputBinding:
              prefix: -D
outputs:
  example_out:
    type: stdout
stdout: output.txt
baseCommand: echo
