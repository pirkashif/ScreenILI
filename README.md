# screenILI · ILI9488 Display Helper for MicroPython & CircuitPython

High-level, ergonomic wrapper around an ILI9488 480×320 TFT driver with:
- Simple `Display` class
- Drawing primitives (lines, rectangles, circles, polygons, etc.)
- Text (built-in 8×8 or XglcdFont)
- Images & sprites
- Rotation, scrolling, sleep/power control
- Optional debug logging

---

[![status](https://img.shields.io/badge/status-alpha-blue.svg)](#)
[![platform](https://img.shields.io/badge/platform-MicroPython%20%7C%20CircuitPython-informational.svg)](#)
[![display](https://img.shields.io/badge/display-ILI9488-ff6f00.svg)](#)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](#)

> Full API reference & advanced docs live in the dedicated documentation (see **Documentation** below).

---

## Contents

- [screenILI · ILI9488 Display Helper for MicroPython \& CircuitPython](#screenili--ili9488-display-helper-for-micropython--circuitpython)
  - [Contents](#contents)
  - [Features](#features)
  - [Hardware \& Requirements](#hardware--requirements)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
    - [Minimal example](#minimal-example)
    - [Drawing primitives](#drawing-primitives)
    - [Text](#text)
      - [Built-in 8×8 font](#built-in-88-font)
      - [XglcdFont (custom fonts)](#xglcdfont-custom-fonts)
    - [Images \& sprites](#images--sprites)
      - [Full-screen / partial image](#full-screen--partial-image)
      - [Sprites \& blitting](#sprites--blitting)
  - [API Overview](#api-overview)
    - [Construction](#construction)
    - [Drawing](#drawing)
    - [Text](#text-1)
    - [Images \& sprites](#images--sprites-1)
    - [Screen operations](#screen-operations)
    - [Power \& lifecycle](#power--lifecycle)
    - [Debug](#debug)
  - [Rotation \& Coordinate System](#rotation--coordinate-system)
  - [Scrolling](#scrolling)
  - [Power, Sleep \& Cleanup](#power-sleep--cleanup)
  - [Debug Logging](#debug-logging)
  - [Self Test](#self-test)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [Credits](#credits)
  - [License](#license)

---

## Features

- High-level `Display` wrapper (`screenILI.Display`)
- Works with ILI9488 480×320 TFT displays (like: [This one on Aliexpress](https://aliexpress.com/item/1005006323424927.html))
- Supports MicroPython and CircuitPython
- Automatic or custom SPI configuration
- Rotations: `landscape`, `portrait`, `reverse_landscape`, `reverse_portrait`
- Drawing primitives:
  - Pixels, lines, polylines
  - Rectangles (outline & filled)
  - Circles & ellipses (outline & filled)
  - Regular polygons (outline & filled)
- Text rendering:
  - Built-in 8×8 MicroPython font (with rotation)
  - XglcdFont bitmap fonts (portrait & landscape)
- Images & sprites:
  - Full-screen or partial raw RGB565 images
  - RAM sprites & buffer blitting
- Scrolling:
  - Vertical scrolling and scroll regions
- Power control:
  - Display on/off, sleep mode
- Optional debug logging with multiple verbosity levels

---

## Hardware & Requirements

- **Display:** ILI9488-based TFT (e.g. 480×320)
- **MCU:** Board running:
  - MicroPython (preferred), or
  - CircuitPython (driver supports both)
- **Interface:** SPI
- **Pins:**
  - `SCK`, `MOSI`, (optional `MISO`)
  - `CS` – Chip Select
  - `DC` – Data/Command
  - `RST` – Reset

---

## Installation

1. Copy the following files to your board:
   - `screenILI.py`
   - `ili9488.py`
   - `xglcd_font.py`
   - (Optional) any X-GLCD `.c` font files and/or image/sprite binary files you use
2. Make sure they are on the Python path (typically the board root or `/lib`).

---

## Quick Start

### Minimal example

```python
from machine import Pin
from screenILI import Display, color565

# Example pins – adjust to your board and wiring
SCK_PIN  = 10
MOSI_PIN = 11
MISO_PIN = None      # or an actual pin if available
CS_PIN   = 13
DC_PIN   = 14
RST_PIN  = 15

display = Display(
    spi_id=0,
    baudrate=60_000_000,
    sck=SCK_PIN,
    mosi=MOSI_PIN,
    miso=MISO_PIN,
    cs=CS_PIN,
    dc=DC_PIN,
    rst=RST_PIN,
    rotation="landscape",   # or "portrait", "reverse_landscape", "reverse_portrait"
    debug_level="warn",     # "debug", "info", "warn", "error", "none"
)

# Clear screen to black
display.clear()

# Fill with a color
display.fill(color565(30, 144, 255))  # Dodger blue
````

---

### Drawing primitives

```python
from screenILI import color565

# Pixel
display.pixel(10, 10, color565(255, 255, 0))

# Lines
display.line(0, 0, display.width - 1, display.height - 1, color565(255, 0, 0))
display.hline(0, 50, 100, color565(0, 255, 0))
display.vline(50, 0, 100, color565(0, 0, 255))

# Rectangle
display.rect(20, 20, 100, 60, color565(255, 255, 255))
display.fill_rect(25, 25, 90, 50, color565(128, 0, 128))  # purple

# Circle
display.circle(display.width // 2, display.height // 2, 40, color565(255, 255, 255))
display.fill_circle(60, 60, 25, color565(255, 165, 0))  # orange

# Polygon (e.g. hexagon)
display.polygon(6, 200, 120, 40, color565(0, 255, 255), rotate=30)
display.fill_polygon(3, 260, 180, 30, color565(255, 0, 255))  # triangle
```

You can also access ellipse helpers directly via the underlying driver:

```python
display.draw_ellipse(100, 200, 40, 20, color565(0, 255, 0))
display.fill_ellipse(200, 220, 30, 15, color565(0, 0, 255))
```

---

### Text

#### Built-in 8×8 font

```python
from screenILI import color565

display.clear()

display.text8x8(10, 10, "Hello", color565(255, 255, 255))
display.text8x8(10, 30, "World!", color565(0, 255, 0), background=color565(0, 0, 0))

# Rotated text (90, 180, 270)
display.text8x8(100, 100, "ROT 90", color565(255, 0, 0), rotate=90)
```

#### XglcdFont (custom fonts)

```python
from screenILI import color565
from xglcd_font import XglcdFont

display.clear()

# X-GLCD C font exported from MikroElektronika GLCD Font Creator
font = XglcdFont(
    "/assets/fonts/ArcadePix9x11.c",
    width=9,
    height=11,
    start_letter=32,
    letter_count=96,
)

display.text(
    x=10,
    y=50,
    text="Custom font!",
    font=font,
    color=color565(255, 255, 0),
    background=color565(0, 0, 0),
    landscape=False,
    spacing=1,
)
```

---

### Images & sprites

#### Full-screen / partial image

`ili9488.Display.draw_image` expects a raw RGB565 binary file of size `width × height × 2` bytes.

```python
from screenILI import color565

display.clear()

# Full-screen (defaults to display size if width/height are omitted)
display.image("/images/bg.raw")

# Partial
display.image("/images/logo.raw", x=50, y=50, width=120, height=80)
```

#### Sprites & blitting

```python
# Load a small sprite (raw RGB565) from disk via low-level helper
sprite_buf = display.load_sprite("/sprites/player.raw", w=32, h=32)

# Draw at (x, y)
display.sprite(sprite_buf, x=100, y=150, w=32, h=32)

# Move / animate by redrawing at new coordinates
display.sprite(sprite_buf, x=120, y=150, w=32, h=32)

# Or use the alias
display.blit_buffer(sprite_buf, x=140, y=150, w=32, h=32)
```

---

## API Overview

This is a high-level view of the most commonly used methods. See full documentation for complete details and low-level commands.

### Construction

| Method / attribute                | Description                                        |
| --------------------------------- | -------------------------------------------------- |
| `Display(...)`                    | Create high-level display instance                 |
| `display.width`, `display.height` | Current logical width/height (depends on rotation) |
| `display.rotation`                | Rotation name (`"landscape"`, etc.)                |
| `display.rotation_degrees`        | Rotation in degrees (`0`, `90`, `180`, `270`)      |

### Drawing

| Method                                  | Description                 |
| --------------------------------------- | --------------------------- |
| `pixel(x, y, color)`                    | Draw a single pixel         |
| `line(x1, y1, x2, y2, color)`           | Line between two points     |
| `hline(x, y, w, color)`                 | Horizontal line             |
| `vline(x, y, h, color)`                 | Vertical line               |
| `rect(x, y, w, h, color)`               | Rectangle outline           |
| `fill_rect(x, y, w, h, color)`          | Filled rectangle            |
| `circle(x, y, r, color)`                | Circle outline              |
| `fill_circle(x, y, r, color)`           | Filled circle               |
| `polygon(sides, x0, y0, r, color)`      | Regular polygon outline     |
| `fill_polygon(sides, x0, y0, r, color)` | Filled regular polygon      |
| `draw_ellipse(...)`                     | Ellipse outline (low-level) |
| `fill_ellipse(...)`                     | Filled ellipse (low-level)  |

### Text

| Method                                                | Description                             |
| ----------------------------------------------------- | --------------------------------------- |
| `text(x, y, text, font=None, color, background, ...)` | High-level text (built-in or XglcdFont) |
| `text8x8(x, y, text, color, background=0, rotate=0)`  | Built-in 8×8 font with rotation         |
| `draw_text(...)`, `draw_letter(...)`                  | Low-level XglcdFont helpers             |

### Images & sprites

| Method                                           | Description                        |
| ------------------------------------------------ | ---------------------------------- |
| `image(path, x=0, y=0, width=None, height=None)` | Draw raw RGB565 image from storage |
| `sprite(buf, x, y, w, h)`                        | Draw sprite from buffer            |
| `blit_buffer(buf, x, y, w, h)`                   | Alias of `sprite(...)`             |
| `load_sprite(path, w, h)`                        | Load raw sprite from file          |

### Screen operations

| Method                    | Description                   |
| ------------------------- | ----------------------------- |
| `fill(color=0x0000)`      | Fill entire screen with color |
| `clear(color=0x0000)`     | Clear screen                  |
| `set_rotation(rotation)`  | Change rotation               |
| `scroll(y)`               | Vertical scroll               |
| `set_scroll(top, bottom)` | Configure scroll region       |

### Power & lifecycle

| Method                                    | Description                        |
| ----------------------------------------- | ---------------------------------- |
| `on()` / `off()`                          | Display on / off                   |
| `sleep(enable=True)`                      | Enter/exit sleep mode              |
| `cleanup(clear=True, turn_off=True, ...)` | Clear screen, turn off, deinit SPI |
| `self_test(delay_ms=600)`                 | Built-in self-test pattern         |

### Debug

| Method                   | Description                                        |
| ------------------------ | -------------------------------------------------- |
| `set_debug_level(level)` | `"debug"`, `"info"`, `"warn"`, `"error"`, `"none"` |
| `get_debug_level()`      | Get current debug level name                       |

---

## Rotation & Coordinate System

The high-level `Display` exposes a friendly rotation API:

```python
display.set_rotation("landscape")          # 0°
display.set_rotation("portrait")           # 90°
display.set_rotation("reverse_landscape")  # 180°
display.set_rotation("reverse_portrait")   # 270°
```

* `display.width` / `display.height` are automatically updated.
* All primitives (`pixel`, `line`, `rect`, `text`, etc.) use the rotated coordinate system.

You can also pass degrees directly:

```python
display.set_rotation(90)
```

---

## Scrolling

The low-level driver supports vertical scrolling and scroll regions:

```python
# Simple vertical scroll
display.scroll(50)  # scroll content by 50 pixels

# Define scrollable area (with fixed top/bottom)
top_margin = 20
bottom_margin = 20
display.set_scroll(top_margin, bottom_margin)
```

This makes it possible to:

* Keep a header area static
* Scroll the central area
* Keep a footer/status bar fixed

---

## Power, Sleep & Cleanup

```python
# Turn display off/on
display.off()
display.on()

# Enter sleep mode
display.sleep(True)

# Exit sleep mode
display.sleep(False)

# Cleanup resources when done
display.cleanup(
    clear=True,       # optional: clear screen
    turn_off=True,    # send DISPLAY_OFF
    deinit_spi=True,  # deinit SPI if owned by this instance
)
```

The high-level `Display` also calls `cleanup()` in its destructor (`__del__`), with `clear=False` by default.

---

## Debug Logging

The wrapper has a simple built-in logger:

```python
display.set_debug_level("debug")  # "debug", "info", "warn", "error", "none"

print(display.get_debug_level())  # e.g. "debug"
```

* `"debug"`: very verbose, logs most drawing operations.
* `"info"`: high-level operations (rectangles, fills, text, image calls, etc.).
* `"warn"`: only warnings.
* `"error"`: critical errors.
* `"none"`: silent.

Logs are printed in a structured format prefixed with `[ILI9488]`.

---

## Self Test

Use the built-in self-test to verify wiring, basic drawing and colors:

```python
display.self_test(delay_ms=600)
```

It will:

1. Fill the screen red, green, blue, then black.
2. Draw a centered circle.
3. Render `"SELF TEST"` using 8×8 text.

---

## Documentation

This README provides a high-level overview and quick examples.

For full API reference and more examples (animations, UI widgets, font preparation, image format details, performance tips, etc.), see the dedicated documentation:

> [screenILI Documentation](/docs/)

---

## Contributing

* Report issues (bug descriptions, board type, display model, wiring, MicroPython/CircuitPython version).
* Open pull requests for:

  * New examples
  * Additional helpers (widgets, convenience APIs)
  * Documentation improvements

Please keep code compatible with both MicroPython and CircuitPython where possible.

---

## Credits

> See [CREDITS.md](./CREDITS.md) for third-party authors and attributions.

---

## License

This project is licensed under the MIT License:

```plaintext
  MIT License

Copyright (c) 2026 Nolly
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
  
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
```