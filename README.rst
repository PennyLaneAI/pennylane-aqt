PennyLane-AQT Plugin
####################

.. image:: https://img.shields.io/github/actions/workflow/status/PennyLaneAI/pennylane-aqt/tests.yml?branch=master&logo=github&style=flat-square
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/PennyLaneAI/pennylane-aqt/actions?query=workflow%3ATests

.. image:: https://img.shields.io/codecov/c/github/PennyLaneAI/pennylane-aqt/master.svg?logo=codecov&style=flat-square
    :alt: Codecov coverage
    :target: https://codecov.io/gh/PennyLaneAI/pennylane-aqt

.. image:: https://img.shields.io/codefactor/grade/github/PennyLaneAI/pennylane-aqt/master?logo=codefactor&style=flat-square
    :alt: CodeFactor Grade
    :target: https://www.codefactor.io/repository/github/pennylaneai/pennylane-aqt

.. image:: https://readthedocs.com/projects/xanaduai-pennylane-aqt/badge/?version=latest&style=flat-square
    :alt: Read the Docs
    :target: https://docs.pennylane.ai/projects/aqt

.. image:: https://img.shields.io/pypi/v/PennyLane-aqt.svg?style=flat-square
    :alt: PyPI
    :target: https://pypi.org/project/PennyLane-aqt

.. image:: https://img.shields.io/pypi/pyversions/PennyLane-aqt.svg?style=flat-square
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/PennyLane-aqt

.. header-start-inclusion-marker-do-not-remove

The PennyLane-AQT plugin provides the ability to use Alpine Quantum Technologies' ion-trap
quantum computing backends with PennyLane.

`PennyLane <https://pennylane.ai>`_ provides open-source tools for
quantum machine learning, quantum computing, quantum chemistry, and hybrid quantum-classical computing.

`Alpine Quantum Technologies <https://www.aqt.eu>`_ is an ion-trap quantum computing
company offering access to quantum computing devices over the cloud.

.. header-end-inclusion-marker-do-not-remove

The plugin documentation can be found here: `PennyLane-AQT <https://docs.pennylane.ai/projects/aqt>`__.

Features
========

* Provides two devices which can be used with AQT's online API: ``"aqt.sim"`` and ``"aqt.noisy_sim"``.
  These provide access to an ideal ion-trap simulator and a noisy ion-trap simulator, respectively.

* The plugin provides additional support for the AQT's custom rotation and Mølmer-Sørenson-type gates.

* Supports core PennyLane operations such as qubit rotations, Hadamard, basis state preparations, etc.

.. installation-start-inclusion-marker-do-not-remove

Installation
============

PennyLane-AQT requires Python >= 3.10. If you currently do not have Python 3 installed,
we recommend `Anaconda for Python 3 <https://www.anaconda.com/download/>`_, a distributed
version of Python packaged for scientific computation. If you are using Python 3.12, 
ensure `setuptools` is up to date prior to installation:
::

    $ python3 -m pip install --upgrade setuptools

PennyLane-AQT only requires PennyLane for use, no additional external frameworks are needed.
The plugin can be installed via ``pip``:
::

    $ python3 -m pip install pennylane-aqt

Alternatively, you can install PennyLane-AQT from the source code by navigating to the top directory and running
::

    $ python3 setup.py install

Software tests
~~~~~~~~~~~~~~

To ensure that PennyLane-AQT is working correctly after installation, the test suite should be
run. Begin by installing the required packages via ``pip``
::

    $ pip install -r requirements-ci.txt

Then navigate to the source code folder and run
::

    $ make test


Documentation
~~~~~~~~~~~~~

To build the HTML documentation, go to the top-level directory and run
::

    $ make docs

The documentation can then be found in the ``doc/_build/html/`` directory.

.. installation-end-inclusion-marker-do-not-remove

Getting started
===============

Once PennyLane is installed, the provided AQT devices can be accessed straight
away in PennyLane. However, the user will need access credentials for the AQT platform in order to
use these remote devices. These credentials should be provided to PennyLane via a
`configuration file or environment variable <https://pennylane.readthedocs.io/en/stable/introduction/configuration.html>`_.
Specifically, the variable ``AQT_TOKEN`` must contain a valid access key for AQT's online platform.

You can instantiate the AQT devices for PennyLane as follows:

.. code-block:: python

    import pennylane as qml
    dev1 = qml.device('aqt.sim', wires=2)
    dev2 = qml.device('aqt.noisy_sim', wires=2)

These devices can then be used just like other devices for the definition and evaluation of
quantum circuits within PennyLane. For more details and ideas, see the
`PennyLane website <https://pennylane.ai>`_ and refer
to the `PennyLane documentation <https://pennylane.readthedocs.io>`_.


Contributing
============

We welcome contributions—simply fork the PennyLane-AQT repository, and then make a
`pull request <https://help.github.com/articles/about-pull-requests/>`_ containing your contribution.
All contributers to PennyLane-AQT will be listed as contributors on the releases.

We also encourage bug reports, suggestions for new features and enhancements, and even links to cool
projects or applications built on PennyLane and AQT.

The PennyLane-AQT repository provide a top-level file (``.pre-commit-config.yaml``) 
for configuring `pre-commit <https://pre-commit.com/>`_ to run ``black``, ``isort`` and ``pylint`` as a ``git``
pre-commit hook. Once configured, issuing ``git commit`` will run the tools
automatically. If any of the checks fail, committing fails too. A failed
``black`` check will reformat the required files. Running the pre-commit hook
mechanisms can be disabled for a commit by passing the ``-n/--no-verify``
option.

The ``pre-commit`` package can be installed e.g., via ``pip``:

.. code-block:: bash

    pip install pre-commit

Then, it can be installed for a specific repository by running

.. code-block:: bash

    pre-commit install

in the folder where the ``.pre-commit-config.yaml`` file exists (the top-level
folder for PennyLane-AQT).


Contributors
============

PennyLane-AQT is the work of many `contributors <https://github.com/PennyLaneAI/pennylane-aqt/graphs/contributors>`_.

If you are doing research using PennyLane, please cite our papers:

    Ville Bergholm, Josh Izaac, Maria Schuld, Christian Gogolin, M. Sohaib Alam, Shahnawaz Ahmed,
    Juan Miguel Arrazola, Carsten Blank, Alain Delgado, Soran Jahangiri, Keri McKiernan, Johannes Jakob Meyer,
    Zeyue Niu, Antal Száva, Nathan Killoran.
    *PennyLane: Automatic differentiation of hybrid quantum-classical computations.* 2018.
    `arXiv:1811.04968 <https://arxiv.org/abs/1811.04968>`_

    Maria Schuld, Ville Bergholm, Christian Gogolin, Josh Izaac, and Nathan Killoran.
    *Evaluating analytic gradients on quantum hardware.* 2018.
    `Phys. Rev. A 99, 032331 <https://journals.aps.org/pra/abstract/10.1103/PhysRevA.99.032331>`_

.. support-start-inclusion-marker-do-not-remove

Support
=======

- **Source Code:** https://github.com/PennyLaneAI/pennylane-aqt
- **Issue Tracker:** https://github.com/PennyLaneAI/pennylane-aqt/issues

If you are having issues, please let us know by posting the issue on our GitHub issue tracker.

.. support-end-inclusion-marker-do-not-remove
.. license-start-inclusion-marker-do-not-remove

License
=======

PennyLane-AQT is **free** and **open source**, released under the Apache License, Version 2.0.

.. license-end-inclusion-marker-do-not-remove
