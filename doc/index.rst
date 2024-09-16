PennyLane-AQT Plugin
####################

:Release: |release|

.. include:: ../README.rst
  :start-after:	header-start-inclusion-marker-do-not-remove
  :end-before: header-end-inclusion-marker-do-not-remove


Once the PennyLane-AQT plugin is installed, the two provided AQT devices can be accessed
directly using PennyLane, without the need to import any additional packages.

Devices
=======

PennyLane-AQT provides two AQT devices for PennyLane:

.. title-card::
    :name: 'aqt.sim'
    :description: Ideal noiseless ion-trap simulator.
    :link: devices.html#ideal-ion-trap-simulator

.. title-card::
    :name: 'aqt.noisy_sim'
    :description: Noisy ion-trap simulator.
    :link: devices.html#noisy-ion-trap-simulator

.. raw:: html

    <div style='clear:both'></div>
    </br>

Both devices support the same operations, including AQT's
custom :class:`rotation <.ops.R>` and :class:`Mølmer-Sørenson-type <.ops.MS>` gates.

Remote backend access
=====================

The user will need access credentials for the AQT platform in order to
use these remote devices. These credentials should be provided to PennyLane via a
`configuration file or environment variable <https://pennylane.readthedocs.io/en/stable/introduction/configuration.html>`_.
Specifically, the variable ``AQT_TOKEN`` must contain a valid access key for AQT's online platform.


.. toctree::
   :maxdepth: 2
   :titlesonly:
   :hidden:

   installation
   support

.. toctree::
   :maxdepth: 2
   :caption: Usage
   :hidden:

   devices

.. toctree::
   :maxdepth: 1
   :caption: API
   :hidden:

   code/__init__
   code/ops
