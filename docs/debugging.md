# Debugging & Troubleshooting

This document explains how to debug **screenILI**, interpret log output,
and diagnose common hardware and software issues.

---

## Debug Logging Overview

`screenILI` includes a lightweight built-in logger integrated into the
high-level `Display` class.

Logging is **optional** and disabled by default beyond warnings.

---

## Setting Debug Level

```python
display.set_debug_level("debug")
````

### Available levels

| Level   | Description                                      |
| ------- | ------------------------------------------------ |
| `debug` | Very verbose, logs most operations               |
| `info`  | High-level operations (draw calls, images, text) |
| `warn`  | Warnings only (default)                          |
| `error` | Critical failures                                |
| `none`  | Completely silent                                |

Check current level:

```python
display.get_debug_level()
```

---

## Log Format

Logs are printed to the serial console:

```text
[ILI9488][INFO] rect {'x': 10, 'y': 10, 'w': 100, 'h': 50, 'color': 65535}
```

Format:

```text
[ILI9488][LEVEL] message {optional data}
```

---

## When to Use Each Level

### `debug`

Use when:

* Display does not respond
* Coordinates seem wrong
* Investigating drawing order

> ⚠ Very verbose and slower.

---

### `info`

Use when:

* Verifying drawing logic
* Debugging UI layout

---

### `warn` (default)

Use for:

* Normal development
* Catching out-of-bounds or misuse

---

### `error`

Use when:

* Display fails to initialize
* SPI errors occur

---

## Common Problems & Fixes

### Blank Screen

**Possible causes:**

* Incorrect wiring (`CS`, `DC`, `RST`)
* SPI clock too high
* Wrong SPI bus

**Actions:**

```python
display.set_debug_level("debug")
```

* Verify `init:start` and `init:done` messages
* Lower `baudrate` (e.g. `40_000_000`)

---

### Colors Look Wrong

**Possible causes:**

* Image not RGB565
* Byte order incorrect
* Passing RGB tuples instead of `color565()`

**Check:**

```python
display.fill(color565(255, 0, 0))
```

If red is not red → wiring or panel issue.

---

### Drawing Is Offset or Cut

**Cause:**

* Width/height mismatch
* Wrong rotation assumptions

**Fix:**

* Always use `display.width` / `display.height`
* Avoid hardcoded values

---

### Scrolling Behaves Strangely

**Cause:**

* Scroll region misconfigured

**Fix:**

```python
display.set_scroll(0, 0)
display.scroll(0)
```

Reset state before testing again.

---

### SPI Errors After Cleanup

**Cause:**

* SPI was deinitialized

**Fix:**

* Recreate the `Display` instance
* Or pass an externally managed SPI object

---

## Debugging Images

Checklist:

* File size = `width × height × 2`
* No headers
* RGB565, big-endian

Test with known-good image first.

---

## Minimal Diagnostic Script

```python
display.set_debug_level("debug")

display.fill(color565(255, 0, 0))
display.fill(color565(0, 255, 0))
display.fill(color565(0, 0, 255))
display.text8x8(10, 10, "DEBUG", color565(255,255,255))
```

If this fails, the issue is **not** your application logic.

---

## Hardware-Specific Notes

* Some displays require delays after reset
* Some backlights stay on even when display is off
* Poor wires = flaky SPI

---

## Reporting Issues

When opening an issue, include:

* Board model
* Display model/link
* MicroPython or CircuitPython version
* SPI wiring
* Debug logs (`debug` level)

---

## Summary

* Enable logging early
* Start with simple fills
* Trust hardware scroll and rotation
* Reset state before deep debugging