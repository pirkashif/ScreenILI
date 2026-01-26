from machine import Pin, SPI
from time import sleep_ms
from ili9488 import Display as _LowLevelDisplay, color565 as _color565

def color565(r, g, b):
    return _color565(r, g, b)

rgb = color565

_ROTATION_NAME_TO_DEGREES = {
    "portrait": 90,
    "landscape": 0,
    "reverse_portrait": 270,
    "reverse_landscape": 180,
}

_DEBUG_LEVELS = {
    "debug": 10,
    "info": 20,
    "warn": 30,
    "error": 40,
    "none": 100,
}

class Display:
    def __init__(
        self,
        *,
        spi=None,
        spi_id=0,
        baudrate=60_000_000,
        sck=None,
        mosi=None,
        miso=None,
        spi_polarity=0,
        spi_phase=0,
        rst=None,
        dc=None,
        cs=None,
        width=None,
        height=None,
        rotation="landscape",
        auto_write=True,
        debug_level="warn",
        **spi_kwargs,
    ):
        self._debug_level_name = None
        self._debug_level = _DEBUG_LEVELS["warn"]
        self.set_debug_level(debug_level)
        rotation_deg = self._normalize_rotation(rotation)
        self._rotation_deg = rotation_deg
        self._rotation_name = self._deg_to_rotation_name(rotation_deg)
        if width is None or height is None:
            if rotation_deg in (0, 180):
                default_width, default_height = 480, 320
            else:
                default_width, default_height = 320, 480
            if width is None:
                width = default_width
            if height is None:
                height = default_height
        self._log("info", "init:start", {"spi_id": spi_id, "baudrate": baudrate, "width": width, "height": height, "rotation": rotation})
        self._own_spi = False
        self._auto_write = bool(auto_write)
        if spi is None:
            if sck is None or mosi is None:
                self._log("error", "spi:create:missing_pins", {"sck": sck, "mosi": mosi})
                raise ValueError('When "spi" is not provided, you must provide "sck" and "mosi" pins.')
            sck_pin = sck if isinstance(sck, Pin) else Pin(sck)
            mosi_pin = mosi if isinstance(mosi, Pin) else Pin(mosi)
            if isinstance(miso, Pin) or miso is None:
                miso_pin = miso
            else:
                miso_pin = Pin(miso)
            self._log("debug", "spi:create", {"spi_id": spi_id, "polarity": spi_polarity, "phase": spi_phase})
            spi = SPI(
                spi_id,
                baudrate=baudrate,
                polarity=spi_polarity,
                phase=spi_phase,
                sck=sck_pin,
                mosi=mosi_pin,
                miso=miso_pin,
                **spi_kwargs,
            )
            self._own_spi = True
        if rst is None:
            self._log("error", "init:missing_rst")
            raise ValueError('"rst" pin is required.')
        dc_pin = dc if isinstance(dc, Pin) else Pin(dc)
        cs_pin = cs if isinstance(cs, Pin) else Pin(cs)
        rst_pin = rst if isinstance(rst, Pin) else Pin(rst)
        self._log("debug", "ili9488:create", {"width": width, "height": height, "rotation_deg": rotation_deg})
        self._lcd = _LowLevelDisplay(
            spi=spi,
            cs=cs_pin,
            dc=dc_pin,
            rst=rst_pin,
            width=width,
            height=height,
            rotation=rotation_deg,
        )
        self.spi = spi
        if self._rotation_deg in (0, 180):
            self._native_width = width
            self._native_height = height
        else:
            self._native_width = height
            self._native_height = width
        if self._rotation_deg in (0, 180):
            self.width = self._native_width
            self.height = self._native_height
        else:
            self.width = self._native_height
            self.height = self._native_width
        self._lcd.width = self.width
        self._lcd.height = self.height
        self._log("info", "init:done", {"width": self.width, "height": self.height, "rotation_deg": self._rotation_deg, "rotation_name": self._rotation_name})

    def _normalize_rotation(self, rotation):
        if isinstance(rotation, str):
            try:
                return _ROTATION_NAME_TO_DEGREES[rotation]
            except KeyError:
                valid = ", ".join(_ROTATION_NAME_TO_DEGREES.keys())
                raise ValueError('Invalid rotation "%s". Must be one of: %s' % (rotation, valid))
        deg = int(rotation)
        if deg not in (0, 90, 180, 270):
            raise ValueError("Rotation degrees must be 0, 90, 180 or 270.")
        return deg

    def _deg_to_rotation_name(self, deg):
        for name, d in _ROTATION_NAME_TO_DEGREES.items():
            if d == deg:
                return name
        return "unknown"

    def _log(self, level, msg, extra=None):
        if level not in _DEBUG_LEVELS:
            return
        lvl_val = _DEBUG_LEVELS[level]
        if lvl_val < self._debug_level:
            return
        if extra is not None:
            print("[ILI9488][%s] %s %s" % (level.upper(), msg, extra))
        else:
            print("[ILI9488][%s] %s" % (level.upper(), msg))

    def set_debug_level(self, level):
        if level not in _DEBUG_LEVELS:
            raise ValueError('Invalid debug_level "%s". Use one of: %s' % (level, ", ".join(_DEBUG_LEVELS.keys())))
        self._debug_level_name = level
        self._debug_level = _DEBUG_LEVELS[level]

    def get_debug_level(self):
        return self._debug_level_name

    def __getattr__(self, name):
        try:
            return getattr(self._lcd, name)
        except AttributeError:
            raise AttributeError("%r object has no attribute %r" % (type(self).__name__, name))

    @property
    def rotation(self):
        return self._rotation_name

    @property
    def rotation_degrees(self):
        return self._rotation_deg

    @property
    def auto_write(self):
        return self._auto_write

    def set_rotation(self, rotation):
        deg = self._normalize_rotation(rotation)
        if deg not in self._lcd.ROTATE:
            self._log("error", "rotation:unsupported", {"deg": deg})
            raise ValueError("Rotation not supported by underlying driver.")
        self._rotation_deg = deg
        self._rotation_name = self._deg_to_rotation_name(deg)
        self._lcd.rotation = self._lcd.ROTATE[deg]
        self._lcd.write_cmd(self._lcd.MADCTL, self._lcd.rotation)
        if deg in (0, 180):
            self.width = self._native_width
            self.height = self._native_height
        else:
            self.width = self._native_height
            self.height = self._native_width
        self._lcd.width = self.width
        self._lcd.height = self.height
        self._log("info", "rotation:set", {"deg": deg, "name": self._rotation_name, "width": self.width, "height": self.height})

    def pixel(self, x, y, color):
        self._log("debug", "pixel", {"x": x, "y": y, "color": color})
        self._lcd.draw_pixel(x, y, color)

    def line(self, x1, y1, x2, y2, color):
        self._log("debug", "line", {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "color": color})
        self._lcd.draw_line(x1, y1, x2, y2, color)

    def hline(self, x, y, w, color):
        self._log("debug", "hline", {"x": x, "y": y, "w": w, "color": color})
        self._lcd.draw_hline(x, y, w, color)

    def vline(self, x, y, h, color):
        self._log("debug", "vline", {"x": x, "y": y, "h": h, "color": color})
        self._lcd.draw_vline(x, y, h, color)

    def rect(self, x, y, w, h, color):
        self._log("info", "rect", {"x": x, "y": y, "w": w, "h": h, "color": color})
        self._lcd.draw_rectangle(x, y, w, h, color)

    def fill_rect(self, x, y, w, h, color):
        self._log("info", "fill_rect", {"x": x, "y": y, "w": w, "h": h, "color": color})
        self._lcd.fill_rectangle(x, y, w, h, color)

    def circle(self, x, y, r, color):
        self._log("info", "circle", {"x": x, "y": y, "r": r, "color": color})
        self._lcd.draw_circle(x, y, r, color)

    def fill_circle(self, x, y, r, color):
        self._log("info", "fill_circle", {"x": x, "y": y, "r": r, "color": color})
        self._lcd.fill_circle(x, y, r, color)

    def polygon(self, sides, x0, y0, r, color, rotate=0):
        self._log("info", "polygon", {"sides": sides, "x0": x0, "y0": y0, "r": r, "color": color, "rotate": rotate})
        self._lcd.draw_polygon(sides, x0, y0, r, color, rotate)

    def fill_polygon(self, sides, x0, y0, r, color, rotate=0):
        self._log("info", "fill_polygon", {"sides": sides, "x0": x0, "y0": y0, "r": r, "color": color, "rotate": rotate})
        self._lcd.fill_polygon(sides, x0, y0, r, color, rotate)

    def text(self, x, y, text, font=None, color=0xFFFF, background=0x0000, landscape=False, spacing=1):
        self._log("info", "text", {"x": x, "y": y, "text": text, "font": "xglcd" if font else "builtin", "color": color, "background": background, "landscape": landscape})
        if font is None:
            self._lcd.draw_text8x8(x, y, text, color, background, rotate=0)
        else:
            self._lcd.draw_text(x, y, text, font=font, color=color, background=background, landscape=landscape, spacing=spacing)

    def text8x8(self, x, y, text, color=0xFFFF, background=0x0000, rotate=0):
        self._log("info", "text8x8", {"x": x, "y": y, "text": text, "color": color, "background": background, "rotate": rotate})
        self._lcd.draw_text8x8(x, y, text, color, background, rotate)

    def image(self, path, x=0, y=0, width=None, height=None):
        w = self.width if width is None else width
        h = self.height if height is None else height
        self._log("info", "image", {"path": path, "x": x, "y": y, "w": w, "h": h})
        self._lcd.draw_image(path, x, y, w, h)

    def sprite(self, buf, x, y, w, h):
        self._log("info", "sprite", {"x": x, "y": y, "w": w, "h": h})
        self._lcd.draw_sprite(buf, x, y, w, h)

    def blit_buffer(self, buf, x, y, w, h):
        self._log("info", "blit_buffer", {"x": x, "y": y, "w": w, "h": h})
        self.sprite(buf, x, y, w, h)

    def fill(self, color=0x0000):
        self._log("info", "fill", {"color": color})
        self._lcd.clear(color)

    def clear(self, color=0x0000):
        self._log("info", "clear", {"color": color})
        self._lcd.clear(color)

    def off(self):
        self._log("info", "display_off", None)
        self._lcd.display_off()

    def on(self):
        self._log("info", "display_on", None)
        self._lcd.display_on()

    def sleep(self, enable=True):
        self._log("info", "sleep", {"enable": enable})
        self._lcd.sleep(enable)

    def cleanup(self, *, clear=True, turn_off=True, deinit_spi=True):
        self._log("info", "cleanup:start", {"clear": clear, "turn_off": turn_off, "deinit_spi": deinit_spi, "own_spi": self._own_spi})
        if clear:
            try:
                self._lcd.clear()
            except Exception as e:
                self._log("warn", "cleanup:clear_failed", {"error": str(e)})
        if turn_off:
            try:
                self._lcd.display_off()
            except Exception as e:
                self._log("warn", "cleanup:display_off_failed", {"error": str(e)})
        if deinit_spi and self._own_spi:
            try:
                if hasattr(self.spi, "deinit"):
                    self.spi.deinit()
                    self._log("info", "cleanup:spi_deinit", None)
            except Exception as e:
                self._log("warn", "cleanup:spi_deinit_failed", {"error": str(e)})
        self._log("info", "cleanup:done", None)

    def self_test(self, delay_ms=600):
        self._log("info", "self_test:start", {"width": self.width, "height": self.height, "delay_ms": delay_ms})
        try:
            self.fill(color565(255, 0, 0))
            sleep_ms(delay_ms)
            self.fill(color565(0, 255, 0))
            sleep_ms(delay_ms)
            self.fill(color565(0, 0, 255))
            sleep_ms(delay_ms)
            self.fill(color565(0, 0, 0))
            sleep_ms(delay_ms)
            c = color565(255, 255, 255)
            self.circle(self.width // 2, self.height // 2, min(self.width, self.height) // 4, c)
            self.text8x8(5, 5, "SELF TEST", c, 0x0000, rotate=0)
            self._log("info", "self_test:end", None)
        except Exception as e:
            self._log("error", "self_test:exception", {"error": str(e)})

    def __del__(self):
        try:
            self.cleanup(clear=False, turn_off=True, deinit_spi=True)
        except Exception:
            pass