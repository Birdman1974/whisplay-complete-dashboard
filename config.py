# ============================================================
# WHISPLAY AI DASHBOARD - MASTER CONFIGURATION
# ============================================================
# This is your central configuration file for ALL features
# ============================================================

# ============================================================
# API KEYS & CREDENTIALS (GET THESE FIRST!)
# ============================================================
WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # https://openweathermap.org/api
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"                # https://newsapi.org/
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"           # https://openai.com/api (optional)

# ============================================================
# LOCATION & UNITS
# ============================================================
WEATHER_CITY = "New York"
WEATHER_COUNTRY = "US"
WEATHER_UNITS = "imperial"  # "imperial" for Fahrenheit, "metric" for Celsius
TIMEZONE = "America/New_York"

# ============================================================
# DISPLAY SETTINGS
# ============================================================
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
DISPLAY_REFRESH_RATE = 5  # seconds
DISPLAY_TYPE = "pygame"   # "pygame" for testing, "actual_hardware" for real display
MOCK_MODE = True  # Set to False when on actual Whisplay hardware
FRAMERATE = 30  # FPS for animations

# ============================================================
# FEATURE TOGGLES (Enable/Disable as needed)
# ============================================================

# AI & MACHINE LEARNING
ENABLE_AI = True
ENABLE_SENTIMENT_ANALYSIS = True
ENABLE_OLLAMA = False  # Requires Ollama installed
ENABLE_OPENAI = False  # Requires OPENAI_API_KEY
ENABLE_VOICE_RECOGNITION = False  # Requires Vosk or Google Speech-to-Text

# MULTIMEDIA & ENTERTAINMENT
ENABLE_MUSIC_PLAYER = False
ENABLE_RADIO = False
ENABLE_PODCAST = False
ENABLE_VISUALIZATION = True  # Audio spectrum visualization

# SMART HOME & SECURITY
ENABLE_HOME_ASSISTANT = False
ENABLE_FAIL2BAN = True  # System intrusion detection
ENABLE_SNORT = False  # Network intrusion detection (advanced)
ENABLE_WEATHER_ALERTS = True

# SYSTEM MONITORING
ENABLE_SYSTEM_DASHBOARD = True
ENABLE_NETWORK_MONITOR = True
ENABLE_RESOURCE_MONITOR = True

# CALENDAR & SCHEDULING
ENABLE_CALENDAR = True
ENABLE_REMINDERS = True
ENABLE_SCHEDULED_TASKS = True
CALENDAR_SOURCE = "local"  # "local" or "google" (requires Google Calendar API)

# DISPLAY FEATURES
ENABLE_LIVE_CHARTS = True
ENABLE_ANIMATED_FACE = True
ENABLE_LED_CONTROL = False  # Requires RGB LED setup
ENABLE_TEXT_TO_SPEECH = True

# NEWS & INFORMATION
ENABLE_NEWS = True
ENABLE_HEADLINE_SCROLLING = True
ENABLE_NEWS_SORTING = True

# NETWORK TOOLS
ENABLE_WIFI_MONITORING = True
ENABLE_NETWORK_ANALYZER = True
ENABLE_CONNECTION_STATS = True

# ============================================================
# AI & MACHINE LEARNING CONFIGURATION
# ============================================================

# Ollama Settings (Offline AI)
OLLAMA_MODEL = "neural-chat"  # lightweight model for Pi Zero 2W
OLLAMA_API_URL = "http://localhost:11434"
OLLAMA_TEMPERATURE = 0.7

# OpenAI Settings
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.7
OPENAI_MAX_TOKENS = 150

# Sentiment Analysis
SENTIMENT_THRESHOLD_POSITIVE = 0.5
SENTIMENT_THRESHOLD_NEGATIVE = -0.5

# Voice Recognition
VOICE_RECOGNITION_ENGINE = "google"  # "google" or "vosk" (vosk = offline)
VOICE_CONFIDENCE_THRESHOLD = 0.7

# ============================================================
# WEATHER CONFIGURATION
# ============================================================

WEATHER_REFRESH_INTERVAL = 600  # 10 minutes in seconds
WEATHER_SHOW_FORECAST = True
WEATHER_FORECAST_DAYS = 3
WEATHER_SHOW_ALERTS = True
WEATHER_ALERT_TYPES = ["severe", "wind", "rain", "snow", "extreme_temp"]

