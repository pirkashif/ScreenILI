# Color Handling (RGB565)

This document explains how colors are represented and used in **screenILI**.

The library uses **RGB565**, a 16-bit color format commonly used on embedded TFT displays.

---

## RGB565 Overview

RGB565 packs color into **16 bits**:

```text
RRRRR GGGGGG BBBBB
 5      6      5   bits
````

* Red:   0–31
* Green: 0–63
* Blue:  0–31

This format balances color depth and memory/bandwidth efficiency.

---

## `color565()` Helper

```python
from screenILI import color565
```

### Usage

```python
color = color565(r, g, b)
```

Where:

* `r`, `g`, `b` are **0–255**
* Return value is a **16-bit integer** suitable for all drawing calls

Example:

```python
white = color565(255, 255, 255)
black = color565(0, 0, 0)
red   = color565(255, 0, 0)
green = color565(0, 255, 0)
blue  = color565(0, 0, 255)
```

---

## Aliases

`screenILI` also exposes:

```python
rgb = color565
```

So you may write:

```python
display.fill(rgb(30, 144, 255))  # DodgerBlue
```

---

## Common Colors

| Name    | RGB           | Code                    |
| ------- | ------------- | ----------------------- |
| Black   | (0, 0, 0)     | `color565(0,0,0)`       |
| White   | (255,255,255) | `color565(255,255,255)` |
| Red     | (255,0,0)     | `color565(255,0,0)`     |
| Green   | (0,255,0)     | `color565(0,255,0)`     |
| Blue    | (0,0,255)     | `color565(0,0,255)`     |
| Yellow  | (255,255,0)   | `color565(255,255,0)`   |
| Cyan    | (0,255,255)   | `color565(0,255,255)`   |
| Magenta | (255,0,255)   | `color565(255,0,255)`   |

---

## Background Colors

Most drawing functions accept an optional `background` color:

```python
display.text8x8(
    10,
    10,
    "Hello",
    color=color565(255,255,255),
    background=color565(0,0,0),
)
```

* `background=0` means transparent/unchanged background
* Any non-zero value fills the background pixels

---

## Color in Images & Sprites

* Images must already be encoded in RGB565
* No conversion is done at runtime
* Byte order must be **big-endian**

See:

* [`docs/images.md`](../images.md)

---

## Performance Notes

* Color values are passed directly to SPI
* Avoid recalculating colors inside tight loops
* Precompute commonly used colors

Example:

```python
WHITE = color565(255,255,255)
BLACK = color565(0,0,0)

for y in range(100):
    display.hline(0, y, display.width, WHITE)
```

---

## Common Pitfalls

### Colors look wrong

* Ensure values are 0–255
* Do not pass 24-bit RGB tuples directly
* Always convert using `color565()`

### Colors inverted

* Usually caused by incorrect display wiring
* Not a color conversion issue

---

## Summary

* All colors are RGB565
* Use `color565(r, g, b)`
* Images must already be RGB565
* Background color `0` means transparent