# ============================================================
# WHISPLAY AI DASHBOARD - MAIN APPLICATION
# ============================================================
# Master control application for all features
# ============================================================

import os
import sys
import time
import logging
import threading
from datetime import datetime
from typing import Dict, List, Optional

# Third-party imports
try:
    import pygame
    pygame.init()
except ImportError:
    print("Installing pygame...")
    os.system("pip3 install pygame")
    import pygame
    pygame.init()

try:
    import requests
except ImportError:
    os.system("pip3 install requests")
    import requests

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    os.system("pip3 install Pillow")
    from PIL import Image, ImageDraw, ImageFont

# Local imports
import config
from weather_service import WeatherService
from news_service import NewsService
from calendar_service import CalendarService
from animated_face import AnimatedFace
from display_manager import DisplayManager
from security_monitor import SecurityMonitor
from wifi_monitor import WiFiMonitor
from sentiment_analyzer import SentimentAnalyzer
from text_to_speech import TextToSpeech
from ai_engine import AIEngine

# ============================================================
# LOGGING SETUP
# ============================================================

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ============================================================
# WHISPLAY DASHBOARD CLASS
# ============================================================

class WhisplayDashboard:
    """
    Main dashboard application combining all features:
    - Weather with alerts
    - News aggregation and sentiment analysis
    - Calendar and reminders
    - Security monitoring (Fail2ban, Snort)
    - WiFi monitoring
    - Animated face with AI
    - Live charts and metrics
    - Text-to-speech
    - LED animations
    """

    def __init__(self):
        """Initialize all services and components"""
        logger.info("Initializing Whisplay AI Dashboard...")
        
        self.running = True
        self.current_view = "dashboard"  # dashboard, calendar, security, network, ai
        self.update_threads = []
        
        # Initialize display
        self.display = DisplayManager(
            width=config.DISPLAY_WIDTH,
            height=config.DISPLAY_HEIGHT,
            mock_mode=config.MOCK_MODE
        )
        
        # Initialize core services
        self.weather = WeatherService() if config.ENABLE_AI else None
        self.news = NewsService() if config.ENABLE_NEWS else None
        self.calendar = CalendarService() if config.ENABLE_CALENDAR else None
        self.face = AnimatedFace() if config.ENABLE_ANIMATED_FACE else None
        self.security = SecurityMonitor() if config.ENABLE_FAIL2BAN else None
        self.wifi = WiFiMonitor() if config.ENABLE_WIFI_MONITORING else None
        self.sentiment = SentimentAnalyzer() if config.ENABLE_SENTIMENT_ANALYSIS else None
        self.tts = TextToSpeech() if config.ENABLE_TEXT_TO_SPEECH else None
        self.ai = AIEngine() if config.ENABLE_AI else None
        
        # Data storage
        self.current_weather = {}
        self.current_news = []
        self.current_events = []
        self.security_alerts = []
        self.network_stats = {}
        
        logger.info("Dashboard initialized successfully")

    def start(self):
        """Start all services and begin main loop"""
        logger.info("Starting Whisplay AI Dashboard...")
        
        # Start background update threads
        self._start_update_threads()
        
        # Main display loop
        try:
            while self.running:
                self._update_display()
                time.sleep(1.0 / config.FRAMERATE)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            self.stop()
        except Exception as e:
            logger.error(f"Fatal error in main loop: {e}", exc_info=True)
            self.stop()

    def _start_update_threads(self):
        """Start background threads for data updates"""
        logger.info("Starting update threads...")
        
        # Weather updates
        if self.weather:
            thread = threading.Thread(target=self._weather_update_loop, daemon=True)
            thread.start()
            self.update_threads.append(thread)
        
        # News updates
        if self.news:
            thread = threading.Thread(target=self._news_update_loop, daemon=True)
            thread.start()
            self.update_threads.append(thread)
        
        # Calendar updates
        if self.calendar:
            thread = threading.Thread(target=self._calendar_update_loop, daemon=True)
            thread.start()
            self.update_threads.append(thread)
        
        # Security monitoring
        if self.security:
            thread = threading.Thread(target=self._security_update_loop, daemon=True)
            thread.start()
            self.update_threads.append(thread)
        
        # Network monitoring
        if self.wifi:
            thread = threading.Thread(target=self._network_update_loop, daemon=True)
            thread.start()
            self.update_threads.append(thread)

    def _weather_update_loop(self):
        """Background thread for weather updates"""
        while self.running:
            try:
                self.current_weather = self.weather.get_weather()
                logger.info(f"Weather updated: {self.current_weather.get('description', 'N/A')}")
            except Exception as e:
                logger.error(f"Weather update error: {e}")
            time.sleep(config.WEATHER_REFRESH_INTERVAL)

    def _news_update_loop(self):
        """Background thread for news updates"""
        while self.running:
            try:
                self.current_news = self.news.get_headlines()
                logger.info(f"News updated: {len(self.current_news)} headlines")
            except Exception as e:
                logger.error(f"News update error: {e}")
            time.sleep(config.NEWS_REFRESH_INTERVAL)

    def _calendar_update_loop(self):
        """Background thread for calendar updates"""
        while self.running:
            try:
                self.current_events = self.calendar.get_upcoming_events()
                logger.info(f"Calendar updated: {len(self.current_events)} events")
            except Exception as e:
                logger.error(f"Calendar update error: {e}")
            time.sleep(60)  # Check every minute

    def _security_update_loop(self):
        """Background thread for security monitoring"""
        while self.running:
            try:
                alerts = self.security.check_for_threats()
                if alerts:
                    self.security_alerts = alerts
                    logger.warning(f"Security alerts: {len(alerts)}")
            except Exception as e:
                logger.error(f"Security check error: {e}")
            time.sleep(config.FAIL2BAN_CHECK_INTERVAL)

    def _network_update_loop(self):
        """Background thread for network monitoring"""
        while self.running:
            try:
                self.network_stats = self.wifi.get_network_stats()
                logger.info(f"Network stats updated")
            except Exception as e:
                logger.error(f"Network update error: {e}")
            time.sleep(config.NETWORK_CHECK_INTERVAL)

    def _update_display(self):
        """Update display based on current view"""
        try:
            if self.current_view == "dashboard":
                self._draw_dashboard()
            elif self.current_view == "calendar":
                self._draw_calendar()
            elif self.current_view == "security":
                self._draw_security()
            elif self.current_view == "network":
                self._draw_network()
            elif self.current_view == "ai":
                self._draw_ai()
            
            self.display.render()
        except Exception as e:
            logger.error(f"Display update error: {e}")

    def _draw_dashboard(self):
        """Draw main dashboard view"""
        canvas = self.display.canvas
        
        # Clock
        current_time = datetime.now().strftime("%H:%M:%S")
        self.display.draw_text(f"🕐 {current_time}", (10, 10), size="large")
        
        # Weather
        if self.current_weather:
            temp = self.current_weather.get('temperature', 'N/A')
            desc = self.current_weather.get('description', 'N/A')
            self.display.draw_text(f"🌡️ {temp}°F - {desc}", (10, 40), size="medium")
        
        # Animated face with sentiment
        if self.face and self.current_news:
            headline = self.current_news[0].get('title', '')
            if self.sentiment:
                sentiment = self.sentiment.analyze(headline)
                expression = self._sentiment_to_expression(sentiment)
            else:
                expression = "neutral"
            
            self.face.draw(canvas, expression)
        
        # Top news headline
        if self.current_news:
            headline = self.current_news[0].get('title', 'No news')
            self.display.draw_text(f"📰 {headline[:50]}...", (10, 180), size="small")
        
        # Calendar events
        if self.current_events:
            event = self.current_events[0]
            self.display.draw_text(f"📅 {event.get('title', 'Event')}", (10, 210), size="small")

    def _draw_calendar(self):
        """Draw calendar view"""
        self.display.canvas.fill((0, 0, 0))
        
        # Title
        self.display.draw_text("CALENDAR", (10, 10), size="large")
        
        # List upcoming events
        y_pos = 40
        for event in self.current_events[:5]:
            time_str = event.get('start_time', 'All day')
            title = event.get('title', 'Event')
            self.display.draw_text(f"📅 {time_str} - {title}", (10, y_pos), size="small")
            y_pos += 30

    def _draw_security(self):
        """Draw security monitoring view"""
        self.display.canvas.fill((0, 0, 0))
        
        # Title
        self.display.draw_text("SECURITY STATUS", (10, 10), size="large")
        
        # Fail2ban status
        if self.security:
            status = "🟢 SECURE" if not self.security_alerts else "🔴 THREATS"
            self.display.draw_text(status, (10, 50), size="medium")
        
        # Recent alerts
        y_pos = 80
        for alert in self.security_alerts[:3]:
            self.display.draw_text(f"⚠️ {alert}", (10, y_pos), size="small")
            y_pos += 30

    def _draw_network(self):
        """Draw network monitoring view"""
        self.display.canvas.fill((0, 0, 0))
        
        # Title
        self.display.draw_text("NETWORK STATUS", (10, 10), size="large")
        
        # WiFi info
        if self.network_stats:
            ssid = self.network_stats.get('ssid', 'N/A')
            signal = self.network_stats.get('signal_strength', 'N/A')
            bandwidth = self.network_stats.get('bandwidth', 'N/A')
            
            self.display.draw_text(f"📶 {ssid}", (10, 50), size="medium")
            self.display.draw_text(f"Signal: {signal}%", (10, 80), size="small")
            self.display.draw_text(f"Speed: {bandwidth}", (10, 110), size="small")

    def _draw_ai(self):
        """Draw AI interaction view"""
        self.display.canvas.fill((0, 0, 0))
        
        # Title
        self.display.draw_text("AI ASSISTANT", (10, 10), size="large")
        
        # AI status
        if self.ai:
            self.display.draw_text("🤖 Ready for interaction", (10, 50), size="medium")
            self.display.draw_text("Say something or ask a question", (10, 80), size="small")

    def _sentiment_to_expression(self, sentiment: float) -> str:
        """Convert sentiment score to face expression"""
        if sentiment > config.SENTIMENT_THRESHOLD_POSITIVE:
            return "happy"
        elif sentiment < config.SENTIMENT_THRESHOLD_NEGATIVE:
            return "sad"
        else:
            return "neutral"

    def handle_input(self, event):
        """Handle user input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.stop()
            elif event.key == pygame.K_1:
                self.current_view = "dashboard"
            elif event.key == pygame.K_2:
                self.current_view = "calendar"
            elif event.key == pygame.K_3:
                self.current_view = "security"
            elif event.key == pygame.K_4:
                self.current_view = "network"
            elif event.key == pygame.K_5:
                self.current_view = "ai"

    def stop(self):
        """Stop all services and shutdown"""
        logger.info("Shutting down Whisplay AI Dashboard...")
        self.running = False
        
        # Wait for threads to finish
        for thread in self.update_threads:
            thread.join(timeout=5)
        
        # Cleanup
        self.display.cleanup()
        
        logger.info("Dashboard shutdown complete")
        sys.exit(0)


# ============================================================
# MAIN ENTRY POINT
# ============================================================

def main():
    """Main entry point"""
    print("=" * 60)
    print("WHISPLAY AI DASHBOARD")
    print("Whisplay HAT + Raspberry Pi Zero 2W/4/5")
    print("=" * 60)
    print()
    
    # Create and start dashboard
    dashboard = WhisplayDashboard()
    
    print("Dashboard started. Controls:")
    print("  1 - Dashboard view")
    print("  2 - Calendar view")
    print("  3 - Security view")
    print("  4 - Network view")
    print("  5 - AI view")
    print("  ESC - Exit")
    print()
    
    dashboard.start()


if __name__ == "__main__":
    main()