# Temperature alerts
TEMP_HIGH_ALERT = 95  # Fahrenheit
TEMP_LOW_ALERT = 32   # Freezing

# ============================================================
# NEWS CONFIGURATION
# ============================================================

NEWS_REFRESH_INTERVAL = 600  # 10 minutes
NEWS_SOURCE = "top-headlines"  # "top-headlines" or "everything"
NEWS_COUNTRY = "us"
NEWS_LANGUAGE = "en"
NEWS_CATEGORY = "general"  # general, business, entertainment, health, science, sports, technology
NEWS_SORT_BY = "publishedAt"  # "publishedAt", "relevancy", "popularity"
NEWS_ARTICLES_LIMIT = 10
NEWS_HEADLINE_DISPLAY_TIME = 5  # seconds per headline
NEWS_SCROLL_SPEED = 2  # pixels per frame

# ============================================================
# CALENDAR & SCHEDULING
# ============================================================

CALENDAR_SHOW_TIME = True
CALENDAR_SHOW_DATE = True
CALENDAR_SHOW_EVENTS = True
CALENDAR_SHOW_REMINDERS = True
CALENDAR_TIMEZONE = TIMEZONE
CALENDAR_REMINDER_ADVANCE = 300  # seconds (5 minutes)

# Local calendar file
CALENDAR_FILE = "events.json"

# Google Calendar (optional)
GOOGLE_CALENDAR_ID = "primary"
GOOGLE_CALENDAR_CREDENTIALS = "credentials.json"

# ============================================================
# SECURITY & MONITORING
# ============================================================

# Fail2ban Configuration
FAIL2BAN_ENABLED = True
FAIL2BAN_CHECK_INTERVAL = 60  # seconds
FAIL2BAN_LOG_FILE = "/var/log/auth.log"
FAIL2BAN_THRESHOLD = 5  # failed attempts before alert

# Snort (Network Intrusion Detection)
SNORT_ENABLED = False
SNORT_NETWORK_INTERFACE = "eth0"
SNORT_ALERT_LEVEL = "medium"

# System Security Alerts
SECURITY_ALERT_ON_FAILED_LOGIN = True
SECURITY_ALERT_ON_UNAUTHORIZED_ACCESS = True
SECURITY_ALERT_ON_UNUSUAL_ACTIVITY = True

# ============================================================
# NETWORK MONITORING (WiFi Bugging)
# ============================================================

NETWORK_MONITOR_ENABLED = True
NETWORK_INTERFACE = "wlan0"  # or "eth0" for ethernet
NETWORK_CHECK_INTERVAL = 30  # seconds

# WiFi Analysis
WIFI_SHOW_SIGNAL_STRENGTH = True
WIFI_SHOW_CHANNEL = True
WIFI_SHOW_FREQUENCY = True
WIFI_SHOW_CONNECTED_DEVICES = True
WIFI_SHOW_BANDWIDTH_USAGE = True

# Network Threats
DETECT_UNUSUAL_TRAFFIC = True
DETECT_UNAUTHORIZED_DEVICES = True
DETECT_DDOS_ATTEMPTS = False
DETECT_PORT_SCANNING = True

# ============================================================
# DISPLAY & ANIMATION SETTINGS
# ============================================================

# Animated Face
FACE_SIZE = 100  # pixels
FACE_BLINK_RATE = 0.3  # blinks per second
FACE_BLINK_DURATION = 150  # milliseconds
FACE_COLOR_NEUTRAL = (255, 255, 0)  # Yellow
FACE_COLOR_HAPPY = (0, 255, 0)      # Green
FACE_COLOR_SAD = (255, 0, 0)        # Red
FACE_COLOR_ANGRY = (255, 165, 0)    # Orange
FACE_COLOR_CONCERNED = (255, 255, 0) # Yellow

# LED Control (if RGB LEDs connected)
LED_PIN_RED = 17
LED_PIN_GREEN = 27
LED_PIN_BLUE = 22
LED_BRIGHTNESS = 255
LED_ANIMATION_SPEED = 0.5

# ============================================================
# GUI & INTERFACE SETTINGS
# ============================================================

