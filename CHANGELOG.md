# Release 0.44.0-dev

### New features since last release

### Improvements 🛠

### Breaking changes 💔

### Deprecations 👋

### Documentation 📝

### Bug fixes 🐛

### Contributors ✍️

This release contains contributions from (in alphabetical order):

---
# Release 0.43.0

### Improvements 🛠

* Overload the batch_transform to carry over the validation of no analytic execution.
  [(#95)](https://github.com/PennyLaneAI/pennylane-aqt/pull/95)

### Breaking changes 💔

* Minimum supported version of PennyLane is now v0.43.0.
  [(#99)](https://github.com/PennyLaneAI/pennylane-aqt/pull/99)

* Remove support for Python 3.10 and add support for Python 3.13.
  [(#93)](https://github.com/PennyLaneAI/pennylane-aqt/pull/93)

### Contributors ✍️

This release contains contributions from (in alphabetical order):

Yushao Chen, Andrija Paurevic.

---
# Release 0.42.0
 
 ### New features since last release
 
 ### Improvements 🛠
 
 ### Breaking changes 💔

 * Upgrade minimum supported version of PennyLane to 0.42.0.
  [(#92)](https://github.com/PennyLaneAI/pennylane-aqt/pull/92)
 
 ### Deprecations 👋

 ### Internal changes ⚙️

 * Bumped the `readthedocs.yml` action up to Ubuntu-24.04.
   [(#88)](https://github.com/PennyLaneAI/pennylane-aqt/pull/88)

 * Use new `pennylane.exceptions` module for custom exceptions.
   [(#86)](https://github.com/PennyLaneAI/pennylane-aqt/pull/86)
 
 ### Documentation 📝
 
 ### Bug fixes 🐛
 
 ### Contributors ✍️
 
 This release contains contributions from (in alphabetical order):
 
 Runor Agbaire, Andrija Paurevic
 ---
# Release 0.41.0

### Internal changes ⚙️

* Pinning `setuptools` in the CI to update how the plugin is installed.
  [(#83)](https://github.com/PennyLaneAI/pennylane-cirq/pull/83)

### Contributors ✍️

This release contains contributions from (in alphabetical order):

Pietropaolo Frisoni

---
# Release 0.40.0

### Breaking changes 💔

* The ``qml.QubitStateVector`` template has been removed. Instead, use :class:`~pennylane.StatePrep`.
  [(#77)](https://github.com/PennyLaneAI/pennylane-aqt/pull/77)

### Contributors ✍️

This release contains contributions from (in alphabetical order):

Andrija Paurevic

---
# Release 0.39.0

### Breaking changes 💔

* Dropped support for Python 3.9.
  [(#70)](https://github.com/PennyLaneAI/pennylane-aqt/pull/70)

* Upgraded minimum supported version of PennyLane to 0.38.0.
  [(#75)](https://github.com/PennyLaneAI/pennylane-aqt/pull/75)

### Bug fixes 🐛

* Fix deprecated import path for `QubitDevice`.
  [(#66)](https://github.com/PennyLaneAI/pennylane-aqt/pull/66)

### Contributors ✍️

This release contains contributions from (in alphabetical order):

Astral Cai
Andrija Paurevic

---
# Release 0.32.0

### Breaking changes 💔

* Drops Python 3.8 support.
  [(#51)](https://github.com/PennyLaneAI/pennylane-aqt/pull/51)

### Improvements 🛠

* Added support for `qml.StatePrep` as a state preparation operation.
  [(#50)](https://github.com/PennyLaneAI/pennylane-aqt/pull/50)

### Contributors ✍️

This release contains contributions from (in alphabetical order):

Mudit Pandey,
Jay Soni

---
# Release 0.29.0

### New features since last release

* Adds Python 3.11 support.
  [(#43)](https://github.com/PennyLaneAI/pennylane-aqt/pull/43)

### Breaking changes

* Drops Python 3.7 support.
  [(#43)](https://github.com/PennyLaneAI/pennylane-aqt/pull/43)

### Bug fixes

* For compatibility with PennyLane v0.29, the use of ``Operation.inv()`` has been removed, 
  and replaced with ``qml.adjoint``.
  [(#45)](https://github.com/PennyLaneAI/pennylane-aqt/pull/45)

### Contributors

This release contains contributions from (in alphabetical order):

Lillian M. A. Frederiksen
Christina Lee

---
# Release 0.27.0

### New features since last release

* Adds Python 3.10 support.
  [(#33)](https://github.com/PennyLaneAI/pennylane-aqt/pull/33)

### Contributors

This release contains contributions from (in alphabetical order):

Christina Lee

---

# Release 0.22.0

### Improvements

* Raising an `HTTPError` now provides more information about the exact issues
  by using the underlying response object.
  [(#27)](https://github.com/XanaduAI/pennylane-aqt/pull/27)

### Bug fixes

* Fixed `MS` gate parameter in `CNOT` gate decomposition.
  [(#26)](https://github.com/XanaduAI/pennylane-aqt/pull/26)

### Contributors

This release contains contributions from (in alphabetical order):

Christina Lee, Antal Száva, Tamás Varga

---

# Release 0.18.0

### New features

* Add support for the `CNOT` gate by using a decomposition with the `MS` gate.
  [(#14)](https://github.com/XanaduAI/pennylane-aqt/pull/14)
  [(#19)](https://github.com/XanaduAI/pennylane-aqt/pull/19)
  
### Breaking changes

* Remove support for Python 3.5, 3.6 and add support for Python 3.8, 3.9.
  [(#15)](https://github.com/XanaduAI/pennylane-aqt/pull/15)
  
### Contributors

This release contains contributions from (in alphabetical order):

Romain Moyard, Antal Száva

---

# Release 0.15.0

### Bug fixes

* For compatibility with PennyLane v0.15, the `analytic` keyword argument
  has been removed from usage within the AQT device.
  [(#12)](https://github.com/XanaduAI/pennylane-aqt/pull/12)

### Contributors

This release contains contributions from (in alphabetical order):

Josh Izaac

---

# Release 0.11.0

### New features since last release

* The AQT plugin now supports arbitrary wire labels when instantiating the device [(#8)](https://github.com/XanaduAI/pennylane-aqt/pull/8) [(#9)](https://github.com/XanaduAI/pennylane-aqt/pull/9)

### Contributors

This release contains contributions from (in alphabetical order):

Maria Schuld

---

# Release 0.9.1

### New features since last release

* Both of the native gates `R` and `MS` now support the parameter-shift differentiation
  method in PennyLane. [(#4)](https://github.com/XanaduAI/pennylane-aqt/pull/4)

### Improvements

* Lowered the retry timer so the plugin won't hammer the server for results.
  [(#4)](https://github.com/XanaduAI/pennylane-aqt/pull/4)

### Contributors

This release contains contributions from (in alphabetical order):

Nathan Killoran

---

# Release 0.9.0

Initial release.

This release contains contributions from (in alphabetical order):

Nathan Killoran, Josh Izaac
