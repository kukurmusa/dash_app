from __future__ import annotations

import os

from ai_summary_config import AI_SUMMARY_CONFIG


def _dummy_summary(page_key: str) -> str:
    config = AI_SUMMARY_CONFIG.get(page_key, {})
    return config.get("dummy_summary", "No summary config found for this page.")


def get_ai_summary(page_key: str) -> str:
    config = AI_SUMMARY_CONFIG.get(page_key)
    if not config:
        return "No summary config found for this page."

    system_prompt = config["system_prompt"]
    user_prompt = config["user_prompt"].format(page_content=config.get("page_content", ""))

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _dummy_summary(page_key)

    try:
        from openai import OpenAI
    except Exception:
        return _dummy_summary(page_key)

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini"),
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        summary = getattr(response, "output_text", None)
        return summary.strip() if summary else _dummy_summary(page_key)
    except Exception:
        return _dummy_summary(page_key)
