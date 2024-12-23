# Copyright 2020 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This is the top level module from which all PennyLane-AQT device classes can be directly imported.
"""
from . import ops as ops
from ._version import __version__ as __version__
from .simulator import (
    AQTNoisySimulatorDevice as AQTNoisySimulatorDevice,
)
from .simulator import (
    AQTSimulatorDevice as AQTSimulatorDevice,
)
