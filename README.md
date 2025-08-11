# CWL Worflow inputs/outputs to OGC API Processes inputs/outputs

The OGC API - Processes Part 2: Deploy, Replace, Undeploy (DRU) specification enables the deployment of executable Application Packages, such as CWL workflows, as processing services. 

A key part of the deploy operation involves parsing the CWL document to generate an OGC-compliant process description, exposing the workflow’s inputs and outputs.

The **cwl2ogc** Python library is a helper library to automate the conversion of CWL input/output definitions into OGC API - Processes and JSON Schemas

## Using the Playground

**Requirements**

- docker
- task 

**Run the Playground container**

```bash
task run-playground
```

Open the browser at [http://127.0.0.1](http://127.0.0.1)

**Build and run the Playground container** 

```bash
task run-playground-dev
```

Open the browser at [http://127.0.0.1](http://127.0.0.1)

## Contribute

Submit a [Github issue](https://github.com/eoap/cwl2ogc/issues) if you have comments or suggestions.

## Documentation

See the documentation at https://eoap.github.io/cwl2ogc/

## License

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
