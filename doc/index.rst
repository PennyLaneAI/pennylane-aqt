PennyLane-AQT Plugin
####################

:Release: |release|

.. include:: ../README.rst
  :start-after:	header-start-inclusion-marker-do-not-remove
  :end-before: header-end-inclusion-marker-do-not-remove


Once the PennyLane-SF plugin is installed, the two provided Strawberry Fields devices can be accessed
straight away in PennyLane, without the need to import any additional packages.

Devices
=======

PennyLane-AQT provides two AQT devices for PennyLane:

.. devicegalleryitem::
    :name: 'aqt.sim'
    :description: Ideal noiseless ion-trap simulator.

.. devicegalleryitem::
    :name: 'aqt.noisy_sim'
    :description: Noisy ion-trap simulator.

.. raw:: html

    <div style='clear:both'></div>
    </br>

Both devices support the same operations, including AQT's
custom rotation and Mølmer-Sørenson-type gates

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

   devices/aqt_devices
   devices/ops

.. toctree::
   :maxdepth: 1
   :caption: API
   :hidden:

   code
