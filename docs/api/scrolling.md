# Scrolling API

This document explains vertical scrolling support in **screenILI**,
including simple scrolling and scroll regions (fixed header/footer).

---

## Overview

The ILI9488 controller supports **hardware vertical scrolling**.
This allows content to move smoothly without redrawing the entire screen.

`screenILI` exposes this through two methods:

- `scroll(y)`
- `set_scroll(top, bottom)`

Scrolling is **vertical only**.

---

## Simple Scrolling

```python
display.scroll(y)
````

### Parameters

| Name | Type | Description                      |
| ---- | ---- | -------------------------------- |
| `y`  | int  | Vertical scroll offset in pixels |

### Example

```python
# Scroll content down by 40 pixels
display.scroll(40)
```

* Positive values scroll downward
* Wrap-around behavior is handled by the controller

---

## Scroll Regions (Advanced)

You can define **fixed top and bottom regions** that do not scroll,
leaving a scrollable middle area.

```python
display.set_scroll(top, bottom)
```

### Parameters

| Name     | Type | Description                          |
| -------- | ---- | ------------------------------------ |
| `top`    | int  | Height of fixed top area (pixels)    |
| `bottom` | int  | Height of fixed bottom area (pixels) |

Constraint:

```text
top + bottom <= display.height
```

---

## Example: Header + Scrolling Content + Footer

```python
HEADER = 30
FOOTER = 20

display.set_scroll(HEADER, FOOTER)

# Draw static header
display.fill_rect(0, 0, display.width, HEADER, color565(30, 30, 30))
display.text8x8(5, 10, "HEADER", color565(255,255,255))

# Draw static footer
display.fill_rect(
    0,
    display.height - FOOTER,
    display.width,
    FOOTER,
    color565(30, 30, 30),
)

# Scroll only the middle area
offset = 0
while True:
    display.scroll(offset)
    offset += 1
```

---

## Interaction with Rotation

* Scrolling always follows the **current logical orientation**
* `scroll(y)` scrolls along the Y axis as defined by rotation
* No manual adjustment is required

---

## Resetting Scroll Position

To reset scrolling back to the top:

```python
display.scroll(0)
```

To remove scroll regions:

```python
display.set_scroll(0, 0)
```

---

## Performance Notes

* Scrolling is handled entirely in hardware
* No pixel data is moved in RAM
* Extremely fast compared to redraw-based scrolling

---

## Common Pitfalls

### Content appears clipped

* Scroll regions too large
* `top + bottom` exceeds screen height

### Nothing scrolls

* `set_scroll()` defines regions but does not scroll by itself
* You must still call `scroll(y)`

---

## Example

See:

* [`examples/05_scrolling_and_rotation/main.py`](../../examples/05_scrolling_and_rotation/main.py)

---

## Summary

* Use `scroll(y)` for simple vertical movement
* Use `set_scroll(top, bottom)` for fixed UI regions
* Hardware scrolling is fast and efficient
* Works seamlessly with rotation