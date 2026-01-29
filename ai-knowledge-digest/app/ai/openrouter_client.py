# app/ai/openrouter_client.py
import requests
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class OpenRouterClient:
    """
    OpenRouter API client with chat method for Processor class
    """
    
    def __init__(self):
        from app.config.settings import (
            OPENROUTER_API_KEY,
            OPENROUTER_MODEL,
            OPENROUTER_API_URL
        )
        
        self.api_key = OPENROUTER_API_KEY
        self.model = OPENROUTER_MODEL
        self.base_url = OPENROUTER_API_URL
        
        if not self.api_key or self.api_key == "":
            logger.warning("OPENROUTER_API_KEY is not set. AI features will not work.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI Knowledge Digest Platform"
        }
    
    def chat(self, system_prompt: str, user_prompt: str, max_tokens: int = 500) -> str:
        """
        Chat completion method for Processor class
        Returns: JSON string or text response
        """
        # If no API key, return fallback response
        if not self.api_key or self.api_key == "":
            logger.warning("No API key, returning fallback response")
            return self._fallback_response(user_prompt)
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.3,
                "response_format": {"type": "json_object"}  # Force JSON response
            }
            
            logger.info(f"Sending request to OpenRouter (model: {self.model})")
            
            response = requests.post(
                self.base_url,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                logger.info("OpenRouter response received")
                return content
                
            elif response.status_code == 401:
                error_data = response.json()
                logger.error(f"Authentication failed: {error_data}")
                logger.error("Please check your OPENROUTER_API_KEY in .env file")
                return self._fallback_response(user_prompt)
                
            else:
                logger.error(f"OpenRouter error {response.status_code}: {response.text}")
                return self._fallback_response(user_prompt)
                
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            return self._fallback_response(user_prompt)
            
        except Exception as e:
            logger.error(f"Error in chat request: {str(e)}")
            return self._fallback_response(user_prompt)
    
    def _fallback_response(self, user_prompt: str) -> str:
        """Generate fallback response when API fails"""
        # Extract article content from prompt
        import re
        
        # Try to find article content
        article_match = re.search(r'ARTICLE CONTENT:(.*?)(?=TASK:|$)', user_prompt, re.DOTALL)
        article_content = article_match.group(1).strip() if article_match else ""
        
        # Simple fallback summary
        sentences = article_content.split('.')[:2]
        summary = ". ".join([s.strip() for s in sentences if s.strip()]) + "."
        
        # Create fallback JSON
        fallback_json = {
            "summary": summary[:100] if summary else "Article summary not available.",
            "takeaways": [
                "Key point 1 from article",
                "Key point 2 from article", 
                "Key point 3 from article"
            ],
            "topic": "general"
        }
        
        return json.dumps(fallback_json)
    
    def summarize(self, text: str) -> str:
        """Simple summarization method (alternative to chat)"""
        return self.chat(
            "You are a helpful assistant that summarizes text concisely.",
            f"Summarize this in 2-3 sentences:\n\n{text[:2000]}",
            max_tokens=180
        )