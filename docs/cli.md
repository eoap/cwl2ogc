# CLI

Since version `0.10.0`, `cwl2ogc` includes a simple CLI to generate a static _OGC API - Processes_ process descriptor.

## Installation

```
pip install cwl2ogc
```

## Help usage

```
$ cwl2ogc --help
Usage: cwl2ogc [OPTIONS] SOURCE

Options:
  --workflow-id TEXT  ID of the workflow  [required]
  --output PATH       The output file path  [default: process.json]
  --help              Show this message and exit.
```

## Sample execution

```
cwl2ogc \
--workflow-id pattern-1 \
/path/to/pattern-1.cwl

2025-11-04 15:24:31.313 | DEBUG    | cwl2ogc.cli:main:54 - Loading pattern-1 from CWL document on /path/to/pattern-1.cwl...
2025-11-04 15:24:31.332 | DEBUG    | cwl2ogc.cli:main:58 - CWL document from /path/to/pattern-1.cwl successfully load!
2025-11-04 15:24:31.332 | INFO     | cwl2ogc.cli:main:75 - ------------------------------------------------------------------------
2025-11-04 15:24:31.332 | INFO     | cwl2ogc.cli:main:76 - BUILD SUCCESS
2025-11-04 15:24:31.332 | INFO     | cwl2ogc.cli:main:77 - ------------------------------------------------------------------------
2025-11-04 15:24:31.332 | INFO     | cwl2ogc.cli:main:79 - Saving the OCG API - Process to process.json...
2025-11-04 15:24:31.338 | INFO     | cwl2ogc.cli:main:89 - New OCG API - Process successfully saved to process.json!
2025-11-04 15:24:31.338 | INFO     | cwl2ogc.cli:main:93 - Total time: 0.0248 seconds
2025-11-04 15:24:31.338 | INFO     | cwl2ogc.cli:main:94 - Finished at: 2025-11-04T15:24:31.338
```

then

```
vim ./process.json
```
