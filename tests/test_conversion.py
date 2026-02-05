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

import json
import os
import unittest
import yaml
from cwl2ogc import BaseCWLtypes2OGCConverter
from cwl_utils.parser import load_document_by_yaml
from loguru import logger

class TestConversion(unittest.TestCase):

    def setUp(self):
        return super().setUp()

    def serialize_io(self, converter, workflow):
        logger.info(f"* OGC Processes API representation of '{workflow.id}' inputs:")
        inputs = converter._to_ogc(workflow.inputs)
        print(json.dumps(inputs))

        logger.info(f"* OGC Processes API representation of '{workflow.id}' outputs:")
        outputs = converter._to_ogc(workflow.outputs)
        print(json.dumps(outputs))

    def print_io(self, file):
        logger.info(f"processing {file}...")
        with open(file) as f:
            cwl_content = yaml.load(f, Loader=yaml.SafeLoader)
        cwl = load_document_by_yaml(yaml=cwl_content, uri="io://", load_all=True)

        converter = BaseCWLtypes2OGCConverter(cwl)

        if isinstance(cwl, list):
            for workflow in cwl:
                self.serialize_io(converter, workflow)
        else:
            self.serialize_io(converter, cwl)

    def test_inp(self):
        self.print_io("./tests/artifacts/cwl-types/inp.cwl")

    def test_array_inputs(self):
        self.print_io("./tests/artifacts/cwl-types/array-inputs.cwl")

    def test_record(self):
        self.print_io("./tests/artifacts/cwl-types/record.cwl")

    def test_exclusive_parameter_expressions(self):
        self.print_io("./tests/artifacts/cwl-types/exclusive-parameter-expressions.cwl")

    def test_water_bodies(self):
        self.print_io("./tests/artifacts/app-water-body.1.1.0.cwl")

    def test_complex_cwl_types(self):
        self.print_io("./tests/artifacts/cwl-types/complex-cwl-types.cwl")

    def test_app(self):
        self.print_io("./tests/artifacts/cwl-types/app.cwl")

    def test_string_formats(self):
        self.print_io("./tests/artifacts/cwl-types/string-formats.cwl")
