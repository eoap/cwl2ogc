cwlVersion: v1.2
class: CommandLineTool
id: exclusive-parameter-expressions
inputs:
  file_format:
    label: file_format label
    doc: file_format doc
    type:
      - 'null'
      - name: format_choices
        type: enum
        symbols:
          - auto
          - fasta
          - fastq
          - fasta.gz
          - fastq.gz
        inputBinding:
          position: 0
          prefix: '--format'
outputs:
  text_output:
    type: string
    outputBinding:
      outputEval: $(inputs.file_format)

baseCommand: 'true'
