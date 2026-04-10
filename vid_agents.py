from openai import OpenAI
import os
import subprocess
import requests

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================
# SIMPLE VIDEO AGENT
# ============================================================

class SimpleVideoAgent:
    def generate_script(self, topic):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Write a short, punchy 45-second script."},
                {"role": "user", "content": f"Topic: {topic}"}
            ]
        )
        return response.choices[0].message.content

def generate_image(self, prompt, filename="output/image.jpg"):
    # Step 1: Convert topic into a visual description
    visual_prompt = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Convert the topic into a concrete visual scene for an illustration."},
            {"role": "user", "content": f"Topic: {prompt}"}
        ]
    ).choices[0].message.content

    # Step 2: Generate the image
    img = client.images.generate(
        model="gpt-image-1",
        prompt=visual_prompt,
        size="1024x1024"
    )

    # Step 3: Validate response
    if not img or not img.data or not img.data[0].url:
        raise ValueError("OpenAI returned no image URL")

    img_url = img.data[0].url
    img_bytes = requests.get(img_url).content

    os.makedirs("output", exist_ok=True)
    with open(filename, "wb") as f:
        f.write(img_bytes)

    return filename


    def generate_voice(self, script, filename="output/audio.mp3"):
        audio = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=script
        )

        os.makedirs("output", exist_ok=True)
        with open(filename, "wb") as f:
            f.write(audio)

        return filename

    def assemble_video(self, image_path, audio_path, output="output/video.mp4"):
        os.makedirs("output", exist_ok=True)

        cmd = [
            "ffmpeg",
            "-loop", "1",
            "-i", image_path,
            "-i", audio_path,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            output
        ]

        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output

    def run(self, topic):
        script = self.generate_script(topic)
        img = self.generate_image(topic)
        audio = self.generate_voice(script)
        video = self.assemble_video(img, audio)
        return video, script



# ============================================================
# MID-TIER VIDEO AGENT (placeholder for now)
# ============================================================

class MidTierVideoAgent:
    def run(self, topic):
        # Placeholder — currently falls back to SimpleVideoAgent
        simple = SimpleVideoAgent()
        return simple.run(topic)


# ============================================================
# HYBRID AGENT (fallback mode)
# ============================================================

class HybridAgent:
    def __init__(self):
        self.simple = SimpleVideoAgent()
        self.mid = MidTierVideoAgent()

    def run(self, topic):
        # For now, always use SimpleVideoAgent
        return self.simple.run(topic)
