# ============================================================
# LED CONTROLLER - Control RGB LEDs and indicators
# ============================================================

import logging
import subprocess
from typing import Tuple
import config

logger = logging.getLogger(__name__)


class LEDController:
    """
    Control RGB LEDs and status indicators
    Support for GPIO, PWM, and WS2812B addressable LEDs
    """

    def __init__(self):
        """Initialize LED controller"""
        self.led_type = config.LED_TYPE
        self.gpio_pins = config.GPIO_PINS
        self.num_leds = config.NUM_LEDS
        self.brightness = config.LED_BRIGHTNESS
        self.current_color = (0, 0, 0)
        
        self._init_gpio()
        logger.info(f"LED controller initialized ({self.led_type})")

    def _init_gpio(self):
        """Initialize GPIO"""
        try:
            if self.led_type == "gpio":
                import RPi.GPIO as GPIO
                GPIO.setmode(GPIO.BCM)
                for pin in self.gpio_pins.values():
                    GPIO.setup(pin, GPIO.OUT)
                logger.info("GPIO initialized")
            elif self.led_type == "ws2812b":
                try:
                    from neopixel import Neopixel
                    self.neopixel = Neopixel(self.num_leds, 0, 18, "GRB")
                    logger.info("WS2812B initialized")
                except ImportError:
                    logger.warning("neopixel library not found")
        except Exception as e:
            logger.warning(f"GPIO initialization warning: {e}")

    def set_color(self, r: int, g: int, b: int):
        """Set LED color"""
        try:
            r = max(0, min(255, int(r * self.brightness / 100)))
            g = max(0, min(255, int(g * self.brightness / 100)))
            b = max(0, min(255, int(b * self.brightness / 100)))
            
            self.current_color = (r, g, b)
            
            if self.led_type == "gpio":
                self._set_color_gpio(r, g, b)
            elif self.led_type == "ws2812b":
                self._set_color_neopixel(r, g, b)
            
            logger.debug(f"Color set: RGB({r}, {g}, {b})")
            
        except Exception as e:
            logger.error(f"Set color error: {e}")

    def _set_color_gpio(self, r: int, g: int, b: int):
        """Set color on GPIO-controlled LED"""
        try:
            import RPi.GPIO as GPIO
            
            # Simple on/off control
            red_pin = self.gpio_pins.get('red')
            green_pin = self.gpio_pins.get('green')
            blue_pin = self.gpio_pins.get('blue')
            
            if red_pin and red_pin > 0:
                GPIO.output(red_pin, GPIO.HIGH if r > 127 else GPIO.LOW)
            if green_pin and green_pin > 0:
                GPIO.output(green_pin, GPIO.HIGH if g > 127 else GPIO.LOW)
            if blue_pin and blue_pin > 0:
                GPIO.output(blue_pin, GPIO.HIGH if b > 127 else GPIO.LOW)
        except Exception as e:
            logger.error(f"GPIO color error: {e}")

    def _set_color_neopixel(self, r: int, g: int, b: int):
        """Set color on WS2812B addressable LED"""
        try:
            for i in range(self.num_leds):
                self.neopixel.set_pixel(i, (r, g, b))
            self.neopixel.show()
        except Exception as e:
            logger.error(f"Neopixel color error: {e}")

    def set_status_color(self, status: str):
        """Set LED color based on status"""
        colors = {
            'ok': (0, 255, 0),           # Green
            'warning': (255, 255, 0),    # Yellow
            'error': (255, 0, 0),        # Red
            'critical': (255, 0, 255),   # Magenta
            'info': (0, 0, 255),         # Blue
            'off': (0, 0, 0)             # Off
        }
        
        color = colors.get(status, (0, 0, 0))
        self.set_color(*color)
        logger.info(f"Status color set: {status}")

    def pulse(self, r: int, g: int, b: int, times: int = 3, duration: int = 500):
        """Pulse LED"""
        try:
            import time
            
            for _ in range(times):
                self.set_color(r, g, b)
                time.sleep(duration / 1000)
                self.set_color(0, 0, 0)
                time.sleep(duration / 1000)
            
            logger.info(f"Pulsed LED {times} times")
            
        except Exception as e:
            logger.error(f"Pulse error: {e}")

    def blink(self, r: int, g: int, b: int, times: int = 5, speed: int = 250):
        """Blink LED"""
        try:
            import time
            
            for _ in range(times):
                self.set_color(r, g, b)
                time.sleep(speed / 1000)
                self.set_color(0, 0, 0)
                time.sleep(speed / 1000)
            
            logger.info(f"LED blinked {times} times")
            
        except Exception as e:
            logger.error(f"Blink error: {e}")

    def rainbow(self, duration: int = 5000):
        """Rainbow animation"""
        try:
            import time
            
            start_time = time.time()
            while time.time() - start_time < duration / 1000:
                hue = ((time.time() - start_time) % (duration / 1000)) / (duration / 1000)
                r, g, b = self._hsv_to_rgb(hue, 1, 1)
                self.set_color(int(r), int(g), int(b))
                time.sleep(0.05)
            
            logger.info("Rainbow animation complete")
            
        except Exception as e:
            logger.error(f"Rainbow error: {e}")

    def _hsv_to_rgb(self, h: float, s: float, v: float) -> Tuple[int, int, int]:
        """Convert HSV to RGB"""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return int(r * 255), int(g * 255), int(b * 255)

    def set_brightness(self, brightness: int):
        """Set LED brightness (0-100)"""
        self.brightness = max(0, min(100, brightness))
        # Reapply current color with new brightness
        self.set_color(*self.current_color)
        logger.info(f"Brightness set to: {self.brightness}%")

    def turn_off(self):
        """Turn off LED"""
        self.set_color(0, 0, 0)
        logger.info("LED turned off")

    def turn_on(self, r: int = 255, g: int = 255, b: int = 255):
        """Turn on LED"""
        self.set_color(r, g, b)
        logger.info("LED turned on")

    def alert(self, severity: str = 'warning'):
        """Flash alert pattern"""
        if severity == 'critical':
            self.pulse(255, 0, 0, times=5, duration=300)
        elif severity == 'warning':
            self.pulse(255, 255, 0, times=3, duration=400)
        elif severity == 'info':
            self.blink(0, 0, 255, times=2, speed=200)
        else:
            self.pulse(0, 255, 0, times=2, duration=500)

    def get_status(self) -> dict:
        """Get LED status"""
        return {
            'led_type': self.led_type,
            'current_color': self.current_color,
            'brightness': self.brightness,
            'num_leds': self.num_leds
        }

    def cleanup(self):
        """Clean up GPIO"""
        try:
            if self.led_type == "gpio":
                import RPi.GPIO as GPIO
                GPIO.cleanup()
                logger.info("GPIO cleaned up")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
