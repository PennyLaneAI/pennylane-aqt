# Release 0.28.0-dev

### New features since last release

### Breaking changes

### Improvements

### Documentation

### Bug fixes

### Contributors

This release contains contributions from (in alphabetical order):

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
