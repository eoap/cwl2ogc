# CWL Worflow inputs/outputs to OGC API Processes inputs/outputs

The OGC API - Processes Part 2: Deploy, Replace, Undeploy (DRU) specification enables the deployment of executable Application Packages, such as CWL workflows, as processing services. 

A key part of the deploy operation involves parsing the CWL document to generate an OGC-compliant process description, exposing the workflow’s inputs and outputs.

The **cwl2ogc** Python library is a helper library to automate the conversion of CWL input/output definitions into OGC API - Processes input/output schemas.

## The library:

* Parses a CWL Workflow document.

* Extracts and interprets its inputs and outputs.

* Converts them to the structure required for input and output definitions in OGC API - Processes (JSON Schema-like structure, including metadata such as title, description, schema, etc.).

* Supports common CWL types (File, Directory, string, int, float, arrays, optional types, custom types etc.) and map them to OGC API Process I/O types.

* Handles CWL input binding attributes (e.g., default values, required vs. optional) to enrich the process description.

Provides utilities to assist with:

* `GET /processes/{id}` (i.e. process description generation)

* `POST /processes` (i.e. deployment flow)

This library may be useful for OGC API - Processes implementations that support deploying CWL Workflows as execution units, helping bridge the gap between CWL syntax and the standardized OGC process interface.
