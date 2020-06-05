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
Alpine Quantum Technologies device class
========================================

This module contains an abstract base class for constructing AQT devices for PennyLane.

"""
import os
import json
from time import sleep

import numpy as np
from pennylane import QubitDevice, DeviceError

from ._version import __version__
from .api_client import verify_valid_status, submit

BASE_SHOTS = 200


class AQTDevice(QubitDevice):
    r"""AQT device for PennyLane.

    Args:
        wires (int): the number of wires to initialize the device with
        shots (int): number of circuit evaluations/random samples used
            to estimate expectation values of observables
        api_key (str): The AQT API key. If not provided, the environment
            variable ``AQT_TOKEN`` is used.
        retry_delay (float): The time (in seconds) to wait between requests
            to the remote server when checking for completion of circuit
            execution.
    """
    # pylint: disable=too-many-instance-attributes
    name = "Alpine Quantum Technologies PennyLane plugin"
    pennylane_requires = ">=0.9.0"
    version = __version__
    author = "Xanadu Inc."
    _capabilities = {
        "model": "qubit",
        "tensor_observables": True,
        "inverse_operations": True,
    }

    short_name = "aqt.base_device"
    _operation_map = {
        # native PennyLane operations also native to AQT
        "RX": "X",
        "RY": "Y",
        "RZ": "Z",
        # operations not natively implemented in AQT
        "BasisState": None,
        "PauliX": None,
        "PauliY": None,
        "PauliZ": None,
        "Hadamard": None,
        "S": None,
        # additional operations not native to PennyLane but present in AQT
        "R": "R",
        "MS": "MS",
    }

    BASE_HOSTNAME = "https://gateway.aqt.eu/marmot"
    TARGET_PATH = ""
    HTTP_METHOD = "PUT"

    def __init__(self, wires, shots=BASE_SHOTS, api_key=None, retry_delay=1):
        super().__init__(wires=wires, shots=shots, analytic=False)
        self.shots = shots
        self._retry_delay = retry_delay

        self._api_key = api_key
        self.set_api_configs()

        self.reset()

    def reset(self):
        """Reset the device and reload configurations."""
        self.circuit = []
        self.circuit_json = ""
        self.samples = None

    def set_api_configs(self):
        """
        Set the configurations needed to connect to AQT API.
        """
        self._api_key = self._api_key or os.getenv("AQT_TOKEN")
        if not self._api_key:
            raise ValueError("No valid api key for AQT platform found.")
        self.header = {"Ocp-Apim-Subscription-Key": self._api_key, "SDK": "pennylane"}
        self.data = {"access_token": self._api_key, "no_qubits": self.num_wires}
        self.hostname = "/".join([self.BASE_HOSTNAME, self.TARGET_PATH])

    @property
    def retry_delay(self):
        """
        The time (in seconds) to wait between requests
        to the remote server when checking for completion of circuit
        execution.

        """
        return self._retry_delay

    @retry_delay.setter
    def retry_delay(self, time):
        """Changes the devices's ``retry_delay`` property.

        Args:
            time (float): time (in seconds) to wait between calls to remote server

        Raises:
            DeviceError: if the retry delay is not a positive number
        """
        if time <= 0:
            raise DeviceError(
                "The specified retry delay needs to be positive. Got {}.".format(time)
            )

        self._retry_delay = float(time)

    @property
    def operations(self):
        """Get the supported set of operations.

        Returns:
            set[str]: the set of PennyLane operation names the device supports
        """
        return set(self._operation_map.keys())

    def apply(self, operations, **kwargs):
        rotations = kwargs.pop("rotations", [])

        for i, operation in enumerate(operations):
            if i > 0 and operation.name in {"BasisState", "QubitStateVector"}:
                raise DeviceError(
                    "The operation {} is only supported at the beginning of a circuit.".format(
                        operation.name
                    )
                )
            self._apply_operation(operation)

        # diagonalize observables
        for operation in rotations:
            self._apply_operation(operation)

        # create circuit job for submission
        self.circuit_json = self.serialize(self.circuit)
        self.data["repetitions"] = self.shots
        job_submission = {**self.data, "data": self.circuit_json}
        response = submit(self.HTTP_METHOD, self.hostname, job_submission, self.header)

        # poll for completed job
        verify_valid_status(response)
        job = response.json()
        job_query_data = {"id": job["id"], "access_token": self._api_key}
        while job["status"] != "finished":
            job = submit(self.HTTP_METHOD, self.hostname, job_query_data, self.header).json()
            sleep(self.retry_delay)

        self.samples = job["samples"]

    def _apply_operation(self, operation):
        """
        Add the specified operation to ``self.circuit`` with the native AQT op name.

        Args:
            operation[pennylane.operation.Operation]: the operation instance to be applied
        """
        op_name = operation.name
        if len(operation.parameters) == 1:
            par = operation.parameters[0]
        elif len(operation.parameters) == 2:
            par = operation.parameters
        else:
            par = None
        wires = operation.wires

        name_parts = op_name.split(".")
        if len(name_parts) == 1:
            op_name = name_parts[0]
            inv = False
        elif len(name_parts) == 2 and name_parts[1] == "inv":
            op_name = name_parts[0]
            inv = True

        if op_name == "R":
            if inv:
                par = [-p for p in par]
            self.circuit.append([op_name, par[0], par[1], wires])
            return
        if op_name == "BasisState":
            for bit, wire in zip(par, wires):
                if bit == 1:
                    self._append_op_to_queue("RX", np.pi, wires=[wire])
            return
        if op_name == "Hadamard":
            if inv:
                self._append_op_to_queue("RY", np.pi / 2, wires)
                self._append_op_to_queue("RX", np.pi, wires)
            else:
                self._append_op_to_queue("RX", np.pi, wires)
                self._append_op_to_queue("RY", -np.pi / 2, wires)
            return

        if op_name == "S":
            op_name = "RZ"
            par = 0.5 * np.pi
        elif op_name in ("PauliX", "PauliY", "PauliZ"):
            op_name = "R{}".format(op_name[-1])
            par = np.pi
        elif op_name == "MS":
            par *= np.pi

        if inv:
            par *= -1

        self._append_op_to_queue(op_name, par, wires)

    def _append_op_to_queue(self, op_name, par, wires):
        """
        Append the given operation to the circuit queue in the correct format for AQT API.

        Args:
            op_name[str]: the PennyLane name of the op
            par[float]: the numeric parameter value for the op
            wires[list[int]]: the wires the op is to be applied on
        """
        if not op_name in self.operations:
            raise DeviceError("Operation {} is not supported on AQT devices.")
        par = par / np.pi  # AQT convention: all gates differ from PennyLane by factor of pi
        aqt_op_name = self._operation_map[op_name]
        self.circuit.append([aqt_op_name, par, wires])

    @staticmethod
    def serialize(circuit):
        """
        Serialize ``circuit`` to a valid AQT-formatted JSON string.

        Args:
             circuit[list[list]]: a list of lists of the form
                 [["X", 0.3, [0]], ["Z", 0.1, [2]], ...]
        """
        return json.dumps(circuit)

    def generate_samples(self):
        # AQT indexes in reverse scheme to PennyLane, so we have to specify "F" ordering
        samples_array = np.stack(np.unravel_index(self.samples, [2] * self.num_wires, order="F")).T
        return samples_array
