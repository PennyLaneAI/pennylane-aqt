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
# ruff: noqa: D205
"""Alpine Quantum Technologies device class.
========================================

This module contains an abstract base class for constructing AQT devices for PennyLane.

"""
import json
import os
from time import sleep

import numpy as np
from pennylane import DeviceError
from pennylane.devices import QubitDevice
from pennylane.ops import Adjoint

from ._version import __version__
from .api_client import submit, verify_valid_status

BASE_SHOTS = 200


class AQTDevice(QubitDevice):
    r"""AQT device for PennyLane.

    Args:
        wires (int or Iterable[Number, str]]): Number of subsystems represented by the device,
            or iterable that contains unique number labels for the subsystems (i.e., ``[-1, 0, 2]``)
            or strings (``['ancilla', 'q1', 'q2']``).
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
    pennylane_requires = ">=0.38.0"
    version = __version__
    author = "Xanadu Inc."
    _capabilities = {
        "model": "qubit",
        "tensor_observables": True,
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
        "CNOT": None,
        # additional operations not native to PennyLane but present in AQT
        "R": "R",
        "MS": "MS",
        # adjoint versions of operators are also allowed
        "Adjoint(RX)": None,
        "Adjoint(RY)": None,
        "Adjoint(RZ)": None,
        "Adjoint(PauliX)": None,
        "Adjoint(PauliY)": None,
        "Adjoint(PauliZ)": None,
        "Adjoint(Hadamard)": None,
        "Adjoint(S)": None,
        "Adjoint(CNOT)": None,
        "Adjoint(R)": None,
        "Adjoint(MS)": None,
    }

    BASE_HOSTNAME = "https://gateway.aqt.eu/marmot"
    TARGET_PATH = ""
    HTTP_METHOD = "PUT"

    def __init__(self, wires, shots=BASE_SHOTS, api_key=None, retry_delay=1):
        """Initialize the AQT Device.

        Args:
            wires (int or Iterable[Number, str]]): Number of subsystems represented by the device,
                or iterable that contains unique number labels (i.e., ``[-1, 0, 2]``)
                or strings (``['ancilla', 'q1', 'q2']``).
            shots (int): number of circuit evaluations/random samples used
                to estimate expectation values of observables
            api_key (str): The AQT API key. If not provided, the environment
                variable ``AQT_TOKEN`` is used.
            retry_delay (float): The time (in seconds) to wait between requests
                to the remote server when checking for completion of circuit
                execution.

        Raises:
            ValueError: AQT base device does not support analytic expectation values

        """
        if shots is None:
            raise ValueError(
                "The aqt.base_device device does not support analytic expectation values",
            )

        super().__init__(wires=wires, shots=shots)
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
        """Set the configurations needed to connect to AQT API.

        Raises:
            ValueError: if no valid api key for the AQT platform is found

        """
        self._api_key = self._api_key or os.getenv("AQT_TOKEN")
        if not self._api_key:
            raise ValueError("No valid api key for AQT platform found.")
        self.header = {"Ocp-Apim-Subscription-Key": self._api_key, "SDK": "pennylane"}
        self.data = {"access_token": self._api_key, "no_qubits": self.num_wires}
        self.hostname = f"{self.BASE_HOSTNAME}/{self.TARGET_PATH}"

    @property
    def retry_delay(self):
        """The time (in seconds) to wait between requests to the remote server."""
        return self._retry_delay

    @retry_delay.setter
    def retry_delay(self, time):
        """Change devices's ``retry_delay`` property.

        Args:
            time (float): time (in seconds) to wait between calls to remote server

        Raises:
            DeviceError: if the retry delay is not a positive number

        """
        if time <= 0:
            msg = f"The specified retry delay needs to be positive. Got {time}."
            raise DeviceError(
                msg,
            )

        self._retry_delay = float(time)

    @property
    def operations(self):
        """Get the supported set of operations.

        Returns:
            set[str]: the set of PennyLane operation names the device supports

        """
        return set(self._operation_map.keys())

    # ruff: noqa: D417
    def apply(self, operations, **kwargs):
        """Apply quantum operations, rotate the circuit into the measurement
        basis, and compile and execute the quantum circuit.

        This method receives a list of quantum operations queued by the QNode,
        and should be responsible for:

        * Constructing the quantum program
        * (Optional) Rotating the quantum circuit using the rotation
          operations provided. This diagonalizes the circuit so that arbitrary
          observables can be measured in the computational basis.
        * Compile the circuit
        * Execute the quantum circuit

        Both arguments are provided as lists of PennyLane :class:`~.Operation`
        instances. Useful properties include :attr:`~.Operation.name`,
        :attr:`~.Operation.wires`, and :attr:`~.Operation.parameters`:

        >>> op = qml.RX(0.2, wires=[0])
        >>> op.name # returns the operation name
        "RX"
        >>> op.wires # returns a Wires object representing the wires that the operation acts on
        Wires([0])
        >>> op.parameters # returns a list of parameters
        [0.2]

        Args:
            operations (list[~.Operation]): operations to apply to the device

        Keyword Args:
            rotations (list[~.Operation]): operations that rotate the circuit
                pre-measurement into the eigenbasis of the observables.
            hash (int): the hash value of the circuit constructed by `CircuitGraph.hash`

        Raises:
            DeviceError: If an operation is not where it is supposed to be in the circuit.
            ValueError: If something went wrong with the HTTP request.

        """
        rotations = kwargs.pop("rotations", [])

        for i, operation in enumerate(operations):
            if i > 0 and operation.name in {"BasisState", "StatePrep"}:
                msg = f"Operation {operation.name} is only supported at the beginning of a circuit."
                raise DeviceError(
                    msg,
                )
            self._apply_operation(operation)

        # diagonalize observables
        for operation in rotations:
            self._apply_operation(operation)

        # create circuit job for submission
        # pylint: disable = attribute-defined-outside-init
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

        error_msg = job.get("ERROR", None)

        if error_msg:
            msg = f"Something went wrong with the request, got the error message: {error_msg}"
            raise ValueError(
                msg,
            )

        # pylint: disable = attribute-defined-outside-init
        self.samples = job["samples"]

    # ruff: noqa: PLR0912
    # ruff: noqa: C901
    # pylint: disable = too-many-branches
    def _apply_operation(self, operation):
        """Add the specified operation to ``self.circuit`` with the native AQT op name.

        Args:
            operation (pennylane.operation.Operation): the operation instance to be applied

        """
        op_name = operation.name
        if isinstance(operation, Adjoint):
            op_name = operation.base.name

        if len(operation.parameters) == 1:
            par = operation.parameters[0]
        elif len(operation.parameters) == 2:
            par = operation.parameters
        else:
            par = None

        # translate operation wire labels to the one's used by the device
        device_wires = self.map_wires(operation.wires)
        device_wire_labels = device_wires.tolist()

        if op_name == "R":
            if isinstance(operation, Adjoint):
                par = [-p for p in par]
            self.circuit.append([op_name, par[0], par[1], device_wire_labels])
            return
        if op_name == "BasisState":
            for bit, label in zip(par, device_wire_labels, strict=False):
                if bit == 1:
                    self._append_op_to_queue("RX", np.pi, device_wire_labels=[label])
            return
        if op_name == "Hadamard":
            if isinstance(operation, Adjoint):
                self._append_op_to_queue("RY", np.pi / 2, device_wire_labels)
                self._append_op_to_queue("RX", np.pi, device_wire_labels)
            else:
                self._append_op_to_queue("RX", np.pi, device_wire_labels)
                self._append_op_to_queue("RY", -np.pi / 2, device_wire_labels)
            return
        if op_name == "CNOT":
            self._append_op_to_queue("RY", np.pi / 2, [device_wire_labels[0]])
            self._append_op_to_queue("MS", np.pi / 2, device_wire_labels)
            self._append_op_to_queue("RX", -np.pi / 2, [device_wire_labels[0]])
            self._append_op_to_queue("RX", -np.pi / 2, [device_wire_labels[1]])
            self._append_op_to_queue("RY", -np.pi / 2, [device_wire_labels[0]])
            return
        if op_name == "S":
            op_name = "RZ"
            par = 0.5 * np.pi
        elif op_name in {"PauliX", "PauliY", "PauliZ"}:
            op_name = f"R{op_name[-1]}"
            par = np.pi
        elif op_name == "MS":
            par *= np.pi

        if isinstance(operation, Adjoint):
            par *= -1

        self._append_op_to_queue(op_name, par, device_wire_labels)

    def _append_op_to_queue(self, op_name, par, device_wire_labels):
        """Append the given operation to the circuit queue in the correct format for AQT API.

        Args:
            op_name (str): the PennyLane name of the op
            par (float): the numeric parameter value for the op
            device_wire_labels (list[int]): device wire labels for which the op is to be applied on

        Raises:
            DeviceError: if operation is not supported on AQT devices

        """
        if op_name not in self.operations:
            raise DeviceError("Operation {} is not supported on AQT devices.")
        par /= np.pi  # AQT convention: all gates differ from PennyLane by factor of pi
        aqt_op_name = self._operation_map[op_name]
        self.circuit.append([aqt_op_name, par, device_wire_labels])

    @staticmethod
    def serialize(circuit):
        """Serialize ``circuit`` to a valid AQT-formatted JSON string.

        Args:
            circuit (list[list]): a list of lists of the form
                [["X", 0.3, [0]], ["Z", 0.1, [2]], ...]

        Returns:
            serialized_circuit (str): the serialized circuit as a JSON string.

        """
        return json.dumps(circuit)

    def generate_samples(self):
        r"""Return the computational basis samples generated for all wires.

        Returns:
            array[complex]: array of samples in the shape ``(dev.shots, dev.num_wires)``

        """
        # AQT indexes in reverse scheme to PennyLane, so we have to specify "F" ordering
        return np.stack(np.unravel_index(self.samples, [2] * self.num_wires, order="F")).T
