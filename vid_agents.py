import os
import subprocess
import base64
import requests
from openai import OpenAI

# New imports for upgraded HybridAgent
from script_parser import ScriptParser
from media_resolver import MediaResolver
from video_assembler import VideoAssembler


# ============================================================
# OPENAI CLIENT
# ============================================================

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================
# SIMPLE VIDEO AGENT (your original)
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

        image_base64 = result.data[0].b64_json

        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_base64))

        return filename

    def generate_voice(self, script, filename="output/audio.mp3"):
        response = self.client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=script
        )

        os.makedirs("output", exist_ok=True)

        with open(filename, "wb") as f:
            f.write(response.read())

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
# MID-TIER VIDEO AGENT (still a placeholder)
# ============================================================

class MidTierVideoAgent:
    def run(self, topic):
        simple = SimpleVideoAgent()
        return simple.run(topic)


# ============================================================
# NEW HYBRID AGENT (full upgrade)
# ============================================================

class HybridAgent:
    """
    Upgraded HybridAgent:
    - Generates script/title/description
    - Parses cues (ScriptParser)
    - Resolves B-roll (MediaResolver)
    - Assembles full video (VideoAssembler)
    - Falls back to SimpleVideoAgent if needed
    """

    def __init__(self):
        self.client = client
        self.simple = SimpleVideoAgent()
        self.mid = MidTierVideoAgent()

        # New components
        self.script_parser = ScriptParser()
        self.media_resolver = MediaResolver()
        self.video_assembler = VideoAssembler()

    def _generate_script_title_description(self, topic):
        prompt = f"""
        You are writing a short-form video script for a hybrid athlete, tactical, AI-automation creator.

        Topic: "{topic}"

        1) Write a 30–45 second script that:
           - Uses bracketed cues for B-roll, music, SFX, and on-screen text.
           - Is punchy, direct, and practical.
           - Speaks from the perspective of someone who actually trains and builds systems.

           Use cues like:
           - [INTRO: Energetic music begins]
           - [ON-SCREEN TEXT: ...]
           - [B-ROLL: ...]
           - [SFX: ...]
           - [MUSIC: ...]
           - [CUT TO: ...]

        2) Then on a new line, write:
           TITLE: <compelling title, 5–10 words>

        3) Then on a new line, write:
           DESCRIPTION
