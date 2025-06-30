# CWL Worflow inputs/outputs to OGC API Processes inputs/outputs

The OGC API - Processes Part 2: Deploy, Replace, Undeploy (DRU) specification enables the deployment of executable Application Packages, such as CWL workflows, as processing services. 

A key part of the deploy operation involves parsing the CWL document to generate an OGC-compliant process description, exposing the workflow’s inputs and outputs.

The **cwl2ogc** Python library is a helper library to automate the conversion of CWL input/output definitions into OGC API - Processes input/output schemas.
 