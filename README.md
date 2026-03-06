# cwl2ogc

`cwl2ogc` converts CWL workflow/tool inputs and outputs into:
- OGC API - Processes I/O descriptors
- JSON Schema documents for those I/O definitions

This is useful when publishing CWL-based application packages through OGC API - Processes interfaces.

## Why

The OGC API - Processes Deploy/Replace/Undeploy workflow requires a process description that exposes valid input and output metadata. `cwl2ogc` helps generate that description directly from CWL definitions.

## Installation

```bash
pip install cwl2ogc
```

Python `3.10+` is required.

## Quick Start (CLI)

Generate a process descriptor from a CWL document:

```bash
cwl2ogc tests/artifacts/cwl-types/inp.cwl \
  --workflow-id inp \
  --output process.json
```

Show command help:

```bash
cwl2ogc --help
```

## Quick Start (Python API)

```python
from cwl_utils.parser import load_document_by_uri
from cwl2ogc import BaseCWLtypes2OGCConverter

workflow = load_document_by_uri("tests/artifacts/cwl-types/inp.cwl#inp")
converter = BaseCWLtypes2OGCConverter(workflow)

inputs = converter.get_inputs()
outputs = converter.get_outputs()

inputs_json_schema = converter.get_inputs_json_schema()
outputs_json_schema = converter.get_outputs_json_schema()
```

## Playground

Requirements:
- `docker`
- `task`

Run the published playground image:

```bash
task run-playground
```

Build and run the local playground image:

```bash
task run-playground-dev
```

Open [http://127.0.0.1](http://127.0.0.1).

## Development

Install development tooling with Hatch and run checks:

```bash
hatch run test:test-q
hatch run dev:check
hatch run dev:lint
```

Equivalent Taskfile targets:

```bash
task test
task check
task lint
```

## Documentation

Project docs: https://eoap.github.io/cwl2ogc/

CLI docs: [docs/cli.md](docs/cli.md)

## Contributing

Issues and pull requests are welcome:
https://github.com/eoap/cwl2ogc/issues

## License

Apache-2.0. See [LICENSE](LICENSE).
