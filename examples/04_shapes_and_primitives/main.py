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
    rotation="landscape",
    debug_level="warn",
)

display.clear()
display.fill(color565(0, 0, 0))

# =========================
# Pixels & lines
# =========================
display.pixel(10, 10, color565(255, 255, 255))
display.line(20, 20, 200, 20, color565(255, 0, 0))
display.hline(20, 40, 180, color565(0, 255, 0))
display.vline(20, 40, 120, color565(0, 0, 255))

# =========================
# Rectangles
# =========================
display.rect(40, 70, 120, 60, color565(255, 255, 255))
display.fill_rect(45, 75, 110, 50, color565(128, 0, 128))

# =========================
# Circles
# =========================
display.circle(260, 100, 40, color565(255, 255, 0))
display.fill_circle(360, 100, 30, color565(255, 165, 0))

# =========================
# Ellipses (low-level)
# =========================
display.draw_ellipse(260, 200, 50, 25, color565(0, 255, 255))
display.fill_ellipse(360, 200, 40, 20, color565(0, 128, 255))

# =========================
# Polygons
# =========================
display.polygon(
    sides=5,
    x0=100,
    y0=220,
    r=40,
    color=color565(0, 255, 0),
    rotate=0,
)

display.fill_polygon(
    sides=3,
    x0=180,
    y0=220,
    r=35,
    color=color565(255, 0, 255),
    rotate=30,
)

display.polygon(
    sides=6,
    x0=260,
    y0=220,
    r=35,
    color=color565(0, 128, 255),
    rotate=15,
)

# =========================
# Screen bounds
# =========================
display.rect(
    0,
    0,
    display.width,
    display.height,
    color565(64, 64, 64),
)