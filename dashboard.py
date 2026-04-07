# ============================================================
# WHISPLAY AI DASHBOARD - Main Application
# ============================================================

import logging
import time
import threading
from datetime import datetime
import config

# Import all modules
from weather_service import WeatherService
from news_service import NewsService
from calendar_service import CalendarService
from animated_face import AnimatedFace
from wifi_monitor import WiFiMonitor
from sentiment_analyzer import SentimentAnalyzer
from display_manager import DisplayManager
from text_to_speech import TextToSpeech
from ai_engine import AIEngine
from led_controller import LEDController

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WhisplayDashboard:
    """
    Main Whisplay AI Dashboard application
    Orchestrates all services and displays
    """

    def __init__(self):
        """Initialize dashboard"""
        logger.info("=" * 60)
        logger.info("WHISPLAY AI DASHBOARD STARTING")
        logger.info("=" * 60)
        
        # Initialize services
        self.weather = WeatherService()
        self.news = NewsService()
        self.calendar = CalendarService()
        self.face = AnimatedFace()
        self.wifi = WiFiMonitor()
        self.sentiment = SentimentAnalyzer()
        self.display = DisplayManager(
            width=config.DISPLAY_WIDTH,
            height=config.DISPLAY_HEIGHT,
            mock_mode=config.DISPLAY_MOCK_MODE
        )
        self.tts = TextToSpeech()
        self.ai = AIEngine()
        self.led = LEDController()
        
        # Application state
        self.running = True
        self.current_screen = "home"
        self.screen_update_interval = config.SCREEN_UPDATE_INTERVAL
        self.last_update_time = 0
        
        logger.info("All services initialized successfully")

    def run(self):
        """Main application loop"""
        try:
            # Start update thread
            update_thread = threading.Thread(target=self._update_loop, daemon=True)
            update_thread.start()
            
            # Start display loop
            self._display_loop()
            
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            self.shutdown()
        except Exception as e:
            logger.error(f"Application error: {e}", exc_info=True)
            self.shutdown()

    def _update_loop(self):
        """Background update loop for services"""
        logger.info("Update loop started")
        
        while self.running:
            try:
                current_time = time.time()
                
                # Update weather every 10 minutes
                if current_time - getattr(self, '_last_weather_update', 0) > 600:
                    self.weather.get_weather()
                    self.weather.check_weather_alerts()
                    self._last_weather_update = current_time
                
                # Update news every 15 minutes
                if current_time - getattr(self, '_last_news_update', 0) > 900:
                    self.news.get_headlines()
                    self._last_news_update = current_time
                
                # Check calendar reminders
                self.calendar.check_reminders()
                
                # Detect WiFi threats
                if current_time - getattr(self, '_last_wifi_check', 0) > 30:
                    self.wifi.get_network_stats()
                    self.wifi.detect_threats()
                    self._last_wifi_check = current_time
                
                # Check alerts and update LED
                self._check_alerts()
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Update loop error: {e}")
                time.sleep(5)

    def _display_loop(self):
        """Main display loop"""
        logger.info("Display loop started")
        
        while self.running:
            try:
                current_time = time.time()
                
                # Update display at specified interval
                if current_time - self.last_update_time > self.screen_update_interval:
                    self._render_screen()
                    self.last_update_time = current_time
                
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Display loop error: {e}")
                time.sleep(1)

    def _render_screen(self):
        """Render current screen"""
        try:
            self.display.clear()
            
            if self.current_screen == "home":
                self._render_home_screen()
            elif self.current_screen == "weather":
                self._render_weather_screen()
            elif self.current_screen == "news":
                self._render_news_screen()
            elif self.current_screen == "calendar":
                self._render_calendar_screen()
            elif self.current_screen == "network":
                self._render_network_screen()
            elif self.current_screen == "status":
                self._render_status_screen()
            
            self.display.render()
            
        except Exception as e:
            logger.error(f"Render error: {e}")

    def _render_home_screen(self):
        """Render home screen"""
        try:
            # Title
            self.display.draw_text("WHISPLAY AI", (10, 10), size="large", color=(0, 255, 255))
            
            # Current time
            current_time = datetime.now().strftime("%H:%M:%S")
            self.display.draw_text(current_time, (10, 50), size="medium")
            
            # Quick status
            weather_summary = self.weather.get_summary()
            temp = weather_summary.get('temperature', '?')
            weather_text = f"{weather_summary.get('icon', '?')} {temp}°"
            self.display.draw_text(weather_text, (10, 80))
            
            # News headline
            if self.news.headlines:
                headline = self.news.get_scrolling_headline()
                title = headline.get('title', '')[:40]
                self.display.draw_text(f"📰 {title}...", (10, 110), size="small")
            
            # Calendar events
            today_events = self.calendar.get_today_events()
            if today_events:
                event = today_events[0]
                event_text = self.calendar.format_event_for_display(event)
                self.display.draw_text(event_text, (10, 140), size="small")
            
            # WiFi status
            wifi_summary = self.wifi.get_summary()
            signal = wifi_summary.get('signal_strength', 0)
            wifi_text = f"📶 {signal}%"
            self.display.draw_text(wifi_text, (10, 170))
            
            # Alerts
            if self.weather.alerts or self.wifi.threats_detected:
                self.display.draw_text("⚠️ ALERTS ACTIVE", (10, 200), color=(255, 0, 0))
            
        except Exception as e:
            logger.error(f"Home screen render error: {e}")

    def _render_weather_screen(self):
        """Render weather screen"""
        try:
            self.display.draw_text("WEATHER", (10, 10), size="large")
            
            weather = self.weather.get_summary()
            self.display.draw_text(f"City: {weather.get('city', 'Unknown')}", (10, 50))
            self.display.draw_text(f"Temp: {weather.get('temperature', '?')}°", (10, 70))
            self.display.draw_text(f"Feels: {weather.get('feels_like', '?')}°", (10, 90))
            self.display.draw_text(f"Humidity: {weather.get('humidity', '?')}%", (10, 110))
            self.display.draw_text(f"Wind: {weather.get('wind_speed', '?')} m/s", (10, 130))
            self.display.draw_text(f"Description: {weather.get('description', 'N/A')}", (10, 150))
            
            # Alerts
            if self.weather.alerts:
                self.display.draw_text("⚠️ ALERTS:", (10, 180))
                for alert in self.weather.alerts[:2]:
                    self.display.draw_text(alert.get('message', '')[:40], (15, 200))
            
        except Exception as e:
            logger.error(f"Weather screen render error: {e}")

    def _render_news_screen(self):
        """Render news screen"""
        try:
            self.display.draw_text("NEWS", (10, 10), size="large")
            
            if self.news.headlines:
                headline = self.news.headlines[0]
                title = headline.get('title', '')[:45]
                self.display.draw_text(title, (10, 50), size="small")
                
                source = headline.get('source', 'Unknown')
                self.display.draw_text(f"Source: {source}", (10, 100))
                
                desc = headline.get('description', '')[:50]
                self.display.draw_text(desc, (10, 130), size="small")
            else:
                self.display.draw_text("No headlines available", (10, 100))
            
        except Exception as e:
            logger.error(f"News screen render error: {e}")

    def _render_calendar_screen(self):
        """Render calendar screen"""
        try:
            self.display.draw_text("CALENDAR", (10, 10), size="large")
            
            today_events = self.calendar.get_today_events()
            
            if today_events:
                self.display.draw_text("Today's Events:", (10, 50))
                for i, event in enumerate(today_events[:3]):
                    event_str = self.calendar.format_event_for_display(event)
                    self.display.draw_text(event_str, (10, 70 + i * 40), size="small")
            else:
                self.display.draw_text("No events today", (10, 100))
            
            # Upcoming
            upcoming = self.calendar.get_upcoming_events(days=1, limit=1)
            if upcoming:
                self.display.draw_text("Next:", (10, 180))
                event_str = self.calendar.format_event_for_display(upcoming[0])
                self.display.draw_text(event_str, (10, 200), size="small")
            
        except Exception as e:
            logger.error(f"Calendar screen render error: {e}")

    def _render_network_screen(self):
        """Render network status screen"""
        try:
            self.display.draw_text("NETWORK", (10, 10), size="large")
            
            wifi_info = self.wifi.format_for_display()
            self.display.draw_text(wifi_info, (10, 50), size="small")
            
            # Threats
            if self.wifi.threats_detected:
                self.display.draw_text("🚨 THREATS DETECTED", (10, 120), color=(255, 0, 0))
                for threat in self.wifi.threats_detected[:2]:
                    msg = threat.get('message', '')[:40]
                    self.display.draw_text(msg, (10, 150), color=(255, 0, 0), size="small")
            else:
                self.display.draw_text("✅ Network Secure", (10, 120), color=(0, 255, 0))
            
        except Exception as e:
            logger.error(f"Network screen render error: {e}")

    def _render_status_screen(self):
        """Render system status screen"""
        try:
            self.display.draw_text("STATUS", (10, 10), size="large")
            
            # Weather status
            weather_status = self.weather.get_summary()
            self.display.draw_text(f"Weather: OK", (10, 50))
            
            # News status
            news_status = self.news.get_summary()
            self.display.draw_text(f"News: {news_status['total_articles']} articles", (10, 70))
            
            # Calendar status
            cal_status = self.calendar.get_summary()
            self.display.draw_text(f"Calendar: {cal_status['total_events']} events", (10, 90))
            
            # WiFi status
            wifi_status = self.wifi.get_summary()
            self.display.draw_text(f"WiFi: {wifi_status['signal_strength']}%", (10, 110))
            
            # AI status
            ai_status = self.ai.get_status()
            self.display.draw_text(f"AI: {ai_status['provider']}", (10, 130))
            
        except Exception as e:
            logger.error(f"Status screen render error: {e}")

    def _check_alerts(self):
        """Check for alerts and update LED"""
        try:
            has_critical = False
            has_warning = False
            
            # Check weather alerts
            if self.weather.alerts:
                for alert in self.weather.alerts:
                    if alert.get('severity') == 'high':
                        has_critical = True
                    else:
                        has_warning = True
            
            # Check WiFi threats
            if self.wifi.threats_detected:
                for threat in self.wifi.threats_detected:
                    if threat.get('severity') == 'high':
                        has_critical = True
                    else:
                        has_warning = True
            
            # Check calendar reminders
            if self.calendar.reminders:
                has_warning = True
            
            # Update LED accordingly
            if has_critical:
                self.led.set_status_color('critical')
            elif has_warning:
                self.led.set_status_color('warning')
            else:
                self.led.set_status_color('ok')
            
        except Exception as e:
            logger.error(f"Alert check error: {e}")

    def switch_screen(self, screen_name: str):
        """Switch to different screen"""
        valid_screens = ["home", "weather", "news", "calendar", "network", "status"]
        if screen_name in valid_screens:
            self.current_screen = screen_name
            logger.info(f"Switched to screen: {screen_name}")
        else:
            logger.warning(f"Invalid screen: {screen_name}")

    def shutdown(self):
        """Shutdown dashboard"""
        logger.info("Shutting down Whisplay AI Dashboard...")
        self.running = False
        
        try:
            self.led.turn_off()
            self.display.cleanup()
            logger.info("Shutdown complete")
        except Exception as e:
            logger.error(f"Shutdown error: {e}")

    def get_status(self) -> dict:
        """Get overall system status"""
        return {
            'weather': self.weather.get_summary(),
            'news': self.news.get_summary(),
            'calendar': self.calendar.get_summary(),
            'wifi': self.wifi.get_summary(),
            'ai': self.ai.get_status(),
            'led': self.led.get_status(),
            'timestamp': datetime.now().isoformat()
        }


def main():
    """Main entry point"""
    try:
        dashboard = WhisplayDashboard()
        dashboard.run()
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
