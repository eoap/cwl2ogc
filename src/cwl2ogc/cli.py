"""
CWL2OGC (c) 2025

CWL2OGC is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from . import BaseCWLtypes2OGCConverter
from cwl_utils.parser import (
    load_document_by_uri,
    Process
)
from datetime import datetime
from loguru import logger
from pathlib import Path

import click
import json
import time  

@click.command(context_settings={'show_default': True})
@click.argument(
    'source',
    type=click.Path(
        path_type=Path,
        exists=True,
        readable=True,
        resolve_path=True
    ),
    required=True
)
@click.option(
    '--workflow-id',
    required=True,
    help="ID of the workflow"
)
@click.option(
    '--output',
    type=click.Path(path_type=Path),
    required=False,
    default='process.json',
    help="The output file path"
)
def main(
    source: Path,
    workflow_id: str,
    output: Path
):
    start_time = time.time()

    logger.debug(f"Loading {workflow_id} from CWL document on {source}...")

    workflow: Process = load_document_by_uri(f"{source}#{workflow_id}")

    logger.debug(f"CWL document from {source} successfully load!")

    cwl_converter = BaseCWLtypes2OGCConverter(workflow)

    data = {
        'id': workflow.id.split('#')[-1],
        'version': workflow.cwlVersion,
        'inputs': cwl_converter.get_inputs(),
        'outputs': cwl_converter.get_outputs()
    }

    if workflow.label:
        data['title'] = workflow.label

    if workflow.doc:
        data['description'] = workflow.doc

    logger.info('------------------------------------------------------------------------')
    logger.info('BUILD SUCCESS')
    logger.info('------------------------------------------------------------------------')

    logger.info(f"Saving the OCG API - Process to {output}...")

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w') as output_stream:
        json.dump(
            data,
            output_stream,
            indent=2,   
        )

    logger.info(f"New OCG API - Process successfully saved to {output}!")

    end_time = time.time()

    logger.info(f"Total time: {end_time - start_time:.4f} seconds")
    logger.info(f"Finished at: {datetime.fromtimestamp(end_time).isoformat(timespec='milliseconds')}")

