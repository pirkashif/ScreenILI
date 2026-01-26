# Credits & Attribution

This project builds upon the work of several excellent open-source authors.
Full credit goes to the original creators listed below.

---

## Core Dependencies

### `xglcd_font.py`
- **Author:** @rdagger
- **Source:** https://github.com/rdagger/micropython-ssd1309/blob/master/xglcd_font.py
- **Description:** X-GLCD font loader and renderer for MicroPython.
- **License:** MIT (as per original repository)

Used without functional modification.

---

### `ili9488.py`
- **Author:** @QiaoTuCodes (绒毛宝贝)
- **Source:** https://github.com/QiaoTuCodes/MicroPython-_ILI9488
- **Description:** Low-level MicroPython driver for ILI9488 TFT displays.
- **License:** MIT (as per original repository)

Adapted and wrapped by `screenILI.py` to provide a higher-level, ergonomic API.

---

## Fonts

### ArcadePix 9×11
- **Original Font Author:** Reekee (Dimenzioned)
- **Original Source:** https://www.dafont.com/arcadepix.font
- **Font License:** Free for personal use (see DaFont page)

### X-GLCD Conversion
- **Tool:** MikroElektronika GLCD Font Creator
- **Converted Example Reference:**  
  https://github.com/rdagger/micropython-ssd1309/blob/master/fonts/ArcadePix9x11.c

The font was converted to **X-GLCD C format** for use with `XglcdFont`.

---

## screenILI

- **High-level wrapper, API design, examples, documentation:**  
  © 2026 Nolly

This project would not exist without the work of the authors listed above.
If you use or fork this project, please respect their licenses and give proper credit.