GUI_THEME = "dark"  # "dark" or "light"
GUI_FONT_SIZE = 12
GUI_BUTTON_SIZE = (100, 40)
GUI_SHOW_CLOCK = True
GUI_SHOW_STATS = True
GUI_LAYOUT = "dashboard"  # "dashboard", "minimalist", "detailed"

# ============================================================
# PERFORMANCE OPTIMIZATION
# ============================================================

# Reduce CPU usage on Pi Zero 2W
OPTIMIZE_FOR_PERFORMANCE = True
REDUCE_ANIMATION_COMPLEXITY = False
DISABLE_EFFECTS_ON_LOW_BATTERY = True
BATTERY_THRESHOLD = 20  # percentage

# Memory management
MAX_CACHE_SIZE = 50 * 1024 * 1024  # 50MB
CLEANUP_INTERVAL = 3600  # 1 hour

# ============================================================
# LOGGING & DEBUGGING
# ============================================================

DEBUG_MODE = False
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "whisplay_dashboard.log"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# What to log
LOG_API_CALLS = False
LOG_DISPLAY_UPDATES = False
LOG_ERRORS = True
LOG_SECURITY_EVENTS = True

# ============================================================
# AUDIO SETTINGS
# ============================================================

# Text-to-Speech
ENABLE_AUDIO_OUTPUT = True
TTS_ENGINE = "espeak"  # "espeak", "pico", or "gtts"
TTS_RATE = 150  # words per minute
TTS_PITCH = 50
TTS_VOLUME = 100

# Audio Input
ENABLE_AUDIO_INPUT = False
MICROPHONE_DEVICE = "default"
AUDIO_RECORDING_QUALITY = "16000Hz"  # Sample rate

# ============================================================
# POWER MANAGEMENT (PiSugar)
# ============================================================

PISU_SUGAR_ENABLED = True
SHOW_BATTERY_LEVEL = True
BATTERY_WARNING_LEVEL = 30  # percentage
BATTERY_CRITICAL_LEVEL = 10
SHUTDOWN_ON_CRITICAL_BATTERY = True
LOW_POWER_MODE_THRESHOLD = 50  # Enable power saving below this %

# ============================================================
# AUTO-START & SCHEDULING
# ============================================================

AUTOSTART_ON_BOOT = True
AUTOSTART_DELAY = 5  # seconds
ENABLE_SCHEDULED_SLEEP = False
SLEEP_START_TIME = "22:00"
SLEEP_END_TIME = "07:00"

# ============================================================
# DATA STORAGE
# ============================================================

DATA_DIRECTORY = "./data"
CACHE_DIRECTORY = "./cache"
LOG_DIRECTORY = "./logs"
CONFIG_BACKUP_DIRECTORY = "./backups"

# Database
USE_DATABASE = False
DATABASE_TYPE = "sqlite"  # "sqlite" or "postgres"
DATABASE_PATH = "./whisplay.db"

# ============================================================
# ADVANCED SETTINGS (Modify with caution!)
# ============================================================

# Threading
USE_THREADING = True
MAX_THREADS = 4

# API Timeout
API_TIMEOUT = 10  # seconds
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds

# Network
PROXY_ENABLED = False
PROXY_URL = "http://proxy.example.com:8080"

# Custom Headers for API calls
CUSTOM_USER_AGENT = "Whisplay-AI-Dashboard/1.0"

# ============================================================
# FEATURE FLAGS (For development/testing)
# ============================================================

FEATURE_NEW_FACE_ENGINE = True
FEATURE_ADVANCED_SENTIMENT = True
FEATURE_PREDICTIVE_WEATHER = False
FEATURE_VOICE_COMMANDS = False
FEATURE_MULTI_USER_SUPPORT = False

# ============================================================
# SYSTEM PATHS (Don't change unless you know what you're doing)
# ============================================================

PROJECT_ROOT = "."
ASSETS_PATH = "./assets"
FONTS_PATH = "./assets/fonts"
SOUNDS_PATH = "./assets/sounds"
IMAGES_PATH = "./assets/images"

# ============================================================
# END OF CONFIGURATION
# ============================================================
# Remember to set API keys before running!
# Test with: python3 main.py --test
