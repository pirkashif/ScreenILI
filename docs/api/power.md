# Power, Sleep & Lifecycle

This document describes power management, sleep mode, and cleanup behavior
in **screenILI**.

Proper lifecycle handling is important for:
- Power savings
- Display longevity
- Clean shutdowns
- SPI bus safety

---

## Display Power Control

### Turn display on

```python
display.on()
````

Sends the `DISPLAY_ON` command to the controller.

---

### Turn display off

```python
display.off()
```

* Turns off panel output
* Does **not** clear screen memory
* Does **not** put controller to sleep

Useful for:

* Temporary blanking
* Power-saving UI states

---

## Sleep Mode

### Enter sleep mode

```python
display.sleep(True)
```

* Sends `SLPIN`
* Reduces power consumption
* Display contents are preserved internally

---

### Exit sleep mode

```python
display.sleep(False)
```

* Sends `SLPOUT`
* Display resumes operation
* May require a short delay before drawing

---

## Recommended Sleep Pattern

```python
display.off()
display.sleep(True)
```

Wake-up:

```python
display.sleep(False)
display.on()
```

---

## Cleanup

### `cleanup()` Method

```python
display.cleanup(
    clear=True,
    turn_off=True,
    deinit_spi=True,
)
```

### Parameters

| Name         | Type | Description                     |
| ------------ | ---- | ------------------------------- |
| `clear`      | bool | Clear screen before shutdown    |
| `turn_off`   | bool | Turn display off                |
| `deinit_spi` | bool | Deinitialize SPI bus (if owned) |

---

## SPI Ownership

If `Display` created the SPI instance internally:

* `cleanup()` will deinitialize it (default)

If SPI was passed in manually:

* SPI is **not** deinitialized unless explicitly allowed

This prevents breaking other peripherals sharing the SPI bus.

---

## Automatic Cleanup (`__del__`)

The `Display` object performs automatic cleanup when garbage-collected:

* `clear=False`
* `turn_off=True`
* `deinit_spi=True` (only if SPI is owned)

This is a safety net — **do not rely on it for critical shutdown logic**.

---

## Self Test

The built-in self-test exercises:

* Color fill
* Geometry
* Text rendering

```python
display.self_test(delay_ms=600)
```

Sequence:

1. Red → Green → Blue → Black
2. Centered circle
3. `"SELF TEST"` label

Used for:

* Wiring verification
* Basic health checks
* Demos

---

## Power Consumption Notes

* Display backlight power is **hardware-dependent**
* `DISPLAY_OFF` does not always turn off backlight
* Some modules require a separate backlight control pin

If available, control backlight via GPIO or PWM for best results.

---

## Common Pitfalls

### Display does not wake up

* Add a short delay after `sleep(False)`
* Call `display.on()` after waking

### SPI errors after cleanup

* SPI was deinitialized
* Recreate `Display` or SPI object before reuse

---

## Example

See:

* [`examples/06_power_and_selftest/main.py`](../../examples/06_power_and_selftest/main.py)

---

## Summary

* `on()` / `off()` control panel output
* `sleep()` controls controller power state
* `cleanup()` safely shuts everything down
* Self-test validates basic functionality