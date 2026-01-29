
# Canonical topics used across the system
CANONICAL_TOPICS = {
    "ai": ["ai", "llm", "llms", "machine learning", "deep learning"],
    "mlops": ["mlops", "devops", "deployment", "pipelines"],
    "startup": ["startup", "startups", "founder", "entrepreneurship"],
    "vc": ["vc", "venture capital", "investment", "funding"],
    "product": ["product", "pm", "product management", "ux"],
    "cloud": ["cloud", "aws", "gcp", "azure"],
}


def normalize_interest(interest: str) -> str | None:
    """
    Convert user interest into a canonical topic.
    """
    interest = interest.lower().strip()

    for canonical, aliases in CANONICAL_TOPICS.items():
        if interest == canonical or interest in aliases:
            return canonical

    return None