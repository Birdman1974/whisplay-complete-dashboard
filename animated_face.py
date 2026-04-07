# ============================================================
# ANIMATED FACE - Interactive face with expressions
# ============================================================

import logging
import math
from datetime import datetime
import config

try:
    from PIL import Image, ImageDraw
except ImportError:
    import os
    os.system("pip3 install Pillow")
    from PIL import Image, ImageDraw

logger = logging.getLogger(__name__)


class AnimatedFace:
    """
    Render an animated face with different expressions
    Support for sentiment-driven emotions
    """

    def __init__(self, width: int = 200, height: int = 200):
        """Initialize animated face"""
        self.width = width
        self.height = height
        self.expression = "neutral"
        self.blink_state = False
        self.blink_counter = 0
        self.frame_count = 0
        
        # Expression colors
        self.colors = {
            'happy': config.FACE_COLOR_HAPPY,
            'sad': config.FACE_COLOR_SAD,
            'angry': config.FACE_COLOR_ANGRY,
            'neutral': config.FACE_COLOR_NEUTRAL,
            'concerned': config.FACE_COLOR_CONCERNED
        }
        
        logger.info(f"Animated face initialized ({width}x{height})")

    def set_expression(self, expression: str):
        """Set face expression"""
        if expression in self.colors:
            self.expression = expression
            logger.info(f"Expression changed to: {expression}")
        else:
            logger.warning(f"Unknown expression: {expression}")

    def update(self):
        """Update face state (blink, animations)"""
        self.frame_count += 1
        
        # Handle blinking
        blink_interval = int(config.FRAMERATE / config.FACE_BLINK_RATE)
        if self.frame_count % blink_interval == 0:
            self.blink_state = not self.blink_state

    def draw(self, canvas, expression: str = None):
        """Draw face on canvas"""
        if expression:
            self.set_expression(expression)
        
        self.update()
        
        # Create face image
        face_img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(face_img)
        
        color = self.colors.get(self.expression, self.colors['neutral'])
        
        # Draw face circle
        margin = 10
        draw.ellipse(
            [margin, margin, self.width - margin, self.height - margin],
            fill=color,
            outline=(200, 200, 200),
            width=2
        )
        
        # Draw eyes
        self._draw_eyes(draw, color)
        
        # Draw mouth based on expression
        self._draw_mouth(draw, color)
        
        return face_img

    def _draw_eyes(self, draw, face_color):
        """Draw eyes"""
        eye_y = self.height // 3
        left_eye_x = self.width // 3
        right_eye_x = 2 * self.width // 3
        eye_size = 15
        
        if not self.blink_state:
            # Open eyes
            draw.ellipse(
                [left_eye_x - eye_size, eye_y - eye_size, 
                 left_eye_x + eye_size, eye_y + eye_size],
                fill=(0, 0, 0)
            )
            draw.ellipse(
                [right_eye_x - eye_size, eye_y - eye_size,
                 right_eye_x + eye_size, eye_y + eye_size],
                fill=(0, 0, 0)
            )
            
            # Draw pupils
            pupil_size = 5
            draw.ellipse(
                [left_eye_x - pupil_size, eye_y - pupil_size,
                 left_eye_x + pupil_size, eye_y + pupil_size],
                fill=(255, 255, 255)
            )
            draw.ellipse(
                [right_eye_x - pupil_size, eye_y - pupil_size,
                 right_eye_x + pupil_size, eye_y + pupil_size],
                fill=(255, 255, 255)
            )
        else:
            # Closed eyes (lines)
            draw.line(
                [left_eye_x - eye_size, eye_y, left_eye_x + eye_size, eye_y],
                fill=(0, 0, 0),
                width=2
            )
            draw.line(
                [right_eye_x - eye_size, eye_y, right_eye_x + eye_size, eye_y],
                fill=(0, 0, 0),
                width=2
            )

    def _draw_mouth(self, draw, face_color):
        """Draw mouth based on expression"""
        mouth_y = 2 * self.height // 3
        mouth_width = 60
        mouth_height = 20
        mouth_x = self.width // 2
        
        if self.expression == "happy":
            # Smile
            draw.arc(
                [mouth_x - mouth_width, mouth_y - mouth_height,
                 mouth_x + mouth_width, mouth_y + mouth_height],
                0, 180,
                fill=(0, 0, 0),
                width=3
            )
        elif self.expression == "sad":
            # Frown
            draw.arc(
                [mouth_x - mouth_width, mouth_y + mouth_height,
                 mouth_x + mouth_width, mouth_y - mouth_height],
                180, 360,
                fill=(0, 0, 0),
                width=3
            )
        elif self.expression == "angry":
            # Angry mouth (straight line)
            draw.line(
                [mouth_x - mouth_width, mouth_y, mouth_x + mouth_width, mouth_y],
                fill=(0, 0, 0),
                width=3
            )
        else:
            # Neutral (straight line)
            draw.line(
                [mouth_x - mouth_width, mouth_y, mouth_x + mouth_width, mouth_y],
                fill=(0, 0, 0),
                width=2
            )

    def get_expression(self) -> str:
        """Get current expression"""
        return self.expression

    def animate_sequence(self, expressions: list, delay: int = 10):
        """Animate through a sequence of expressions"""
        for expr in expressions:
            self.set_expression(expr)
            for _ in range(delay):
                self.update()

    def react_to_sentiment(self, sentiment_score: float):
        """React to sentiment analysis"""
        if sentiment_score > config.SENTIMENT_THRESHOLD_POSITIVE:
            self.set_expression("happy")
        elif sentiment_score < config.SENTIMENT_THRESHOLD_NEGATIVE:
            self.set_expression("sad")
        else:
            self.set_expression("neutral")

    def react_to_alert(self, alert_type: str):
        """React to security alerts"""
        if alert_type in ['critical', 'high']:
            self.set_expression("concerned")
        elif alert_type == 'medium':
            self.set_expression("neutral")

    def show_thinking(self):
        """Show thinking animation"""
        self.set_expression("concerned")
        for _ in range(20):
            self.update()
