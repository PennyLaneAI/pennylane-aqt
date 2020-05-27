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
"""
AQT Simulator Devices
=====================

**Module name:** :mod:`pennylane_aqt.simulator`

.. currentmodule:: pennylane_aqt.simulator

Classes
-------

.. autosummary::
   AQTSimulatorDevice
   AQTNoisySimulatorDevice

----
"""

from .device import AQTDevice


class AQTSimulatorDevice(AQTDevice):
    r"""AQTSimulatorDevice for PennyLane.

    This device runs simulations on the backend provided at the address
    https://gateway.aqt.eu/marmot/sim

    Args:
        wires (int): the number of wires to initialize the device with
        shots (int): number of circuit evaluations/random samples used
            to estimate expectation values of observables
        api_key (str): The AQT API key. If not provided, the environment
            variable ``AQT_TOKEN`` is used.

    """
    name = "AQT Simulator device for PennyLane"
    short_name = "pennylane_aqt.Simulator"

    TARGET_PATH = "sim"


class AQTNoisySimulatorDevice(AQTDevice):
    r"""AQTNoisySimulatorDevice for PennyLane.

    This device runs simulations on the backend provided at the address
    https://gateway.aqt.eu/marmot/sim/noise-model-1

    Args:
        wires (int): the number of wires to initialize the device with
        shots (int): number of circuit evaluations/random samples used
            to estimate expectation values of observables
        api_key (str): The AQT API key. If not provided, the environment
            variable ``AQT_TOKEN`` is used.
    """
    name = "AQT Noisy Simulator device for PennyLane"
    short_name = "pennylane_aqt.NoisySimulator"

    TARGET_PATH = "sim/noise-model-1"
