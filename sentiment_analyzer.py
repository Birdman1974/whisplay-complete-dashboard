# ============================================================
# SENTIMENT ANALYZER - AI sentiment analysis
# ============================================================

import logging
from typing import Dict, Tuple
import config

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Analyze sentiment of text using simple NLP
    Can integrate with more advanced models
    """

    def __init__(self):
        """Initialize sentiment analyzer"""
        self.positive_words = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'love', 'happy', 'joy', 'beautiful', 'perfect', 'awesome',
            'incredible', 'outstanding', 'brilliant', 'super', 'best'
        ]
        
        self.negative_words = [
            'bad', 'terrible', 'awful', 'horrible', 'hate', 'sad', 'angry',
            'upset', 'disappointed', 'poor', 'worst', 'disgusting', 'ugly',
            'stupid', 'dumb', 'fail', 'problem', 'issue', 'error'
        ]
        
        self.history = []
        logger.info("Sentiment analyzer initialized")

    def analyze(self, text: str) -> float:
        """
        Analyze sentiment of text
        Returns score from -1.0 (very negative) to 1.0 (very positive)
        """
        try:
            if not text:
                return 0.0
            
            text_lower = text.lower()
            
            # Count positive and negative words
            positive_count = sum(1 for word in self.positive_words if word in text_lower)
            negative_count = sum(1 for word in self.negative_words if word in text_lower)
            
            # Calculate sentiment score
            total = positive_count + negative_count
            if total == 0:
                score = 0.0
            else:
                score = (positive_count - negative_count) / total
            
            # Store in history
            self.history.append({
                'text': text[:100],
                'score': score,
                'timestamp': self._get_timestamp()
            })
            
            logger.debug(f"Sentiment analyzed: {score:.2f}")
            return score
            
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return 0.0

    def analyze_multiple(self, texts: list) -> Dict[str, float]:
        """Analyze sentiment of multiple texts"""
        results = {}
        for text in texts:
            results[text[:50]] = self.analyze(text)
        return results

    def get_emotion(self, score: float) -> str:
        """Convert sentiment score to emotion"""
        if score > config.SENTIMENT_THRESHOLD_POSITIVE:
            return "😊 Happy"
        elif score < config.SENTIMENT_THRESHOLD_NEGATIVE:
            return "😢 Sad"
        else:
            return "😐 Neutral"

    def get_emoji(self, score: float) -> str:
        """Get emoji for sentiment"""
        if score > 0.6:
            return "😄"
        elif score > 0.3:
            return "🙂"
        elif score > -0.3:
            return "😐"
        elif score > -0.6:
            return "☹️"
        else:
            return "😠"

    def get_history(self, limit: int = 10) -> list:
        """Get sentiment analysis history"""
        return self.history[-limit:]

    def get_summary(self) -> Dict:
        """Get sentiment summary"""
        if not self.history:
            return {'average_sentiment': 0.0, 'total_analyzed': 0}
        
        scores = [h['score'] for h in self.history]
        average = sum(scores) / len(scores)
        
        return {
            'average_sentiment': round(average, 2),
            'total_analyzed': len(self.history),
            'most_recent': self.history[-1]['score'] if self.history else 0.0,
            'trend': self._calculate_trend()
        }

    def _calculate_trend(self) -> str:
        """Calculate sentiment trend"""
        if len(self.history) < 2:
            return "stable"
        
        recent = sum(h['score'] for h in self.history[-5:]) / 5
        older = sum(h['score'] for h in self.history[-10:-5]) / 5
        
        if recent > older:
            return "improving"
        elif recent < older:
            return "declining"
        else:
            return "stable"

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

    def reset_history(self):
        """Clear history"""
        self.history = []
        logger.info("History cleared")
