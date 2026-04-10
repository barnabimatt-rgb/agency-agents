import openai
import os
import subprocess
from PIL import Image
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")

class SimpleVideoAgent:
    def generate_script(self, topic):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Write a short, punchy 45-second script."},
                {"role": "user", "content": f"Topic: {topic}"}
            ]
        )
        return response["choices"][0]["message"]["content"]

    def generate_image(self, prompt, filename="output/image.jpg"):
        img = openai.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )
        img_bytes = requests.get(img.data[0].url).content
        with open(filename, "wb") as f:
            f.write(img_bytes)
        return filename

    def generate_voice(self, script, filename="output/audio.mp3"):
        audio = openai.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=script
        )
        with open(filename, "wb") as f:
            f.write(audio)
        return filename

    def assemble_video(self, image_path, audio_path, output="output/video.mp4"):
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
        subprocess.run(cmd)
        return output

    def run(self, topic):
        script = self.generate_script(topic)
        img = self.generate_image(topic)
        audio = self.generate_voice(script)
        video = self.assemble_video(img, audio)
        return video, script

class MidTierVideoAgent:
    def run(self, topic):
        # Placeholder until full mid-tier pipeline is added
        # For now, fallback to simple agent
        return SimpleVideoAgent().run(topic)


class HybridAgent:
    def __init__(self):
        self.simple = SimpleVideoAgent()
        self.mid = MidTierVideoAgent()

    def run(self, topic):
        # Fallback mode: always simple for now
        return self.simple.run(topic)
