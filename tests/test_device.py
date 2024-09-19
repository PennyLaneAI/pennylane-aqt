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
"""Tests for the AQTDevice class"""
import os
import pytest
import appdirs
import requests

import pennylane as qml
import numpy as np

import pennylane_aqt.device
from pennylane_aqt import ops
from pennylane_aqt.device import AQTDevice
from pennylane_aqt.simulator import AQTSimulatorDevice, AQTNoisySimulatorDevice

API_HEADER_KEY = "Ocp-Apim-Subscription-Key"
BASE_HOSTNAME = "https://gateway.aqt.eu/marmot"
HTTP_METHOD = "PUT"

SOME_API_KEY = "ABC123"

test_config = """\
[main]
shots = 1000

[default.gaussian]
hbar = 2

[aqt.sim]
shots = 99
api_key = "{}"
""".format(
    SOME_API_KEY
)

# samples obtained directly from AQT platform
# for a three-qubit circuit ([q0, q1, q2])
# which flips qubit qi when there is a 1
REF_SAMPLES_000 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
REF_SAMPLES_001 = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
REF_SAMPLES_010 = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
REF_SAMPLES_011 = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
REF_SAMPLES_100 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
REF_SAMPLES_101 = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
REF_SAMPLES_110 = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
REF_SAMPLES_111 = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7]

MOCK_SAMPLES = [1, 0, 1, 3, 0, 2, 0, 1, 0, 3]


