# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import traceback

import mock
import yaml

from rally.benchmark import engine
import rally.utils as rutils
from tests.unit import test


class RallyJobsTestCase(test.TestCase):
    rally_jobs_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "rally-jobs")

    @mock.patch("rally.benchmark.engine.BenchmarkEngine"
                "._validate_config_semantic")
    def test_schema_is_valid(self, mock_validate):
        rutils.load_plugins(os.path.join(self.rally_jobs_path, "plugins"))

        for filename in ["rally.yaml", "rally-neutron.yaml",
                         "rally-zaqar.yaml", "rally-designate.yaml"]:
            full_path = os.path.join(self.rally_jobs_path, filename)

            with open(full_path) as task_file:
                try:
                    task_config = yaml.safe_load(task_file.read())
                    eng = engine.BenchmarkEngine(task_config,
                                                 mock.MagicMock())
                    eng.validate()
                except Exception:
                    print(traceback.format_exc())
                    self.fail("Wrong task input file: %s" % full_path)
