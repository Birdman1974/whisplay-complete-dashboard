# ============================================================
# TEXT TO SPEECH - Voice synthesis and output
# ============================================================

import logging
import subprocess
import os
from typing import Optional
import config

logger = logging.getLogger(__name__)


class TextToSpeech:
    """
    Convert text to speech using espeak or Google TTS
    Support for different voices and languages
    """

    def __init__(self):
        """Initialize text-to-speech"""
        self.engine = config.TTS_ENGINE
        self.language = config.TTS_LANGUAGE
        self.voice = config.TTS_VOICE
        self.speed = config.TTS_SPEED
        self.volume = config.TTS_VOLUME
        
        self._check_engine()
        logger.info(f"Text-to-speech initialized ({self.engine})")

    def _check_engine(self):
        """Check if TTS engine is available"""
        try:
            if self.engine == "espeak":
                result = subprocess.run(['which', 'espeak'], 
                                      capture_output=True, timeout=5)
                if result.returncode != 0:
                    logger.warning("espeak not found, installing...")
                    self._install_espeak()
            elif self.engine == "google":
                try:
                    import pyttsx3
                except ImportError:
                    logger.warning("pyttsx3 not found, installing...")
                    os.system("pip3 install pyttsx3")
        except Exception as e:
            logger.error(f"TTS engine check error: {e}")

    def _install_espeak(self):
        """Install espeak"""
        try:
            os.system("sudo apt-get install -y espeak espeak-ng-data")
            logger.info("espeak installed successfully")
        except Exception as e:
            logger.error(f"espeak installation error: {e}")

    def speak(self, text: str, voice: str = None, speed: int = None) -> bool:
        """Speak text"""
        try:
            if not text:
                return False
            
            voice = voice or self.voice
            speed = speed or self.speed
            
            if self.engine == "espeak":
                return self._speak_espeak(text, voice, speed)
            elif self.engine == "google":
                return self._speak_google(text)
            
            return False
            
        except Exception as e:
            logger.error(f"Speech error: {e}")
            return False

    def _speak_espeak(self, text: str, voice: str, speed: int) -> bool:
        """Use espeak for speech synthesis"""
        try:
            cmd = [
                'espeak',
                '-v', voice,
                '-s', str(speed),
                '-a', str(self.volume),
                text
            ]
            
            result = subprocess.run(cmd, timeout=10)
            logger.info(f"Spoke: {text[:50]}...")
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"espeak error: {e}")
            return False

    def _speak_google(self, text: str) -> bool:
        """Use Google Text-to-Speech"""
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            engine.setProperty('rate', self.speed)
            engine.setProperty('volume', self.volume / 100.0)
            
            engine.say(text)
            engine.runAndWait()
            
            logger.info(f"Spoke (Google): {text[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Google TTS error: {e}")
            return False

    def speak_async(self, text: str) -> bool:
        """Speak text asynchronously"""
        try:
            import threading
            
            thread = threading.Thread(target=self.speak, args=(text,), daemon=True)
            thread.start()
            return True
            
        except Exception as e:
            logger.error(f"Async speech error: {e}")
            return False

    def speak_notification(self, title: str, message: str) -> bool:
        """Speak a notification"""
        text = f"{title}. {message}"
        return self.speak_async(text)

    def speak_alert(self, alert_type: str, message: str) -> bool:
        """Speak an alert"""
        alert_sound = {
            'warning': '⚠️ Warning: ',
            'critical': '🚨 Critical alert: ',
            'info': 'ℹ️ Information: ',
            'success': '✅ Success: '
        }
        
        prefix = alert_sound.get(alert_type, '')
        return self.speak_async(prefix + message)

    def set_voice(self, voice: str):
        """Set voice"""
        self.voice = voice
        logger.info(f"Voice changed to: {voice}")

    def set_speed(self, speed: int):
        """Set speech speed (50-300)"""
        self.speed = max(50, min(300, speed))
        logger.info(f"Speed changed to: {self.speed}")

    def set_volume(self, volume: int):
        """Set volume (0-100)"""
        self.volume = max(0, min(100, volume))
        logger.info(f"Volume changed to: {self.volume}")

    def list_voices(self) -> list:
        """List available voices"""
        try:
            if self.engine == "espeak":
                result = subprocess.run(['espeak', '--voices'],
                                      capture_output=True, text=True, timeout=5)
                voices = []
                for line in result.stdout.split('\n')[1:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) > 2:
                            voices.append(parts[3])
                return voices
            
            elif self.engine == "google":
                import pyttsx3
                engine = pyttsx3.init()
                return [v.id for v in engine.getProperty('voices')]
            
        except Exception as e:
            logger.error(f"List voices error: {e}")
        
        return []

    def test_voice(self):
        """Test current voice"""
        test_text = "Hello, this is a test of the Whisplay AI Dashboard voice synthesis system."
        return self.speak(test_text)

    def spell_out(self, text: str) -> bool:
        """Spell out text character by character"""
        try:
            spelled = " ".join(text.upper())
            return self.speak(spelled)
        except Exception as e:
            logger.error(f"Spell out error: {e}")
            return False

    def get_status(self) -> dict:
        """Get TTS status"""
        return {
            'engine': self.engine,
            'language': self.language,
            'voice': self.voice,
            'speed': self.speed,
            'volume': self.volume,
            'available_voices': len(self.list_voices())
        }
