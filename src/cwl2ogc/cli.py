# Copyright 2025 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from . import BaseCWLtypes2OGCConverter
from cwl_utils.parser import load_document_by_yaml, load_document_by_uri, Process
from datetime import datetime
from loguru import logger
from pathlib import Path
from pydantic import BaseModel
from typing import Any, MutableMapping
from transpiler_mate.metadata import MetadataManager
from transpiler_mate.metadata.software_application_models import SoftwareApplication

import click
import json
import time


@click.command(context_settings={"show_default": True})
@click.argument(
    "source",
    type=click.Path(path_type=Path, exists=True, readable=True, resolve_path=True),
    required=True,
)
@click.option("--workflow-id", required=True, help="ID of the workflow")
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    required=False,
    default="process.json",
    help="The output file path",
)
def main(source: Path, workflow_id: str, output: Path):
    start_time = time.time()

    data: MutableMapping[str, Any] = {}

    logger.debug(f"Loading {workflow_id} from CWL document on {source}...")

    try:
        metadata_manager = MetadataManager(source)
        logger.debug("Serializing Schema.org metadata...")

        metadata: SoftwareApplication = metadata_manager.metadata

        if metadata:
            for attribute in ["name", "description", "software_version", "license"]:
                if hasattr(metadata, attribute):
                    attribute_value = getattr(metadata, attribute, None)
                    if attribute_value:
                        data[attribute] = (
                            attribute_value.model_dump()
                            if isinstance(attribute_value, BaseModel)
                            else attribute_value
                        )

        workflow: Process = load_document_by_yaml(
            yaml=metadata_manager.raw_document,
            uri=source.absolute().as_uri(),
            id_=workflow_id,
        )
    except Exception as e:
        logger.debug(
            f"Schema.org metadata not fully available in {source} due to : {e}"
        )
        workflow: Process = load_document_by_uri(
            f"{source.absolute().as_uri()}#{workflow_id}"
        )

    logger.debug("Serializing CWL Workflow metadata...")

    for attribute in ["id", "label", "doc"]:
        if hasattr(workflow, attribute):
            attribute_value = getattr(workflow, attribute, None)
            if attribute_value:
                data[attribute] = attribute_value.split("#")[-1]

    logger.debug("Serializing inputs and outputs OGC API Process Schema...")

    cwl_converter = BaseCWLtypes2OGCConverter(workflow)

    data["inputs"] = cwl_converter.get_inputs()
    data["outputs"] = cwl_converter.get_outputs()

    logger.success(
        "------------------------------------------------------------------------"
    )
    logger.success("BUILD SUCCESS")
    logger.success(
        "------------------------------------------------------------------------"
    )

    logger.info(f"Saving the OCG API - Process to {output}...")

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w") as output_stream:
        json.dump(
            data,
            output_stream,
            indent=2,
        )

    logger.success(f"New OCG API - Process successfully saved to {output}!")

    end_time = time.time()

    logger.info(f"Total time: {end_time - start_time:.4f} seconds")
    logger.info(
        f"Finished at: {datetime.fromtimestamp(end_time).isoformat(timespec='milliseconds')}"
    )
