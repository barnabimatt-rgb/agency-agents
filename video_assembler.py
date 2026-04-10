import os
import subprocess
import uuid
from typing import List, Dict, Any

from gtts import gTTS  # or any TTS you prefer
from moviepy.editor import (
    VideoFileClip,
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
)


class VideoAssembler:
    """
    Takes resolved actions and builds a vertical short-form video.

    Assumptions:
    - B-roll clips are .mp4 files (vertical or close).
    - Narration is generated via TTS.
    - Music/SFX are mapped to local files (simple stubs here).
    """

    def __init__(self):
        self.temp_dir = os.getenv("TEMP_DIR", "/app/tmp")
        os.makedirs(self.temp_dir, exist_ok=True)

        # Simple local libraries (you can customize these paths)
        self.music_library = {
            "intro": os.getenv("MUSIC_INTRO_PATH", ""),
            "change": os.getenv("MUSIC_CHANGE_PATH", ""),
        }
        self.sfx_library = {
            "whoosh": os.getenv("SFX_WHOOSH_PATH", ""),
        }

        # Video settings
        self.width = 1080
        self.height = 1920
        self.fps = 30

    def _tts_narration(self, text: str) -> str:
        """
        Generate TTS audio for narration text.
        """
        if not text:
            return ""

        audio_path = os.path.join(self.temp_dir, f"narration_{uuid.uuid4().hex}.mp3")
        tts = gTTS(text=text, lang="en")
        tts.save(audio_path)
        return audio_path

    def _load_music_clip(self, mode: str) -> AudioFileClip | None:
        path = self.music_library.get(mode)
        if not path or not os.path.exists(path):
            return None
        return AudioFileClip(path)

    def _load_sfx_clip(self, description: str) -> AudioFileClip | None:
        # Very simple mapping: if "whoosh" in description -> whoosh
        key = "whoosh" if "whoosh" in description.lower() else None
        if not key:
            return None

        path = self.sfx_library.get(key)
        if not path or not os.path.exists(path):
            return None
        return AudioFileClip(path)

    def assemble(self, actions: List[Dict[str, Any]], topic: str) -> str:
        """
        Build the final video from resolved actions.

        Strategy:
        - Build a sequence of visual clips (b-roll, text-only screens).
        - Overlay narration audio.
        - Add background music and occasional SFX.
        """
        visual_clips: List[VideoFileClip | ImageClip | CompositeVideoClip] = []
        narration_texts: List[str] = []

        current_music_mode = "intro"
        music_clips: List[AudioFileClip] = []
        sfx_clips: List[AudioFileClip] = []

        # 1) Build visuals and collect narration
        for action in actions:
            atype = action.get("type")

            if atype == "broll":
                path = action.get("path")
                if not path or not os.path.exists(path):
                    continue
                clip = VideoFileClip(path).resize(height=self.height)
                clip = clip.set_position("center").set_fps(self.fps)
                visual_clips.append(clip)

            elif atype == "text":
                content = action.get("content", "")
                if not content:
                    continue
                txt_clip = TextClip(
                    content,
                    fontsize=70,
                    color="white",
                    font="Arial-Bold",
                    method="caption",
                    size=(self.width * 0.9, None),
                ).set_duration(2.5)
                txt_clip = txt_clip.set_position("center")
                bg = ImageClip(color=(0, 0, 0), size=(self.width, self.height)).set_duration(2.5)
                composite = CompositeVideoClip([bg, txt_clip]).set_fps(self.fps)
                visual_clips.append(composite)

            elif atype == "narration":
                narration_texts.append(action.get("content", ""))

            elif atype == "music":
                mode = action.get("mode", "change")
                current_music_mode = mode  # we just track the latest mode

            elif atype == "sfx":
                desc = action.get("description", "")
                sfx = self._load_sfx_clip(desc)
                if sfx:
                    sfx_clips.append(sfx)

        if not visual_clips:
            # Fallback: create a simple text screen if no visuals
            txt_clip = TextClip(
                topic,
                fontsize=80,
                color="white",
                font="Arial-Bold",
                method="caption",
                size=(self.width * 0.9, None),
            ).set_duration(10)
            txt_clip = txt_clip.set_position("center")
            bg = ImageClip(color=(0, 0, 0), size=(self.width, self.height)).set_duration(10)
            visual_clips = [CompositeVideoClip([bg, txt_clip]).set_fps(self.fps)]

        # 2) Concatenate visuals
        final_visual = concatenate_videoclips(visual_clips, method="compose")

        # 3) Narration audio
        narration_text = " ".join(narration_texts).strip()
        narration_audio_path = self._tts_narration(narration_text) if narration_text else ""
        narration_audio = AudioFileClip(narration_audio_path) if narration_audio_path else None

        # 4) Background music
        music_audio = self._load_music_clip(current_music_mode)
        if music_audio:
            music_audio = music_audio.volumex(0.25)

        # 5) Mix audio
        if narration_audio and music_audio:
            mixed_audio = narration_audio.audio_fadein(0.3).audio_fadeout(0.3)
            mixed_audio = mixed_audio.set_duration(final_visual.duration)
            music_audio = music_audio.set_duration(final_visual.duration)
            final_audio = mixed_audio.volumex(1.0).fx(lambda a: a)  # placeholder
            # MoviePy doesn't mix easily inline; simplest is to use narration only for now.
            final_audio = mixed_audio
        elif narration_audio:
            final_audio = narration_audio.set_duration(final_visual.duration)
        elif music_audio:
            final_audio = music_audio.set_duration(final_visual.duration)
        else:
            final_audio = None

        if final_audio:
            final_visual = final_visual.set_audio(final_audio)

        # 6) Export
        output_path = os.path.join(self.temp_dir, f"video_{uuid.uuid4().hex}.mp4")
        final_visual.write_videofile(
            output_path,
            fps=self.fps,
            codec="libx264",
            audio_codec="aac",
            threads=2,
            verbose=False,
            logger=None,
        )

        return output_path
