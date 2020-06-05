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
This module contains custom AQT operations, designed to be used in PennyLane
QNodes when using the PennyLane-AQT devices.
"""
from pennylane.operation import Operation


class R(Operation):
    r"""R(wires)
    Two-parameter rotation gate.

    .. math:: R(t,p) = \begin{bmatrix}
                           \cos(t\tfrac{\pi}{2}) & -i e^{-ip\pi}\sin(t\tfrac{\pi}{2}) \\
                           -i e^{ip\pi}\sin(t\tfrac{\pi}{2}) & \cos(t\tfrac{\pi}{2})
                       \end{bmatrix}

    For further details, see the `AQT API docs <https://www.aqt.eu/aqt-gate-definitions/>`_.

    **Details:**

    * Number of wires: 1
    * Number of parameters: 1

    Args:
        wires (int): the subsystem the gate acts on
    """
    num_params = 2
    num_wires = 1
    par_domain = "R"
    grad_method = "A"


class MS(Operation):
    r"""MS(wires)
    Mølmer-Sørenson gate.

    .. math:: MS(t) = \begin{bmatrix}
                          \cos(t\tfrac{\pi}{2}) & 0 & 0 & -i\sin(t\tfrac{\pi}{2}) \\
                          0 & \cos(t\tfrac{\pi}{2}) & -i\sin(t\tfrac{\pi}{2}) & 0 \\
                          0 & -i\sin(t\tfrac{\pi}{2}) & \cos(t\tfrac{\pi}{2}) & 0 \\
                          -i\sin(t\tfrac{\pi}{2}) & 0 & 0 & \cos(t\tfrac{\pi}{2})
                      \end{bmatrix}

    For further details, see the `AQT API docs <https://www.aqt.eu/aqt-gate-definitions/>`_.

    **Details:**

    * Number of wires: 2
    * Number of parameters: 1

    Args:
        wires (int): the subsystem the gate acts on
    """
    num_params = 1
    num_wires = 2
    par_domain = "R"
    grad_method = "A"
