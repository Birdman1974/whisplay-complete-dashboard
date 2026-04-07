# ============================================================
# DISPLAY MANAGER - Handle all display operations
# ============================================================

import logging
from typing import Tuple, Optional
import config

try:
    import pygame
except ImportError:
    import os
    os.system("pip3 install pygame")
    import pygame

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import os
    os.system("pip3 install Pillow")
    from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class DisplayManager:
    """
    Manage display operations for different platforms
    Support for pygame (testing) and actual hardware display
    """

    def __init__(self, width: int = 320, height: int = 240, mock_mode: bool = False):
        """Initialize display manager"""
        self.width = width
        self.height = height
        self.mock_mode = mock_mode
        self.display_type = config.DISPLAY_TYPE
        
        # Create canvas
        self.canvas = Image.new('RGB', (width, height), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.canvas)
        
        # Initialize display
        if not mock_mode and self.display_type == "actual_hardware":
            self._init_hardware_display()
        else:
            self._init_pygame_display()
        
        logger.info(f"Display manager initialized ({width}x{height}) - Mock: {mock_mode}")

    def _init_pygame_display(self):
        """Initialize pygame display"""
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Whisplay AI Dashboard")
            self.clock = pygame.time.Clock()
            logger.info("Pygame display initialized")
        except Exception as e:
            logger.error(f"Pygame initialization error: {e}")

    def _init_hardware_display(self):
        """Initialize actual hardware display"""
        try:
            # Try to import and initialize hardware display driver
            # This could be for SPI/I2C display, ST7789, etc.
            logger.info("Hardware display initialization (placeholder)")
            # Implementation depends on actual display hardware
        except Exception as e:
            logger.error(f"Hardware display initialization error: {e}")

    def clear(self, color: Tuple[int, int, int] = (0, 0, 0)):
        """Clear display"""
        self.canvas.paste(color, (0, 0, self.width, self.height))
        self.draw = ImageDraw.Draw(self.canvas)

    def draw_text(self, text: str, position: Tuple[int, int], 
                  size: str = "medium", color: Tuple[int, int, int] = (255, 255, 255)):
        """Draw text on display"""
        try:
            font_size = self._get_font_size(size)
            
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            self.draw.text(position, text, fill=color, font=font)
            
        except Exception as e:
            logger.error(f"Text drawing error: {e}")

    def draw_rectangle(self, xy: Tuple, fill: Tuple[int, int, int] = None,
                       outline: Tuple[int, int, int] = (255, 255, 255), width: int = 1):
        """Draw rectangle"""
        try:
            self.draw.rectangle(xy, fill=fill, outline=outline, width=width)
        except Exception as e:
            logger.error(f"Rectangle drawing error: {e}")

    def draw_circle(self, center: Tuple[int, int], radius: int,
                   fill: Tuple[int, int, int] = None,
                   outline: Tuple[int, int, int] = (255, 255, 255)):
        """Draw circle"""
        try:
            x, y = center
            self.draw.ellipse(
                [x - radius, y - radius, x + radius, y + radius],
                fill=fill,
                outline=outline
            )
        except Exception as e:
            logger.error(f"Circle drawing error: {e}")

    def draw_line(self, xy: Tuple, fill: Tuple[int, int, int] = (255, 255, 255), width: int = 1):
        """Draw line"""
        try:
            self.draw.line(xy, fill=fill, width=width)
        except Exception as e:
            logger.error(f"Line drawing error: {e}")

    def draw_image(self, image: Image.Image, position: Tuple[int, int]):
        """Draw image on canvas"""
        try:
            self.canvas.paste(image, position)
        except Exception as e:
            logger.error(f"Image drawing error: {e}")

    def render(self):
        """Render canvas to display"""
        try:
            if self.display_type == "pygame" or self.mock_mode:
                surf = pygame.image.fromstring(self.canvas.tobytes(), self.canvas.size, "RGB")
                self.screen.blit(surf, (0, 0))
                pygame.display.flip()
            else:
                # Hardware display update
                self._update_hardware_display()
        except Exception as e:
            logger.error(f"Render error: {e}")

    def _update_hardware_display(self):
        """Update hardware display"""
        try:
            # Implementation depends on hardware
            # This is a placeholder
            pass
        except Exception as e:
            logger.error(f"Hardware update error: {e}")

    def _get_font_size(self, size: str) -> int:
        """Get font size by name"""
        sizes = {
            'small': 12,
            'medium': 18,
            'large': 24,
            'extra_large': 32
        }
        return sizes.get(size, 18)

    def draw_progress_bar(self, xy: Tuple, progress: float, 
                         color: Tuple[int, int, int] = (0, 255, 0)):
        """Draw progress bar"""
        try:
            x1, y1, x2, y2 = xy
            width = x2 - x1
            filled_width = int(width * min(progress, 1.0))
            
            # Draw background
            self.draw.rectangle(xy, fill=(50, 50, 50), outline=(255, 255, 255))
            
            # Draw progress
            self.draw.rectangle(
                [x1, y1, x1 + filled_width, y2],
                fill=color
            )
        except Exception as e:
            logger.error(f"Progress bar error: {e}")

    def draw_chart(self, data: list, position: Tuple[int, int], 
                   width: int = 100, height: int = 50):
        """Draw simple chart"""
        try:
            if not data:
                return
            
            x, y = position
            max_val = max(data) if data else 1
            
            bar_width = width // len(data)
            
            for i, val in enumerate(data):
                bar_height = int((val / max_val) * height)
                x_pos = x + (i * bar_width)
                y_pos = y + height - bar_height
                
                self.draw.rectangle(
                    [x_pos, y_pos, x_pos + bar_width - 1, y + height],
                    fill=(0, 255, 0)
                )
        except Exception as e:
            logger.error(f"Chart drawing error: {e}")

    def cleanup(self):
        """Clean up display resources"""
        try:
            if self.display_type == "pygame":
                pygame.quit()
            logger.info("Display cleaned up")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

    def get_text_size(self, text: str, size: str = "medium") -> Tuple[int, int]:
        """Get size of rendered text"""
        try:
            font_size = self._get_font_size(size)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            bbox = self.draw.textbbox((0, 0), text, font=font)
            return (bbox[2] - bbox[0], bbox[3] - bbox[1])
        except Exception as e:
            logger.error(f"Text size error: {e}")
            return (0, 0)