class TestAQTDevice:
    """Tests for the AQTDevice base class."""

    @pytest.mark.parametrize("num_wires", [1, 3])
    @pytest.mark.parametrize("shots", [1, 100])
    @pytest.mark.parametrize("retry_delay", [0.1, 1.0])
    def test_default_init(self, num_wires, shots, retry_delay):
        """Tests that the device is properly initialized."""

        dev = AQTDevice(num_wires, shots, SOME_API_KEY, retry_delay)

        assert dev.num_wires == num_wires
        assert dev.shots == shots
        assert dev.retry_delay == retry_delay
        assert dev.analytic == False
        assert dev.circuit == []
        assert dev.circuit_json == ""
        assert dev.samples is None
        assert dev.BASE_HOSTNAME == BASE_HOSTNAME
        assert dev.HTTP_METHOD == HTTP_METHOD
        assert API_HEADER_KEY in dev.header.keys()
        assert dev.header[API_HEADER_KEY] == SOME_API_KEY

    def test_reset(self):
        """Tests that the ``reset`` method corretly resets data."""

        dev = AQTDevice(3, api_key=SOME_API_KEY)
        assert dev.circuit == []

        dev.circuit = [["RX", 0.5, [0]]]
        dev.circuit_json = "some dummy string"
        dev.samples = [5, 5, 5]
        dev.shots = 55

        dev.reset()

        assert dev.circuit == []
        assert dev.circuit_json == ""
        assert dev.samples == None
        assert dev.shots == 55  # should not be reset

    def test_retry_delay(self):
        """Tests that the ``retry_delay`` property can be set manually."""

        dev = AQTDevice(3, api_key=SOME_API_KEY, retry_delay=2.5)
        assert dev.retry_delay == 2.5

        dev.retry_delay = 1.0
        assert dev.retry_delay == 1.0

        with pytest.raises(qml.DeviceError, match="needs to be positive"):
            dev.retry_delay = -5

    def test_set_api_configs(self):
        """Tests that the ``set_api_configs`` method properly (re)sets the API configs."""

        dev = AQTDevice(3, api_key=SOME_API_KEY)
        new_api_key = "ZZZ000"
        dev._api_key = new_api_key
        dev.BASE_HOSTNAME = "https://server.someaddress.com"
        dev.TARGET_PATH = "some/path"
        dev.set_api_configs()

        assert dev.header == {"Ocp-Apim-Subscription-Key": new_api_key, "SDK": "pennylane"}
        assert dev.data == {"access_token": new_api_key, "no_qubits": dev.num_wires}
        assert dev.hostname == "https://server.someaddress.com/some/path"

    def test_api_key_not_found_error(self, monkeypatch, tmpdir):
        """Tests that an error is thrown with the device is created without
        a valid API token."""

        monkeypatch.setenv("AQT_TOKEN", "")
        monkeypatch.setenv("PENNYLANE_CONF", "")
        monkeypatch.setattr("os.curdir", tmpdir.join("folder_without_a_config_file"))

        monkeypatch.setattr(
            "pennylane.default_config", qml.Configuration("config.toml")
        )  # force loading of config
        with pytest.raises(ValueError, match="No valid api key for AQT platform found"):
            dev = AQTDevice(2)

    @pytest.mark.parametrize(
        "circuit, expected",
        [
            ([["X", 0.33, [1]], ["Y", 1.55, [2]]], '[["X", 0.33, [1]], ["Y", 1.55, [2]]]'),
            ([["MS", 1.2, [0, 1]], ["Y", 1.55, [2]]], '[["MS", 1.2, [0, 1]], ["Y", 1.55, [2]]]'),
            ([["Z", -0.8, [1]]], '[["Z", -0.8, [1]]]'),
        ],
    )
    def test_serialize(self, circuit, expected):
        """Tests that the ``serialize`` static method correctly converts
        from a list of lists into an acceptable JSON string."""
        dev = AQTDevice(3, api_key=SOME_API_KEY)
        res = dev.serialize(circuit)
        assert res == expected

    @pytest.mark.parametrize(
        "samples, indices",
        [
            (REF_SAMPLES_000, [0, 0, 0]),
            (REF_SAMPLES_001, [0, 0, 1]),
            (REF_SAMPLES_010, [0, 1, 0]),
            (REF_SAMPLES_011, [0, 1, 1]),
            (REF_SAMPLES_100, [1, 0, 0]),
            (REF_SAMPLES_101, [1, 0, 1]),
            (REF_SAMPLES_110, [1, 1, 0]),
            (REF_SAMPLES_111, [1, 1, 1]),
        ],
    )
    def test_generate_samples(self, samples, indices):
        """Tests that the generate_samples function of AQTDevice provides samples in
        the correct format expected by PennyLane."""

        dev = AQTDevice(3, api_key=SOME_API_KEY)
        dev.shots = 10
        dev.samples = samples
        res = dev.generate_samples()
        expected_array = np.stack([np.ravel(indices)] * 10)

        assert res.shape == (dev.shots, dev.num_wires)
        assert np.all(res == expected_array)

    @pytest.mark.parametrize("wires", [[0], [1], [2]])
    def test_apply_operation_hadamard(self, wires):
        """Tests that the _apply_operation method correctly populates the circuit
        queue when a PennyLane Hadamard operation is provided."""

        dev = AQTDevice(3, api_key=SOME_API_KEY)
        assert dev.circuit == []

        dev._apply_operation(qml.Hadamard(wires=wires))

        assert dev.circuit == [["X", 1.0, wires], ["Y", -0.5, wires]]

    @pytest.mark.parametrize("wires", [[0, 1], [1, 0], [1, 2], [2, 1], [0, 2], [2, 0]])
    def test_operation_cnot(self, wires):
        """Tests that the _apply_operation method correctly populates the circuit
        queue when a PennyLane CNOT operation is provided."""

        dev = AQTDevice(3, api_key=SOME_API_KEY)
        assert dev.circuit == []

        dev._apply_operation(qml.CNOT(wires=wires))

        # Note: the original parameters used in PennyLane are divided by pi as per AQT convetion
        assert dev.circuit == [
            ["Y", 1 / 2, [wires[0]]],
            ["MS", 1 / 2, wires],
            ["X", -1 / 2, [wires[0]]],
            ["X", -1 / 2, [wires[1]]],
            ["Y", -1 / 2, [wires[0]]],
        ]

    @pytest.mark.parametrize("wires", [[0], [1], [2]])
    def test_apply_operation_S(self, wires):
        """Tests that the _apply_operation method correctly populates the circuit
        queue when a PennyLane S operation is provided."""

        dev = AQTDevice(3, api_key=SOME_API_KEY)
        assert dev.circuit == []

        dev._apply_operation(qml.S(wires=wires))

        assert dev.circuit == [["Z", 0.5, wires]]

    @pytest.mark.parametrize("wires", [[0], [1], [2]])
    @pytest.mark.parametrize(
        "op, aqt_name", [(qml.PauliX, "X"), (qml.PauliY, "Y"), (qml.PauliZ, "Z")]
    )
    def test_apply_operation_pauli(self, wires, op, aqt_name):
        """Tests that the _apply_operation method correctly populates the circuit
        queue when a PennyLane Pauli operation is provided."""

        dev = AQTDevice(3, api_key=SOME_API_KEY)
        assert dev.circuit == []

        dev._apply_operation(op(wires=wires))

        assert dev.circuit == [[aqt_name, 1.0, wires]]

    @pytest.mark.parametrize(
        "op,par,wires,aqt_name",
        [
            (qml.RX, 0.51, [0], "X"),
            (qml.RX, 0.22, [1], "X"),
            (qml.RY, 0.35, [1], "Y"),
            (qml.RY, 0.17, [2], "Y"),
            (qml.RZ, 2.25, [0], "Z"),
            (qml.RZ, 1.77, [0], "Z"),
        ],
    )
    def test_apply_operation_rotations(self, op, par, wires, aqt_name):
        """Tests that the _apply_operation method correctly populates the circuit
        queue when a PennyLane RX, RY, or RZ operation is provided."""

        dev = AQTDevice(3, api_key=SOME_API_KEY)
        assert dev.circuit == []

        dev._apply_operation(op(par, wires=wires))
        aqt_par = par / np.pi

        assert dev.circuit == [[aqt_name, aqt_par, wires]]

    @pytest.mark.parametrize(
        "wires,state",
        [
            ([0], [0]),
            ([0], [1]),
            ([0, 1], [0, 0]),
            ([0, 1], [0, 1]),
            ([0, 1], [1, 0]),
            ([0, 1], [1, 1]),
            ([0, 2], [0, 0]),
            ([0, 2], [0, 1]),
            ([0, 2], [1, 0]),
            ([0, 2], [1, 1]),
            ([0, 1, 2], [0, 0, 0]),
            ([0, 1, 2], [0, 0, 1]),
            ([0, 1, 2], [0, 1, 0]),
            ([0, 1, 2], [1, 0, 0]),
            ([0, 1, 2], [1, 0, 1]),
        ],
    )
    def test_apply_operation_basisstate(self, wires, state):
        """Tests that the _apply_operation method correctly populates the circuit
        queue when a PennyLane BasisState operation is provided."""

        dev = AQTDevice(3, api_key=SOME_API_KEY)
        assert dev.circuit == []

        dev._apply_operation(qml.BasisState(np.array(state), wires=wires))
        expected_circuit = []
        for bit, wire in zip(state, wires):
            if bit == 1:
                expected_circuit.append(["X", 1.0, [wire]])

        assert dev.circuit == expected_circuit

    def test_apply_basisstate_not_first_exception(self):
        """Tests that the apply method raises an exception when BasisState
        is not the first operation."""

        dev = AQTDevice(3, api_key=SOME_API_KEY)

        with pytest.raises(qml.DeviceError, match="only supported at the beginning of a circuit"):
            dev.apply([qml.RX(0.5, wires=1), qml.BasisState(np.array([1, 1, 1]), wires=[0, 1, 2])])

    def test_apply_statevector_not_first_exception(self):
        """Tests that the apply method raises an exception when StatePrep
        is not the first operation."""

        dev = AQTDevice(2, api_key=SOME_API_KEY)

        state = np.ones(8) / np.sqrt(8)
        with pytest.raises(qml.DeviceError, match="only supported at the beginning of a circuit"):
            dev.apply([qml.RX(0.5, wires=1), qml.StatePrep(state, wires=[0, 1, 2])])

    def test_apply_raises_for_error(self, monkeypatch):
        """Tests that the apply method raises an exception when an Error has
        been recorded in the response."""

        dev = AQTDevice(3, api_key=SOME_API_KEY)

        some_error_msg = "Error happened."

        class MockResponse:
            def __init__(self):
                self.status_code = 200

            def json(self):
                return {"ERROR": some_error_msg, "status": "finished", "id": 1}

        monkeypatch.setattr(pennylane_aqt.device, "submit", lambda *args, **kwargs: MockResponse())
        with pytest.raises(ValueError, match="Something went wrong with the request"):
            dev.apply([])

    @pytest.mark.parametrize(
        "op, wires, expected_circuit",
        [
            (qml.PauliX, [0], [["X", -1.0, [0]]]),
            (qml.PauliY, [1], [["Y", -1.0, [1]]]),
            (qml.PauliZ, [1], [["Z", -1.0, [1]]]),
            (qml.Hadamard, [0], [["Y", 0.5, [0]], ["X", 1.0, [0]]]),
            (qml.S, [1], [["Z", -0.5, [1]]]),
        ],
    )
    def test_apply_unparametrized_operation_inverse(self, op, wires, expected_circuit):
        """Tests that inverse operations get recognized and converted to correct parameters for
        unparametrized ops."""

        dev = AQTDevice(2, api_key=SOME_API_KEY)
        dev._apply_operation(qml.adjoint(op(wires=wires)))

        assert dev.circuit == expected_circuit

    @pytest.mark.parametrize(
        "op, pars, wires, expected_circuit",
        [
            (qml.RX, [0.5], [0], [["X", -0.5 / np.pi, [0]]]),
            (qml.RY, [1.3], [1], [["Y", -1.3 / np.pi, [1]]]),
            (qml.RZ, [2.2], [0], [["Z", -2.2 / np.pi, [0]]]),
            (ops.MS, [0.1], [0, 1], [["MS", -0.1, [0, 1]]]),
            (ops.R, [0.3, 0.4], [0], [["R", -0.3, -0.4, [0]]]),
            (qml.BasisState, [np.array([1, 1])], [0, 1], [["X", 1.0, [0]], ["X", 1.0, [1]]]),
            (qml.BasisState, [np.array([0, 1])], [0, 1], [["X", 1.0, [1]]]),
        ],
    )
    def test_apply_parametrized_operation_inverse(self, op, pars, wires, expected_circuit):
        """Tests that inverse operations get recognized and converted to correct parameters for
        parametrized ops."""

        dev = AQTDevice(2, api_key=SOME_API_KEY)
        dev._apply_operation(qml.adjoint(op(*pars, wires=wires)))

        assert dev.circuit == expected_circuit

    @pytest.mark.parametrize("wires", [[0, 1], [0, 2], [1, 2]])
    @pytest.mark.parametrize("par", [0.5, 0.3, -1.1])
    def test_apply_operation_MS(self, wires, par):
        """Tests that the _apply_operation method correctly populates the circuit
        queue when a MS gate operation is provided."""

        dev = AQTDevice(3, api_key=SOME_API_KEY)
        assert dev.circuit == []

        dev._apply_operation(ops.MS(par, wires=wires))

        assert dev.circuit == [["MS", par, wires]]

    @pytest.mark.parametrize("wires", [[0], [1], [2]])
    @pytest.mark.parametrize("par0", [0.5, 0.3, -1.1])
    @pytest.mark.parametrize("par1", [1.1, -0.8, 0.0])
    def test_apply_operation_R(self, wires, par0, par1):
        """Tests that the _apply_operation method correctly populates the circuit
        queue when a R gate operation is provided."""

        dev = AQTDevice(3, api_key=SOME_API_KEY)
        assert dev.circuit == []

        dev._apply_operation(ops.R(par0, par1, wires=wires))

        assert dev.circuit == [["R", par0, par1, wires]]

    def test_unsupported_operation_exception(self):
        """Tests whether an exception is raised if an unsupported operation
        is attempted to be appended to queue."""

        dev = AQTDevice(1, api_key=SOME_API_KEY)

        with pytest.raises(qml.DeviceError, match="is not supported on AQT devices"):
            dev._append_op_to_queue("BAD_GATE", 0.5, [0])


