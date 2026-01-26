# Images & Sprites (RGB565)

This document explains how `screenILI` handles images and sprites, the required
file formats, and best practices for performance.

---

## Image Format Overview

All images and sprites must be:

- **Raw binary**
- **RGB565 (16-bit color)**
- **Big-endian byte order**
- **Headerless** (no metadata, no compression)

### RGB565 layout

Each pixel is stored as 2 bytes:

```text
RRRRRGGG GGGBBBBB
````

* Red:   5 bits
* Green: 6 bits
* Blue:  5 bits

Byte order must be **MSB first**.

---

## File Size Rules

File size must exactly match:

```text
width × height × 2 bytes
```

Examples:

| Resolution |     File size |
| ---------: | ------------: |
|    480×320 | 307,200 bytes |
|     120×80 |  19,200 bytes |
|      32×32 |   2,048 bytes |

If the size is wrong, the image will render incorrectly or fail.

---

## Image Locations

Images are stored under:

```text
assets/images/
```

Current project layout:

```text
assets/images/
├─ bg_480x320.raw
├─ logo_120x80.raw
└─ sprite_player_32x32.raw
```

---

## Drawing Images

### Full-screen image

```python
display.image("/assets/images/bg_480x320.raw")
```

* Uses current display width/height by default
* Best used for backgrounds or splash screens

---

### Partial image

```python
display.image(
    "/assets/images/logo_120x80.raw",
    x=50,
    y=50,
    width=120,
    height=80,
)
```

Use this for icons, logos, or UI elements.

---

## Sprites

Sprites are small images loaded into RAM once and drawn many times.

### Loading a sprite

```python
sprite = display.load_sprite(
    "/assets/images/sprite_player_32x32.raw",
    w=32,
    h=32,
)
```

### Drawing a sprite

```python
display.sprite(sprite, x=100, y=150, w=32, h=32)
```

Alias:

```python
display.blit_buffer(sprite, x=100, y=150, w=32, h=32)
```

---

## Animation Strategy

For animation:

1. Load sprite once
2. Redraw sprite at new coordinates
3. Avoid reloading from disk each frame

Example:

```python
x = 0
while True:
    display.sprite(sprite, x=x, y=100, w=32, h=32)
    x += 2
```

---

## Transparency (Color Keying)

Alpha transparency is **not supported**.

To simulate transparency:

* Pick a “key color” (e.g. bright pink)
* Skip drawing pixels of that color manually (advanced use)

For performance reasons, this is not built into the high-level API.

---

## Creating Images

You can create images using:

* GIMP
* Photoshop
* Krita
* ImageMagick
* Python scripts

Workflow:

1. Design image at exact resolution
2. Convert to RGB565
3. Export as raw binary
4. Copy into `assets/images/`

---

## Performance Notes

* Full-screen images are fast but SPI-bound
* Sprites are faster than repeated `image()` calls
* Smaller sprites = higher frame rate
* Avoid frequent full-screen redraws

---

## Common Pitfalls

### Garbled colors

* Wrong RGB565 conversion
* Incorrect byte order

### Image offset or wrap

* Width/height mismatch
* Incorrect file size

### Slow rendering

* SPI clock too low
* Redrawing large areas too often

---

## Example

See:

* [`examples/03_images_and_sprites/main.py`](../examples/03_images_and_sprites/main.py)

---

## Summary

| Use case   | Recommended              |
| ---------- | ------------------------ |
| Background | Full-screen image        |
| Icons      | Partial images           |
| Animation  | Sprites                  |
| UI         | Sprites + minimal redraw |