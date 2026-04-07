# ============================================================
# AI ENGINE - Integration with AI/ML models
# ============================================================

import logging
import requests
import json
from typing import Dict, List, Optional
import config

logger = logging.getLogger(__name__)


class AIEngine:
    """
    Integration with AI models (Ollama, OpenAI, local models)
    Handle natural language processing and AI conversations
    """

    def __init__(self):
        """Initialize AI engine"""
        self.provider = config.AI_PROVIDER
        self.model = config.AI_MODEL
        self.temperature = config.AI_TEMPERATURE
        self.api_key = config.OPENAI_API_KEY if self.provider == "openai" else None
        self.base_url = config.OLLAMA_BASE_URL if self.provider == "ollama" else None
        self.conversation_history = []
        self.max_history = 10
        
        self._test_connection()
        logger.info(f"AI engine initialized ({self.provider})")

    def _test_connection(self):
        """Test connection to AI service"""
        try:
            if self.provider == "ollama":
                response = requests.get(f"{self.base_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    logger.info("Connected to Ollama")
                else:
                    logger.warning("Could not connect to Ollama")
            elif self.provider == "openai":
                logger.info("OpenAI API configured")
        except Exception as e:
            logger.warning(f"AI service connection test failed: {e}")

    def chat(self, user_message: str, context: str = None) -> str:
        """Chat with AI"""
        try:
            # Add to conversation history
            self.conversation_history.append({
                'role': 'user',
                'content': user_message
            })
            
            # Keep history size manageable
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = self.conversation_history[-self.max_history:]
            
            # Get response
            if self.provider == "ollama":
                response = self._chat_ollama(user_message, context)
            elif self.provider == "openai":
                response = self._chat_openai(user_message, context)
            else:
                response = self._chat_local(user_message, context)
            
            # Add response to history
            self.conversation_history.append({
                'role': 'assistant',
                'content': response
            })
            
            logger.info(f"AI response: {response[:100]}...")
            return response
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return "I encountered an error processing your request."

    def _chat_ollama(self, message: str, context: str = None) -> str:
        """Chat using Ollama"""
        try:
            url = f"{self.base_url}/api/generate"
            
            prompt = message
            if context:
                prompt = f"Context: {context}\n\nQuestion: {message}"
            
            payload = {
                'model': self.model,
                'prompt': prompt,
                'stream': False,
                'temperature': self.temperature
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data.get('response', 'No response').strip()
            
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            return "Error communicating with AI model"

    def _chat_openai(self, message: str, context: str = None) -> str:
        """Chat using OpenAI API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            messages = []
            
            # Add system context
            if context:
                messages.append({
                    'role': 'system',
                    'content': context
                })
            
            # Add conversation history
            messages.extend(self.conversation_history)
            
            payload = {
                'model': self.model,
                'messages': messages,
                'temperature': self.temperature,
                'max_tokens': 500
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            logger.error(f"OpenAI chat error: {e}")
            return "Error communicating with OpenAI"

    def _chat_local(self, message: str, context: str = None) -> str:
        """Chat using simple local fallback"""
        try:
            # Simple rule-based responses
            message_lower = message.lower()
            
            if 'weather' in message_lower:
                return "I can help you check the weather. What location would you like to check?"
            elif 'time' in message_lower or 'what time' in message_lower:
                from datetime import datetime
                return f"The current time is {datetime.now().strftime('%I:%M %p')}"
            elif 'hello' in message_lower or 'hi' in message_lower:
                return "Hello! I'm the Whisplay AI Dashboard. How can I assist you?"
            elif 'news' in message_lower:
                return "I can fetch the latest news for you. Would you like general news or a specific category?"
            else:
                return "I'm ready to help. What would you like to know?"
            
        except Exception as e:
            logger.error(f"Local chat error: {e}")
            return "I encountered an error."

    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of text using AI"""
        try:
            prompt = f"Analyze the sentiment of this text and respond with only: positive, negative, or neutral.\n\nText: {text}"
            response = self.chat(prompt)
            
            sentiment = response.lower().strip()
            if 'positive' in sentiment:
                score = 0.8
            elif 'negative' in sentiment:
                score = -0.8
            else:
                score = 0.0
            
            return {
                'sentiment': sentiment,
                'score': score
            }
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return {'sentiment': 'unknown', 'score': 0.0}

    def generate_response(self, context: str, task: str) -> str:
        """Generate response for specific task"""
        try:
            prompt = f"Context: {context}\n\nTask: {task}\n\nProvide a helpful response:"
            return self.chat(prompt, context=context)
        except Exception as e:
            logger.error(f"Response generation error: {e}")
            return "Unable to generate response"

    def summarize(self, text: str, max_length: int = 100) -> str:
        """Summarize text"""
        try:
            prompt = f"Summarize this text in {max_length} characters or less:\n\n{text}"
            return self.chat(prompt)
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            return text[:max_length]

    def answer_question(self, question: str, context: str = None) -> str:
        """Answer a question"""
        try:
            if context:
                prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
            else:
                prompt = f"Question: {question}\n\nAnswer:"
            
            return self.chat(prompt, context=context)
        except Exception as e:
            logger.error(f"Question answering error: {e}")
            return "I cannot answer that question."

    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

    def set_temperature(self, temperature: float):
        """Set temperature (creativity level)"""
        self.temperature = max(0.0, min(2.0, temperature))
        logger.info(f"Temperature set to: {self.temperature}")

    def get_status(self) -> Dict:
        """Get AI engine status"""
        return {
            'provider': self.provider,
            'model': self.model,
            'temperature': self.temperature,
            'history_length': len(self.conversation_history),
            'connected': self._check_status()
        }

    def _check_status(self) -> bool:
        """Check if AI service is available"""
        try:
            if self.provider == "ollama":
                response = requests.get(f"{self.base_url}/api/tags", timeout=2)
                return response.status_code == 200
            elif self.provider == "openai":
                return bool(self.api_key)
            return True
        except:
            return False