class TestAQTDeviceIntegration:
    """Integration tests of AQTDevice base class with PennyLane"""

    @pytest.mark.parametrize("num_wires", [1, 3])
    @pytest.mark.parametrize("shots", [1, 200])
    def test_load_from_device_function(self, num_wires, shots):
        """Tests that the AQTDevice can be loaded from PennyLane `device` function."""

        dev = qml.device("aqt.sim", wires=num_wires, shots=shots, api_key=SOME_API_KEY)

        assert dev.num_wires == num_wires
        assert dev.shots.total_shots == shots
        assert dev.analytic == False
        assert dev.circuit == []
        assert dev.circuit_json == ""
        assert dev.samples is None
        assert dev.BASE_HOSTNAME == BASE_HOSTNAME
        assert dev.HTTP_METHOD == HTTP_METHOD
        assert API_HEADER_KEY in dev.header.keys()
        assert dev.header[API_HEADER_KEY] == SOME_API_KEY

    def test_api_key_not_found_error(self, monkeypatch, tmpdir):
        """Tests that an error is thrown with the device is created without
        a valid API token."""

        monkeypatch.setenv("AQT_TOKEN", "")
        monkeypatch.setenv("PENNYLANE_CONF", "")
        monkeypatch.setattr("os.curdir", tmpdir.join("folder_without_a_config_file"))

        monkeypatch.setattr(
            "pennylane.default_config", qml.Configuration("config.toml")
        )  # force loading of config
        with pytest.raises(ValueError, match="No valid api key for AQT platform found"):
            dev = qml.device("aqt.sim", 2)

    def test_device_gets_local_config(self, monkeypatch, tmpdir):
        """Tests that the device successfully reads a config from the local directory."""

        monkeypatch.setenv("PENNYLANE_CONF", "")
        monkeypatch.setenv("AQT_TOKEN", "")

        tmpdir.join("config.toml").write(test_config)
        monkeypatch.setattr("os.curdir", tmpdir)
        monkeypatch.setattr(
            "pennylane.default_config", qml.Configuration("config.toml")
        )  # force loading of config

        dev = qml.device("aqt.sim", wires=2)

        assert dev.shots.total_shots == 99
        assert API_HEADER_KEY in dev.header.keys()
        assert dev.header[API_HEADER_KEY] == SOME_API_KEY

    def test_device_gets_api_key_default_config_directory(self, monkeypatch, tmpdir):
        """Tests that the device gets an api key that is stored in the default
        config directory."""
        monkeypatch.setenv("AQT_TOKEN", "")
        monkeypatch.setenv("PENNYLANE_CONF", "")

        config_dir = tmpdir.mkdir("pennylane")  # fake default config directory
        config_dir.join("config.toml").write(test_config)
        monkeypatch.setenv(
            "XDG_CONFIG_HOME", os.path.expanduser(tmpdir)
        )  # HACK: only works on linux

        monkeypatch.setattr("os.curdir", tmpdir.join("folder_without_a_config_file"))

        c = qml.Configuration("config.toml")
        monkeypatch.setattr("pennylane.default_config", c)  # force loading of config

        dev = qml.device("aqt.sim", wires=2)

        assert API_HEADER_KEY in dev.header.keys()
        assert dev.header[API_HEADER_KEY] == SOME_API_KEY

    def test_device_gets_api_key_pennylane_conf_env_var(self, monkeypatch, tmpdir):
        """Tests that the device gets an api key via the PENNYLANE_CONF
        environment variable."""
        monkeypatch.setenv("AQT_TOKEN", "")

        filepath = tmpdir.join("config.toml")
        filepath.write(test_config)
        monkeypatch.setenv("PENNYLANE_CONF", str(tmpdir))

        monkeypatch.setattr("os.curdir", tmpdir.join("folder_without_a_config_file"))
        monkeypatch.setattr(
            "pennylane.default_config", qml.Configuration("config.toml")
        )  # force loading of config

        dev = qml.device("aqt.sim", wires=2)

        assert API_HEADER_KEY in dev.header.keys()
        assert dev.header[API_HEADER_KEY] == SOME_API_KEY

    def test_device_gets_api_key_aqt_token_env_var(self, monkeypatch):
        """Tests that the device gets an api key that is stored in AQT_TOKEN
        environment variable."""

        NEW_API_KEY = SOME_API_KEY + "XYZ987"
        monkeypatch.setenv("PENNYLANE_CONF", "")
        monkeypatch.setenv("AQT_TOKEN", SOME_API_KEY + "XYZ987")

        dev = qml.device("aqt.sim", wires=2)

        assert API_HEADER_KEY in dev.header.keys()
        assert dev.header[API_HEADER_KEY] == NEW_API_KEY

    def test_executes_with_online_api(self, monkeypatch):
        """Tests that a PennyLane QNode successfully executes with a
        mocked out online API."""

        dev = qml.device("aqt.sim", wires=2, shots=10, api_key=SOME_API_KEY)

        @qml.qnode(dev)
        def circuit(x, y):
            qml.RX(x, wires=0)
            qml.RY(y, wires=1)
            ops.R(x, y, wires=0)
            ops.MS(0.5, wires=[0, 1])
            return qml.expval(qml.PauliY(0))

        class MockResponse:
            def __init__(self):
                self.status_code = 200
                self.mock_json1 = {"id": "8c05f8aa-513d-4a04-b3ec-05f3a4c53fb6", "status": "queued"}
                self.mock_json2 = {"samples": MOCK_SAMPLES, "status": "finished"}
                self.num_calls = 0

            def json(self):
                if self.num_calls == 0:
                    self.num_calls = 1
                    return self.mock_json1
                else:
                    return self.mock_json2

        mock_response = MockResponse()
        monkeypatch.setattr(requests, "put", lambda *args, **kwargs: mock_response)

        circuit(0.5, 1.2)
        assert dev.samples == MOCK_SAMPLES

    def test_analytic_error(self):
        """Test that instantiating the device with `shots=None` results in an error"""
        with pytest.raises(ValueError, match="does not support analytic"):
            dev = qml.device("aqt.sim", wires=2, shots=None)


