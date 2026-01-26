# Rotation & Coordinate System

This document explains how rotation works in **screenILI**, how it affects
coordinates, and how to reason about width/height.

---

## Supported Rotations

`screenILI.Display` supports four orientations:

| Name | Degrees | Description |
|----|----:|-------------|
| `landscape` | 0° | Default, USB usually on the left |
| `portrait` | 90° | Rotated clockwise |
| `reverse_landscape` | 180° | Upside-down landscape |
| `reverse_portrait` | 270° | Upside-down portrait |

---

## Setting Rotation

### By name

```python
display.set_rotation("portrait")
````

### By degrees

```python
display.set_rotation(90)
```

Accepted values: `0`, `90`, `180`, `270`.

---

## Automatic Width & Height

When rotation changes:

* `display.width`
* `display.height`

are **automatically updated**.

Example:

```python
display.set_rotation("landscape")
print(display.width, display.height)   # 480, 320

display.set_rotation("portrait")
print(display.width, display.height)   # 320, 480
```

Always rely on `display.width` / `display.height`,
never hardcode dimensions.

---

## Coordinate Origin

Regardless of rotation:

* `(0, 0)` is always the **top-left corner**
* X increases → right
* Y increases ↓ downward

Rotation is handled internally by the driver.

---

## Drawing with Rotation

All high-level drawing methods respect rotation automatically:

```python
display.rect(0, 0, display.width, display.height, WHITE)
display.text8x8(5, 5, "ROTATED", WHITE)
```

No coordinate transformation is required by the user.

---

## Text Rotation vs Screen Rotation

### Screen rotation

```python
display.set_rotation(90)
```

* Affects **everything**
* Coordinates, images, shapes, text

### Text-only rotation (8×8 font)

```python
display.text8x8(50, 50, "TEXT", WHITE, rotate=90)
```

* Rotates only the text glyphs
* Screen orientation remains unchanged

---

## Low-level Rotation Notes

Internally, rotation is implemented via the ILI9488 `MADCTL` register.

You normally do **not** need to interact with this directly.

However, low-level access is possible:

```python
display.write_cmd(display.MADCTL, value)
```

Use only if you fully understand the hardware behavior.

---

## Common Pitfalls

### Hardcoded coordinates

Bad:

```python
display.line(0, 0, 479, 319, WHITE)
```

Good:

```python
display.line(0, 0, display.width - 1, display.height - 1, WHITE)
```

---

### Assuming physical orientation

The physical display orientation does not matter once rotation is set.
Always think in **logical coordinates**.

---

## Example

See:

* [`examples/05_scrolling_and_rotation/main.py`](../../examples/05_scrolling_and_rotation/main.py)

---

## Summary

* Rotation is logical and automatic
* Width & height always match orientation
* `(0,0)` is always top-left
* Use names (`"portrait"`) for clarity