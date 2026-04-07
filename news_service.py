# ============================================================
# NEWS SERVICE - Get news headlines with sentiment analysis
# ============================================================

import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional
import config

logger = logging.getLogger(__name__)


class NewsService:
    """
    Fetch news headlines from NewsAPI
    Support headline scrolling and sorting
    """

    def __init__(self):
        """Initialize news service"""
        self.api_key = config.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2"
        self.headlines = []
        self.current_index = 0
        
        logger.info("News service initialized")

    def get_headlines(self, limit: int = None) -> List[Dict]:
        """Get top news headlines"""
        try:
            if limit is None:
                limit = config.NEWS_ARTICLES_LIMIT
            
            url = f"{self.base_url}/top-headlines"
            params = {
                'country': config.NEWS_COUNTRY,
                'language': config.NEWS_LANGUAGE,
                'category': config.NEWS_CATEGORY,
                'sortBy': config.NEWS_SORT_BY,
                'pageSize': limit,
                'apiKey': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] != 'ok':
                logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                return []
            
            self.headlines = []
            for article in data.get('articles', []):
                headline = {
                    'title': article.get('title', 'No title'),
                    'description': article.get('description', ''),
                    'source': article['source'].get('name', 'Unknown'),
                    'url': article.get('url', ''),
                    'image_url': article.get('urlToImage', ''),
                    'published_at': article.get('publishedAt', ''),
                    'content': article.get('content', ''),
                    'author': article.get('author', 'Unknown'),
                    'timestamp': datetime.now().isoformat()
                }
                self.headlines.append(headline)
            
            logger.info(f"Headlines updated: {len(self.headlines)} articles")
            return self.headlines
            
        except requests.exceptions.RequestException as e:
            logger.error(f"News API error: {e}")
            return []
        except KeyError as e:
            logger.error(f"News data parsing error: {e}")
            return []

    def search_news(self, query: str, limit: int = 10) -> List[Dict]:
        """Search news by keyword"""
        try:
            url = f"{self.base_url}/everything"
            params = {
                'q': query,
                'sortBy': 'publishedAt',
                'language': config.NEWS_LANGUAGE,
                'pageSize': limit,
                'apiKey': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for article in data.get('articles', []):
                result = {
                    'title': article.get('title', 'No title'),
                    'description': article.get('description', ''),
                    'source': article['source'].get('name', 'Unknown'),
                    'url': article.get('url', ''),
                    'published_at': article.get('publishedAt', ''),
                    'relevance_score': 1.0
                }
                results.append(result)
            
            logger.info(f"Search results: {len(results)} articles for '{query}'")
            return results
            
        except Exception as e:
            logger.error(f"News search error: {e}")
            return []

    def get_by_category(self, category: str) -> List[Dict]:
        """Get headlines by category"""
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'country': config.NEWS_COUNTRY,
                'category': category,
                'pageSize': config.NEWS_ARTICLES_LIMIT,
                'apiKey': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=config.API_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for article in data.get('articles', []):
                result = {
                    'title': article.get('title', 'No title'),
                    'description': article.get('description', ''),
                    'source': article['source'].get('name', 'Unknown'),
                    'category': category,
                    'published_at': article.get('publishedAt', '')
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Category fetch error: {e}")
            return []

    def sort_headlines(self, sort_by: str = 'publishedAt') -> List[Dict]:
        """Sort headlines by different criteria"""
        if sort_by == 'publishedAt':
            self.headlines.sort(key=lambda x: x.get('published_at', ''), reverse=True)
        elif sort_by == 'relevance':
            self.headlines.sort(key=lambda x: x.get('title', ''))
        elif sort_by == 'source':
            self.headlines.sort(key=lambda x: x.get('source', ''))
        
        logger.info(f"Headlines sorted by: {sort_by}")
        return self.headlines

    def get_scrolling_headline(self) -> Dict:
        """Get next headline for scrolling display"""
        if not self.headlines:
            return {}
        
        headline = self.headlines[self.current_index % len(self.headlines)]
        self.current_index += 1
        
        return headline

    def reset_scroll(self):
        """Reset scroll position"""
        self.current_index = 0

    def get_trending(self, limit: int = 5) -> List[Dict]:
        """Get trending news"""
        if not self.headlines:
            return []
        
        # Return most recent articles as trending
        return self.headlines[:limit]

    def filter_by_source(self, source: str) -> List[Dict]:
        """Filter headlines by news source"""
        filtered = [h for h in self.headlines if h.get('source', '').lower() == source.lower()]
        logger.info(f"Filtered {len(filtered)} articles from {source}")
        return filtered

    def get_summary(self) -> Dict:
        """Get news service summary"""
        return {
            'total_articles': len(self.headlines),
            'categories_available': [
                'general', 'business', 'entertainment', 'health', 
                'science', 'sports', 'technology'
            ],
            'current_country': config.NEWS_COUNTRY,
            'last_update': datetime.now().isoformat()
        }

    def format_for_display(self, headline: Dict = None) -> str:
        """Format headline for display"""
        if headline is None:
            if not self.headlines:
                return "No headlines available"
            headline = self.headlines[0]
        
        title = headline.get('title', 'No title')
        source = headline.get('source', 'Unknown')
        
        # Truncate for display
        if len(title) > 80:
            title = title[:77] + "..."
        
        return f"📰 {title}\n    - {source}"

    def get_detailed_article(self, index: int) -> Dict:
        """Get detailed article information"""
        if 0 <= index < len(self.headlines):
            return self.headlines[index]
        return {}

    def export_headlines(self, format: str = 'json') -> str:
        """Export headlines in different formats"""
        if format == 'json':
            import json
            return json.dumps(self.headlines, indent=2)
        elif format == 'csv':
            import csv
            import io
            
            output = io.StringIO()
            if self.headlines:
                writer = csv.DictWriter(output, fieldnames=self.headlines[0].keys())
                writer.writeheader()
                writer.writerows(self.headlines)
            
            return output.getvalue()
        elif format == 'text':
            result = []
            for i, h in enumerate(self.headlines, 1):
                result.append(f"{i}. {h.get('title', 'No title')}")
                result.append(f"   Source: {h.get('source', 'Unknown')}")
                result.append(f"   Link: {h.get('url', 'N/A')}")
                result.append("")
            return "\n".join(result)
        
        return ""