class TestAQTSimulatorDevices:
    """Tests for the AQT simulator device classes."""

    @pytest.mark.parametrize("num_wires", [1, 3])
    @pytest.mark.parametrize("shots", [1, 100])
    def test_simulator_default_init(self, num_wires, shots):
        """Tests that the device is properly initialized."""

        dev = AQTSimulatorDevice(num_wires, shots, SOME_API_KEY)

        assert dev.num_wires == num_wires
        assert dev.shots == shots
        assert dev.analytic == False
        assert dev.circuit == []
        assert dev.circuit_json == ""
        assert dev.samples is None
        assert dev.hostname == BASE_HOSTNAME + "/sim"
        assert dev.HTTP_METHOD == HTTP_METHOD
        assert API_HEADER_KEY in dev.header.keys()
        assert dev.header[API_HEADER_KEY] == SOME_API_KEY

    @pytest.mark.parametrize("num_wires", [1, 3])
    @pytest.mark.parametrize("shots", [1, 100])
    def test_simulator_default_init(self, num_wires, shots):
        """Tests that the device is properly initialized."""

        dev = AQTNoisySimulatorDevice(num_wires, shots, SOME_API_KEY)

        assert dev.num_wires == num_wires
        assert dev.shots == shots
        assert dev.analytic == False
        assert dev.circuit == []
        assert dev.circuit_json == ""
        assert dev.samples is None
        assert dev.hostname == BASE_HOSTNAME + "/sim/noise-model-1"
        assert dev.HTTP_METHOD == HTTP_METHOD
        assert API_HEADER_KEY in dev.header.keys()
        assert dev.header[API_HEADER_KEY] == SOME_API_KEY

    @pytest.mark.skip("API key needs to be inputted")
    def test_simulator_cnot(self):
        """Test that the CNOT operation is decomposed correctly."""
        dev = qml.device("aqt.sim", wires=2, api_key="<Insert API Key here>")

        @qml.qnode(dev)
        def circuit():
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.PauliZ(0))

        assert circuit() == 1

    @pytest.mark.skip("API key needs to be inputted")
    def test_too_many_shots_for_aqt(self):
        """Test >200 shots is invalid with AQT."""
        dev = qml.device("aqt.sim", wires=2, api_key="<Insert API Key here>", shots=201)

        @qml.qnode(dev)
        def circuit():
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.PauliZ(0))

        with pytest.raises(requests.HTTPError, match="Invalid number of repetitions provided!"):
            circuit()
