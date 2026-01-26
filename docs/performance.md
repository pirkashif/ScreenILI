# Performance Guide

This document explains how to get the best performance out of **screenILI**
on resource-constrained boards.

The core ideas:

- Push as few pixels as possible
- Use hardware features (scrolling, rotation)
- Use sprites for animation
- Tune SPI speed carefully

---

## 1. SPI Configuration

### Baudrate

`baudrate` directly controls how fast pixels are sent.

```python
display = Display(
    spi_id=0,
    baudrate=60_000_000,  # try 60 MHz, lower if unstable
    ...
)
````

Guidelines:

* Start with **40–60 MHz**
* If you see noise, flicker, or corruption:

  * lower to `40_000_000`
  * check wiring length and quality

### SPI Polarity & Phase

Defaults work for most ILI9488 modules:

```python
spi_polarity=0
spi_phase=0
```

Change **only** if your hardware requires it.

---

## 2. Redraw Strategy

### Minimize Full-Screen Updates

Full-screen redraw cost:

```text
480 × 320 × 2 bytes = 307,200 bytes per frame
```

At high frame rates this will saturate the SPI bus.

Prefer:

* Redrawing only the **changed areas**
* Using `fill_rect()` or small `sprite()` calls

---

### Use Sprites for Animation

Bad (full image every frame):

```python
display.image("/assets/images/bg_480x320.raw")
```

Good (background once, then sprites):

```python
display.image("/assets/images/bg_480x320.raw")  # once

sprite = display.load_sprite("/assets/images/sprite_player_32x32.raw", 32, 32)

x = 0
while True:
    display.sprite(sprite, x=x, y=100, w=32, h=32)
    x += 2
```

---

## 3. Hardware Scrolling vs Redraw

### Prefer `scroll()` over manual redraws

Bad:

```python
# Fake scrolling by redrawing everything in a loop
for offset in range(100):
    display.fill(0)
    # draw whole scene shifted by `offset`
```

Good:

```python
display.set_scroll(top=30, bottom=20)

offset = 0
while True:
    display.scroll(offset)
    offset += 1
```

Hardware scroll:

* Is almost free
* Avoids pushing pixel data over SPI
* Ideal for log views, menus, text feeds

---

## 4. Text Performance

### 8×8 Font vs XglcdFont

* Built-in 8×8 font: **fastest**
* XglcdFont: more RAM and CPU, especially large fonts

Tips:

* Use 8×8 for debug/status/info
* Use XglcdFont only where visual style matters
* Avoid redrawing large paragraphs every frame

---

## 5. Image & Sprite Sizes

### Keep Sprites Small

Sprite cost = `w × h × 2` bytes per draw.

Prefer:

* Multiple small sprites over a huge one
* Logical grouping (character, bullets, icons, etc.)

Example sizes:

| Sprite | Cost per draw |
| ------ | ------------- |
| 16×16  | 512 bytes     |
| 32×32  | 2,048 bytes   |
| 64×64  | 8,192 bytes   |

---

## 6. RAM vs Flash Tradeoffs

### Sprites in RAM

Pros:

* Very fast repeated draw
* Great for animation

Cons:

* Uses precious RAM

### Images from Flash

Pros:

* Saves RAM
* Good for static content (backgrounds)

Cons:

* Slower to draw
* Avoid per-frame full-screen loads

Balanced approach:

* Backgrounds in flash (`image()`)
* Dynamic objects as sprites in RAM (`load_sprite()`)

---

## 7. Debug Level & Performance

High debug levels add overhead.

* `debug`: most verbose, slowest
* `info`: moderate overhead
* `warn`: good default
* `none`: maximum performance

For production:

```python
display.set_debug_level("none")
```

Use `debug` only while diagnosing issues.

---

## 8. Coordinate & Logic Optimization

### Avoid Recomputing Colors

Bad:

```python
for y in range(100):
    display.hline(0, y, display.width, color565(255, 255, 255))
```

Good:

```python
WHITE = color565(255, 255, 255)

for y in range(100):
    display.hline(0, y, display.width, WHITE)
```

---

### Batch Operations Logically

Group updates:

* Draw all text for a region before moving on
* Draw related shapes together
* Minimize state changes and redundant calls

---

## 9. Practical Checklist

For smooth performance:

* [ ] Use **40–60 MHz** SPI if stable
* [ ] Use full-screen draws only when necessary
* [ ] Use **sprites** for moving elements
* [ ] Use **hardware scrolling** for feeds/lists
* [ ] Prefer 8×8 font where possible
* [ ] Precompute colors and constants
* [ ] Set `debug_level` to `"none"` in production

---

## Further Reading

* [`docs/images.md`](./images.md)
* [`docs/fonts.md`](./fonts.md)
* [`docs/api/display.md`](./api/display.md)