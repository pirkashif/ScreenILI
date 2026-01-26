from machine import Pin
from screenILI import Display, color565
from xglcd_font import XglcdFont

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
# Built-in 8×8 font
# =========================
display.text8x8(
    10,
    10,
    "Built-in 8x8",
    color565(255, 255, 255),
)

display.text8x8(
    10,
    30,
    "ROT 90",
    color565(255, 0, 0),
    rotate=90,
)

# =========================
# XglcdFont (ArcadePix9x11)
# =========================
font = XglcdFont(
    "/assets/fonts/ArcadePix9x11.c",
    width=9,
    height=11,
    start_letter=32,
    letter_count=96,
)

display.text(
    x=10,
    y=80,
    text="ArcadePix",
    font=font,
    color=color565(0, 255, 0),
    background=color565(0, 0, 0),
    landscape=False,
    spacing=1,
)

display.text(
    x=10,
    y=100,
    text="Landscape",
    font=font,
    color=color565(255, 255, 0),
    background=color565(0, 0, 0),
    landscape=True,
    spacing=1,
)

# =========================
# Visual bounds
# =========================
display.rect(
    0,
    0,
    display.width,
    display.height,
    color565(64, 64, 64),
)