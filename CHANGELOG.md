# Release 0.16.0-dev

### New features

### Improvements

### Bug fixes

### Breaking changes

### Documentation

### Contributors

This release contains contributions from (in alphabetical order):

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
