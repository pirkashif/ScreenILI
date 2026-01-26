from machine import Pin
from screenILI import Display, color565

# =========================
# Pin configuration
# =========================
SCK_PIN  = Pin(10)
MOSI_PIN = Pin(11)
MISO_PIN = None
CS_PIN   = Pin(13)
DC_PIN   = Pin(14)
RST_PIN  = Pin(15)

# =========================
# Display initialization
# =========================
display = Display(
    spi_id=0,
    baudrate=60_000_000,
    sck=SCK_PIN,
    mosi=MOSI_PIN,
    miso=MISO_PIN,
    cs=CS_PIN,
    dc=DC_PIN,
    rst=RST_PIN,
    rotation="portrait",
    debug_level="warn",
)

display.clear()
display.fill(color565(0, 0, 0))

# =========================
# Rotation demo
# =========================
display.text8x8(10, 10, "PORTRAIT", color565(255, 255, 255))

display.set_rotation("landscape")
display.clear()
display.text8x8(10, 10, "LANDSCAPE", color565(0, 255, 0))

display.set_rotation("reverse_landscape")
display.clear()
display.text8x8(10, 10, "REV LAND", color565(255, 255, 0))

display.set_rotation("reverse_portrait")
display.clear()
display.text8x8(10, 10, "REV PORT", color565(255, 0, 0))

# Restore baseline rotation
display.set_rotation("landscape")
display.clear()

# =========================
# Scrolling demo
# =========================
# Fixed header
display.fill_rect(0, 0, display.width, 30, color565(40, 40, 40))
display.text8x8(5, 10, "HEADER", color565(255, 255, 255))

# Fixed footer
display.fill_rect(
    0,
    display.height - 30,
    display.width,
    30,
    color565(40, 40, 40),
)
display.text8x8(
    5,
    display.height - 20,
    "FOOTER",
    color565(255, 255, 255),
)

# Scrollable region
top_margin = 30
bottom_margin = 30
display.set_scroll(top_margin, bottom_margin)

# Draw content taller than the scroll region
y = top_margin
for i in range(20):
    display.text8x8(
        10,
        y,
        "Line {}".format(i),
        color565(200, 200, 200),
    )
    y += 12

# Perform scrolling
for offset in range(0, 120, 4):
    display.scroll(offset)