# Display API Reference

This document describes the high-level `screenILI.Display` class.

It focuses on **what each method does**, expected parameters, and typical usage.
Low-level ILI9488 commands are intentionally abstracted away.

---

## Class: `Display`

```python
from screenILI import Display
````

High-level wrapper around the ILI9488 driver providing:

* Safe defaults
* Friendly rotation handling
* Drawing helpers
* Logging and lifecycle management

---

## Construction

```python
Display(
    *,
    spi=None,
    spi_id=0,
    baudrate=60_000_000,
    sck=None,
    mosi=None,
    miso=None,
    spi_polarity=0,
    spi_phase=0,
    rst,
    dc,
    cs,
    width=None,
    height=None,
    rotation="landscape",
    auto_write=True,
    debug_level="warn",
)
```

### Parameters

| Name                  | Description                                                              |
| --------------------- | ------------------------------------------------------------------------ |
| `spi`                 | Existing SPI object (optional)                                           |
| `spi_id`              | SPI bus ID                                                               |
| `baudrate`            | SPI clock speed                                                          |
| `sck`, `mosi`, `miso` | SPI pins                                                                 |
| `rst`                 | Reset pin (**required**)                                                 |
| `dc`                  | Data/Command pin                                                         |
| `cs`                  | Chip Select pin                                                          |
| `width`, `height`     | Override logical resolution                                              |
| `rotation`            | `"landscape"`, `"portrait"`, `"reverse_landscape"`, `"reverse_portrait"` |
| `auto_write`          | Reserved for future buffering                                            |
| `debug_level`         | `"debug"`, `"info"`, `"warn"`, `"error"`, `"none"`                       |

---

## Core Attributes

| Attribute                  | Description            |
| -------------------------- | ---------------------- |
| `display.width`            | Current logical width  |
| `display.height`           | Current logical height |
| `display.rotation`         | Rotation name          |
| `display.rotation_degrees` | Rotation in degrees    |
| `display.spi`              | SPI instance           |

---

## Drawing Primitives

### Pixel

```python
display.pixel(x, y, color)
```

Draws a single pixel.

---

### Lines

```python
display.line(x1, y1, x2, y2, color)
display.hline(x, y, w, color)
display.vline(x, y, h, color)
```

---

### Rectangles

```python
display.rect(x, y, w, h, color)
display.fill_rect(x, y, w, h, color)
```

---

### Circles

```python
display.circle(x, y, r, color)
display.fill_circle(x, y, r, color)
```

---

### Polygons

```python
display.polygon(sides, x0, y0, r, color, rotate=0)
display.fill_polygon(sides, x0, y0, r, color, rotate=0)
```

* `sides`: number of edges
* `rotate`: rotation in degrees

---

### Ellipses (Low-level passthrough)

```python
display.draw_ellipse(x, y, a, b, color)
display.fill_ellipse(x, y, a, b, color)
```

---

## Text Rendering

### Unified text API

```python
display.text(
    x,
    y,
    text,
    font=None,
    color=0xFFFF,
    background=0x0000,
    landscape=False,
    spacing=1,
)
```

* If `font` is `None`, uses built-in 8×8 font
* If `font` is an `XglcdFont`, uses bitmap font

---

### Built-in 8×8 font

```python
display.text8x8(
    x,
    y,
    text,
    color,
    background=0,
    rotate=0,
)
```

* `rotate`: `0`, `90`, `180`, `270`

---

## Images & Sprites

### Images

```python
display.image(path, x=0, y=0, width=None, height=None)
```

* Expects raw RGB565 file
* If `width` / `height` omitted, uses full screen

---

### Sprites

```python
display.sprite(buf, x, y, w, h)
display.blit_buffer(buf, x, y, w, h)
```

---

### Loading sprites

```python
display.load_sprite(path, w, h)
```

Returns a bytes buffer.

---

## Screen Operations

### Clear / fill

```python
display.clear(color=0x0000)
display.fill(color=0x0000)
```

---

### Rotation

```python
display.set_rotation("portrait")
display.set_rotation(90)
```

Updates:

* Coordinate system
* `width` / `height`

---

### Scrolling

```python
display.scroll(y)
display.set_scroll(top, bottom)
```

---

## Power & Lifecycle

### Display power

```python
display.on()
display.off()
```

---

### Sleep mode

```python
display.sleep(True)   # enter
display.sleep(False)  # exit
```

---

### Cleanup

```python
display.cleanup(
    clear=True,
    turn_off=True,
    deinit_spi=True,
)
```

Automatically called in destructor.

---

## Self Test

```python
display.self_test(delay_ms=600)
```

Used to validate:

* Colors
* Geometry
* Text rendering

---

## Debug Logging

### Set level

```python
display.set_debug_level("debug")
```

Levels:

* `debug`
* `info`
* `warn`
* `error`
* `none`

---

### Get current level

```python
display.get_debug_level()
```

---

## Passthrough to Low-level Driver

Any attribute not found on `Display` is forwarded to `ili9488.Display`.

Example:

```python
display.write_cmd(...)
```

Use with care.

---

## Summary

* Prefer high-level methods (`rect`, `text`, `image`)
* Use low-level access only when necessary
* Keep SPI fast, redraw small areas