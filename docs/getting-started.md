# Getting Started

This guide walks you through setting up **screenILI** on real hardware,
from wiring to running your first example.

---

## Requirements

### Hardware

- ILI9488-based TFT display (480×320)
- Microcontroller board running:
  - **MicroPython** (recommended), or
  - **CircuitPython**
- SPI wiring:
  - `SCK`
  - `MOSI`
  - (optional) `MISO`
  - `CS` (Chip Select)
  - `DC` (Data / Command)
  - `RST` (Reset)

---

## Wiring

Typical SPI wiring (example, adjust to your board):

| Display Pin | MCU Pin |
|------------:|--------:|
| SCK         | GPIO 10 |
| MOSI        | GPIO 11 |
| MISO        | Not used / optional |
| CS          | GPIO 13 |
| DC          | GPIO 14 |
| RST         | GPIO 15 |
| VCC         | 3.3V or 5V (check your display) |
| GND         | GND |

> ⚠ Always verify your display’s voltage requirements.

---

## Copying Files to the Board

At minimum, copy the following files to your board’s filesystem
(root or `/lib`, depending on your setup):

```text
screenILI.py
ili9488.py
xglcd_font.py
assets/
````

Resulting layout on the board:

```text
/
├─ screenILI.py
├─ ili9488.py
├─ xglcd_font.py
└─ assets/
   ├─ fonts/
   │  └─ ArcadePix9x11.c
   └─ images/
      ├─ bg_480x320.raw
      ├─ logo_120x80.raw
      └─ sprite_player_32x32.raw
```

---

## First Test (Minimal Example)

Open and run:

```text
examples/01_minimal/main.py
```

What you should see:

1. Screen clears
2. Screen fills blue, then black
3. White text: `screenILI OK`
4. A red rectangle border around the screen

If this works, your wiring and SPI configuration are correct.

---

## Common Issues

### Blank screen

* Check `CS`, `DC`, and `RST` wiring
* Lower `baudrate` (e.g. `40_000_000`)
* Ensure correct SPI bus (`spi_id`)

### Garbled colors

* Ensure RGB565 is used everywhere
* Verify byte order is big-endian

### Rotation looks wrong

* Check `rotation` argument
* Remember that `width` / `height` change with rotation

---

## Next Steps

Proceed through the examples in order:

1. **Text & fonts**
   -> [`examples/02_text_and_fonts/main.py`](../examples/02_text_and_fonts/main.py)
2. **Images & sprites**
   -> [`examples/03_images_and_sprites/main.py`](../examples/03_images_and_sprites/main.py)
3. **Drawing primitives**
   -> [`examples/04_shapes_and_primitives/main.py`](../examples/04_shapes_and_primitives/main.py)
4. **Scrolling & rotation**
   -> [`examples/05_scrolling_and_rotation/main.py`](../examples/05_scrolling_and_rotation/main.py)
5. **Power & lifecycle**
   -> [`examples/06_power_and_selftest/main.py`](../examples/06_power_and_selftest/main.py)

After that, explore the other documentation sections.