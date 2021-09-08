AQT Devices
===========

The PennyLane-AQT plugin provides the ability for PennyLane to access
devices available via Alpine Quantum Technologies' online API.

Currently, access is available to two online simulators: an ideal and
a noisy ion-trap simulator.

.. raw::html
    <section id="sim">

Ideal ion-trap simulator
------------------------

This device provides an ideal noiseless ion-trap simulation.
Once the plugin has been installed, you can use this device
directly in PennyLane by specifying ``"aqt.sim"``:

.. code-block:: python

    import pennylane as qml
    from pennylane_aqt import ops

    dev = qml.device("aqt.sim", wires=2)

    @qml.qnode(dev)
    def circuit(w, x, y, z):
        qml.RX(w, wires=0)
        ops.R(x, y, wires=1)
        ops.MS(z, wires=[0,1])
        return qml.expval(qml.PauliZ(0))

.. raw::html
    </section>
    <section id="noisy_sim">

Noisy ion-trap simulator
------------------------

This device provides a more realistic noisy ion-trap simulation.
Once the plugin has been installed, you can use this device
directly in PennyLane by specifying ``"aqt.noisy_sim"``:

.. code-block:: python

    import pennylane as qml
    from pennylane_aqt import ops

    dev = qml.device("aqt.noisy_sim", wires=2)

    @qml.qnode(dev)
    def circuit(w, x, y, z):
        qml.RX(w, wires=0)
        ops.R(x, y, wires=1)
        ops.MS(z, wires=[0,1])
        return qml.expval(qml.PauliZ(0))

Both devices support the same set of operations. They differ only in the
type of simulation they carry out (noiseless vs noisy).

.. raw::html
    </section>

AQT Operations
--------------

PennyLane-AQT provides two gates specific to AQT's ion-trap API:

.. autosummary::

    ~pennylane_aqt.ops.R
    ~pennylane_aqt.ops.MS

These two gates can be imported from :mod:`pennylane_aqt.ops <~.ops>`.

Remote backend access
---------------------

The user will need access credentials for the AQT platform in order to
use these remote devices. These credentials should be provided to PennyLane via a
`configuration file or environment variable <https://pennylane.readthedocs.io/en/stable/introduction/configuration.html>`_.
Specifically, the variable ``AQT_TOKEN`` must contain a valid access key for AQT's online platform.
