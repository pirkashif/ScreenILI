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

# =========================
# Full-screen background
# =========================
display.image("/assets/images/bg_480x320.raw")

# =========================
# Partial image (logo)
# =========================
display.image(
    "/assets/images/logo_120x80.raw",
    x=20,
    y=20,
    width=120,
    height=80,
)

# =========================
# Sprite loading
# =========================
sprite = display.load_sprite(
    "/assets/images/sprite_player_32x32.raw",
    w=32,
    h=32,
)

# =========================
# Sprite drawing / movement
# =========================
x = 50
y = 150

display.sprite(sprite, x=x, y=y, w=32, h=32)

# Simple animation step
x += 40
display.sprite(sprite, x=x, y=y, w=32, h=32)

x += 40
display.blit_buffer(sprite, x=x, y=y, w=32, h=32)

# =========================
# Visual reference frame
# =========================
display.rect(
    0,
    0,
    display.width,
    display.height,
    color565(255, 255, 255),
)