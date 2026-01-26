from machine import Pin
from screenILI import Display, color565

# =========================
# Pin configuration
# =========================
# Adjust these values to match your board and wiring
SCK_PIN  = Pin(10)
MOSI_PIN = Pin(11)
MISO_PIN = None      # Set to an actual pin if your board uses it
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

# =========================
# Basic operations
# =========================
display.clear()
display.fill(color565(0, 0, 0))  # black

# Simple color fills
display.fill(color565(30, 144, 255))  # dodger blue
display.fill(color565(0, 0, 0))       # back to black

# Built-in 8×8 text
display.text8x8(
    10,
    10,
    "screenILI OK",
    color565(255, 255, 255),
)

# Small visual marker
display.rect(
    5,
    5,
    display.width - 10,
    display.height - 10,
    color565(255, 0, 0),
)