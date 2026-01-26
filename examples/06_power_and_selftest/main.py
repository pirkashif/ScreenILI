from machine import Pin
from time import sleep_ms
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
    debug_level="info",
)

# =========================
# Self-test demo
# =========================
display.self_test(delay_ms=400)

sleep_ms(800)

# =========================
# Power on/off demo
# =========================
display.fill(color565(0, 0, 0))
display.text8x8(10, 10, "Display OFF in 1s", color565(255, 255, 255))
sleep_ms(1000)

display.off()
sleep_ms(1000)

display.on()
display.clear()
display.text8x8(10, 10, "Display ON", color565(0, 255, 0))
sleep_ms(1000)

# =========================
# Sleep / wake demo
# =========================
display.text8x8(10, 30, "Sleep in 1s", color565(255, 255, 0))
sleep_ms(1000)

display.sleep(True)
sleep_ms(1000)

display.sleep(False)
display.clear()
display.text8x8(10, 10, "Wake up!", color565(0, 255, 255))

# =========================
# Cleanup demo
# =========================
sleep_ms(1000)
display.text8x8(10, 30, "Cleanup in 1s", color565(255, 0, 0))
sleep_ms(1000)

display.cleanup(
    clear=True,
    turn_off=True,
    deinit_spi=True,
)