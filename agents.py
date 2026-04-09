import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def _run_agent(role_name: str, system_prompt: str, task_prompt: str) -> str:
    logger.info(f"🤖 Running agent: {role_name}")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": task_prompt,
            },
        ],
        temperature=0.7,
    )

    content = response.choices[0].message.content
    logger.info(f"✅ Agent {role_name} finished.")
    return content


def generate_content() -> str:
    return _run_agent(
        role_name="📝 Content Creator",
        system_prompt=(
            "You are a multi-platform content creator. "
            "You write short-form content that can be used on Twitter, LinkedIn, and Instagram."
        ),
        task_prompt=(
            "Generate 5 high-signal content ideas with captions and hooks for my online business. "
            "Focus on value, clarity, and shareability."
        ),
    )


def generate_product() -> str:
    return _run_agent(
        role_name="🔍 Trend Researcher",
        system_prompt=(
            "You are a product ideation specialist who turns trends into digital products."
        ),
        task_prompt=(
            "Propose 3 concrete digital product ideas (templates, guides, mini-courses) "
            "that align with the content themes above. Include title, promise, and outline."
        ),
    )


def optimize_funnel() -> str:
    return _run_agent(
        role_name="🚀 Growth Hacker",
        system_prompt=(
            "You are a growth and funnel optimization specialist."
        ),
        task_prompt=(
            "Given that I am creating content and digital products, outline a simple funnel: "
            "top-of-funnel content, lead magnet, core offer, and follow-up sequence. "
            "Make it lean and realistic for a solo operator."
        ),
    )


def generate_strategy_review() -> str:
    return _run_agent(
        role_name="📑 Executive Summary Generator",
        system_prompt=(
            "You create concise strategic summaries for founders."
        ),
        task_prompt=(
            "Write a one-page strategy review summarizing: content direction, product focus, "
            "funnel priorities, and next 3 most important actions."
        ),
    )


def pull_analytics() -> str:
    return _run_agent(
        role_name="📊 Analytics Reporter",
        system_prompt=(
            "You are an analytics strategist. You infer insights from qualitative signals."
        ),
        task_prompt=(
            "Without real data, simulate a weekly analytics snapshot: what content is likely performing, "
            "what offers are resonating, and what experiments should be run next."
        ),
    )
