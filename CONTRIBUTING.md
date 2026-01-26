# Contributing to screenILI

Thank you for your interest in contributing to **screenILI**.

This project aims to stay:
- Small
- Clear
- Stable
- Friendly to MicroPython & CircuitPython environments

Please read this document before opening an issue or pull request.

---

## Scope & Philosophy

`screenILI` is a **high-level + ergonomic** display helper.

Goals:
- Predictable API
- Minimal dependencies
- Hardware-friendly performance
- Compatibility across boards

Non-goals (for now):
- Complex UI frameworks
- High-level widgets
- Heavy abstractions
- Non-embedded features

---

## Reporting Bugs

Before opening an issue:

1. Verify the issue on the **latest commit**
2. Run the relevant example from `/examples`
3. Enable debug logging:

```python
display.set_debug_level("debug")
````

When reporting a bug, include:

* Board model
* Display model / link
* Wiring (SPI pins)
* MicroPython or CircuitPython version
* `screenILI` commit or version
* Debug logs (if available)

Please use the **Bug Report** issue template.

---

## Requesting Features

Feature requests are welcome, but must align with project goals.

Good feature requests:

* Improve ergonomics
* Improve performance
* Add missing low-level access
* Improve documentation or examples

Feature requests likely to be declined:

* Complex UI systems
* Platform-specific hacks
* Large abstractions without clear benefit

Use the **Feature Request** template.

---

## Contributing Code

### General Rules

* Keep changes **focused and small**
* Avoid breaking public APIs
* Prefer clarity over cleverness
* MicroPython compatibility comes first

---

### Code Style

* Follow existing formatting
* Use clear variable names
* Avoid unnecessary abstractions
* Comments should explain *why*, not *what*

---

### Compatibility

Code must work with:

* MicroPython
* CircuitPython (when applicable)

Avoid:

* CPython-only features
* Heavy standard library usage
* Dynamic imports unless necessary

---

### Performance Considerations

This is an embedded project.

When adding or modifying code:

* Avoid unnecessary allocations
* Avoid per-pixel Python loops when possible
* Do not introduce hidden redraws
* Be mindful of SPI bandwidth

---

## Documentation Changes

Documentation improvements are always welcome.

If you add or change a feature:

* Update relevant files in `/docs`
* Update examples if user-facing behavior changes

---

## Examples

If adding a new feature:

* Add or update an example under `/examples`
* Keep examples minimal and focused
* One concept per example

---

## Pull Requests

Before submitting a PR:

* [ ] Code builds and runs on hardware
* [ ] No breaking changes (unless discussed)
* [ ] Examples updated (if applicable)
* [ ] Documentation updated (if applicable)

Please use the Pull Request template.

---

## Versioning & Releases

* The project follows **semantic-ish versioning**
* Breaking changes will be documented clearly
* Releases are tagged manually

---

## License

By contributing, you agree that your contributions will be licensed
under the **MIT License**, the same as this project.

---

## Final Notes

This is a hobbyist-friendly but quality-focused project.

Thoughtful contributions are appreciated.
Low-effort or unfocused changes may be declined.

Thank you for helping improve **screenILI**.