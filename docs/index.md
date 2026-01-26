# screenILI Documentation

Welcome to the official documentation for **screenILI**.

This documentation complements the README by providing deeper explanations,
advanced usage, and implementation details.

---

## Getting Started

If you are new:

1. Read the **README.md** for a high-level overview.
2. Run [`examples/01_minimal/main.py`](../examples/01_minimal/main.py) to verify your wiring.
3. Progress through the examples in order:
   - [`02_text_and_fonts`](../examples/02_text_and_fonts/main.py)
   - [`03_images_and_sprites`](../examples/03_images_and_sprites/main.py)
   - [`04_shapes_and_primitives`](../examples/04_shapes_and_primitives/main.py)
   - [`05_scrolling_and_rotation`](../examples/05_scrolling_and_rotation/main.py)
   - [`06_power_and_selftest`](../examples/06_power_and_selftest/main.py)
---

## Topics (WIP)

The following sections will be expanded over time:

- Display initialization & SPI tuning
- Coordinate system & rotation internals
- Drawing primitives (performance notes)
- Text rendering:
  - Built-in 8×8 font
  - XglcdFont (X-GLCD C fonts)
- Image & sprite formats (RGB565)
- Scrolling regions & UI layouts
- Power management & lifecycle
- Debug logging
- Common pitfalls & troubleshooting

---

## Fonts

Custom fonts are handled via **XglcdFont** and X-GLCD C font files
(exported from [MikroElektronika GLCD Font Creator](https://www.mikroe.com/glcd-font-creator)).

See:
- [`assets/fonts/`](../assets/fonts/)
- [`examples/02_text_and_fonts/main.py`](../examples/02_text_and_fonts/main.py)

---

## Images

Images and sprites must be **raw RGB565**, big-endian, headerless.

See:
- [`assets/images/`](../assets/images/)
- [`examples/03_images_and_sprites/main.py`](../examples/03_images_and_sprites/main.py)

---

## Status

This documentation is a **work in progress**.
Please check back later for more detailed sections and explanations.
For now, **examples are the best source of information**.