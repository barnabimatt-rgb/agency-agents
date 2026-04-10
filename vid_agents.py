from openai import OpenAI
import os
import subprocess
import base64
import requests

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================
# SIMPLE VIDEO AGENT
# ============================================================

class SimpleVideoAgent:
    def __init__(self):
        self.client = client

    def generate_script(self, topic):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Write a short, punchy 45-second script."},
                {"role": "user", "content": f"Topic: {topic}"}
            ]
        )
        return response.choices[0].message.content

    def generate_image(self, prompt, filename="output/image.png"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        result = self.client.images.generate(
            model="gpt-image-1.5",
            prompt=prompt
        )

        # Extract base64 image data
        image_base64 = result.data[0].b64_json

        # Decode and save
        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_base64))

        return filename

    def generate_voice(self, script, filename="output/audio.mp3"):
        audio = self.client.audio.speech.create(
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
        return self.simple.run(topic)
