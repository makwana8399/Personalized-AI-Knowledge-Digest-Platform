from app.ai.openrouter_client import OpenRouterClient
from app.config.logging import logger
import json
import re
import time
from typing import List


class Processor:
    """
    Responsible ONLY for AI work.
    - Per-article summarization
    - Digest overview generation
    """

    def __init__(self):
        self.client = OpenRouterClient()
        self.retry_count = 3
        self.retry_delay = 2

    # --------------------------------------------------
    # ARTICLE LEVEL SUMMARIZATION (RUN ONCE PER ARTICLE)
    # --------------------------------------------------
    def summarize_article(self, raw_text: str) -> dict:
        system_prompt = (
            "You are a senior technology newsletter editor. "
            "You write extremely concise summaries for email digests. "
            "ALWAYS return valid JSON format with exactly these keys: summary, takeaways, topic."
        )

        limited_text = raw_text[:3000] + "..." if len(raw_text) > 3000 else raw_text

        # 🔥 MINIMAL FIX: OpenRouter disabled → direct fallback
        if not getattr(self.client, "api_key", None):
            logger.info("⚠️ OpenRouter disabled. Using fallback summary.")
            return self._create_fallback_summary(limited_text)

        user_prompt = f"""
ARTICLE CONTENT:
{limited_text}

TASK:
Return STRICT JSON with:
- summary: ONE or TWO sentences, max 40 words total
- takeaways: list of EXACTLY 3 very short bullet points (5–7 words each)
- topic: ONE lowercase word (ai, llm, mlops, startup, cloud, security, devtools, web, mobile, data)
"""

        for attempt in range(self.retry_count):
            try:
                logger.info(f"Summarizing article (attempt {attempt + 1}/{self.retry_count})")

                response = self.client.chat(system_prompt, user_prompt)

                if not response:
                    raise ValueError("Empty response from AI")

                parsed = self._safe_parse(response)

                if parsed["summary"] and len(parsed["takeaways"]) == 3:
                    logger.info("Article summarized successfully")
                    return parsed

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay)

        logger.error("All summarization attempts failed, using fallback")
        return self._create_fallback_summary(limited_text)

    # --------------------------------------------------
    # BACKWARD COMPATIBILITY (CRITICAL)
    # --------------------------------------------------
    def process_article(self, raw_text: str) -> dict:
        return self.summarize_article(raw_text)

    # --------------------------------------------------
    # DIGEST OVERVIEW (PER USER)
    # --------------------------------------------------
    def generate_overview(self, articles, interests: List[str]) -> str:
        if not articles:
            return "No articles selected for today's digest."

        # 🔥 MINIMAL FIX: skip LLM if disabled
        if not getattr(self.client, "api_key", None):
            return f"Good morning! Today's digest features {len(articles)} curated articles on technology."

        titles = "\n".join(f"- {a.title[:100]}" for a in articles[:10])

        prompt = f"""
User interests: {", ".join(interests)}

Articles selected:
{titles}

Write a short professional daily digest overview (3–4 lines).
Start with: "Good morning! Today's digest features..."
"""

        try:
            logger.info("Generating digest overview")
            overview = self.client.chat(
                "You are a professional tech newsletter editor.",
                prompt,
                max_tokens=150,
            )
            return overview.strip()

        except Exception as e:
            logger.warning(f"Overview generation failed: {e}")
            return f"Good morning! Today's digest features {len(articles)} curated articles."

    # --------------------------------------------------
    # SAFE JSON PARSER
    # --------------------------------------------------
    def _safe_parse(self, text: str) -> dict:
        cleaned = re.sub(r"```json|```|\n", "", text).strip()
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(0)

        try:
            data = json.loads(cleaned)

            takeaways = data.get("takeaways", [])
            if not isinstance(takeaways, list):
                takeaways = []

            while len(takeaways) < 3:
                takeaways.append("Important insight from the article")

            return {
                "summary": data.get("summary", "Key insights from today's article."),
                "takeaways": takeaways[:3],
                "topic": str(data.get("topic", "general")).lower(),
            }

        except Exception:
            return self._create_fallback_summary(text)

    # --------------------------------------------------
    # FALLBACK SUMMARY
    # --------------------------------------------------
    def _create_fallback_summary(self, text: str) -> dict:
        first_sentence = re.split(r"[.!?]", text)[0][:150]

        return {
            "summary": first_sentence or "Key insights from today's article.",
            "takeaways": [
                "Important development highlighted",
                "Key implications discussed",
                "Future trends indicated",
            ],
            "topic": "general",
        }
