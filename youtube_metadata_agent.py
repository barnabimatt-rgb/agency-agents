import os
import base64
from io import BytesIO
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_youtube_metadata(topic):
    prompt = f"""
    You are creating metadata for a YouTube video.

    Topic: {topic}

    1) Generate a high-retention YouTube title (5–10 words, curiosity-based).
    2) Generate a 2–3 sentence description, keyword-rich, with a clear CTA.
    3) Generate 5–10 SEO-friendly tags as a comma-separated list.

    Respond in this exact format:

    Title: ...
    Description: ...
    Tags: tag1, tag2, tag3, ...
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    title = ""
    description_lines = []
    tags_line = ""

    for line in lines:
        if line.lower().startswith("title:"):
            title = line.split(":", 1)[1].strip()
        elif line.lower().startswith("description:"):
            description_lines.append(line.split(":", 1)[1].strip())
        elif line.lower().startswith("tags:"):
            tags_line = line.split(":", 1)[1].strip()
        else:
            if description_lines and not tags_line:
                description_lines.append(line.strip())

    description = " ".join(description_lines).strip()
    tags = [t.strip() for t in tags_line.split(",") if t.strip()]

    return title, description, tags


def generate_thumbnail_base(topic):
    prompt = f"""
    Create a YouTube thumbnail image for a video about:
    {topic}

    Requirements:
    - Bold, high contrast
    - Strong visual hook
    - Minimal clutter
    """

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1280x720"
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    return image_bytes


def overlay_text_on_thumbnail(image_bytes, text, output_path="thumbnail.png"):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    draw = ImageDraw.Draw(image)

    width, height = image.size

    max_chars = 28
    words = text.split()
    lines = []
    current = []
    for w in words:
        current.append(w)
        if len(" ".join(current)) > max_chars:
            current.pop()
            lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))

    font_size = 80
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    line_height = font_size + 10
    total_text_height = line_height * len(lines)

    y = height - total_text_height - 60

    margin = 40
    for line in lines:
        text_width, _ = draw.textsize(line, font=font)
        x = margin
        draw.rectangle(
            [x - 20, y - 10, x + text_width + 20, y + line_height],
            fill=(0, 0, 0, 180)
        )
        draw.text((x, y), line, font=font, fill=(255, 255, 255))
        y += line_height

    image.save(output_path)
    return output_path


def generate_thumbnail(topic, title_for_text=None, output_path="thumbnail.png"):
    image_bytes = generate_thumbnail_base(topic)
    text = title_for_text or topic
    final_path = overlay_text_on_thumbnail(image_bytes, text, output_path=output_path)
    return final_path
