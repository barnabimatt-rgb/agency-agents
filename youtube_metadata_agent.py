import os
import base64
import requests
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------------------------------------------------------
# 1. Generate Title + Description
# ---------------------------------------------------------
def generate_youtube_metadata(topic):
    prompt = f"""
    Create a YouTube title and description for a short-form video.
    Topic: {topic}

    Requirements:
    - Title: 5–10 words, high retention, curiosity-based
    - Description: 2–3 sentences, keyword-rich, no fluff
    - Include a CTA in the description
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content

    # Simple parsing
    lines = text.split("\n")
    title = lines[0].replace("Title:", "").strip()
    description = "\n".join(lines[1:]).replace("Description:", "").strip()

    return title, description


# ---------------------------------------------------------
# 2. Generate Thumbnail Image
# ---------------------------------------------------------
def generate_thumbnail(topic, output_path="thumbnail.png"):
    prompt = f"""
    Create a YouTube thumbnail image for a video about:
    {topic}

    Requirements:
    - Bold, high contrast
    - No faces
    - Minimal text
    - Strong visual hook
    """

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1280x720"
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    return output_path
