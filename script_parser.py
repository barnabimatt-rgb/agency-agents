import re
from typing import List, Dict, Any


class ScriptParser:
    """
    Parses a script with bracketed cues into a structured timeline.

    Example input:

    [INTRO: Energetic music begins]
    [ON-SCREEN TEXT: Build discipline daily]
    You think discipline is about motivation. It's not.
    [B-ROLL: athlete running in the rain]
    [SFX: whoosh transition]
    [MUSIC: switch to darker tone]

    Output: list of actions, e.g.
    [
        {"type": "music", "mode": "intro", "description": "Energetic music begins"},
        {"type": "text", "content": "Build discipline daily"},
        {"type": "narration", "content": "You think discipline is about motivation. It's not."},
        {"type": "broll", "description": "athlete running in the rain"},
        {"type": "sfx", "description": "whoosh transition"},
        {"type": "music", "mode": "change", "description": "switch to darker tone"},
    ]
    """

    CUE_PATTERN = re.compile(r"^\s*

\[(.+?):\s*(.+?)\]

\s*$")

    def parse(self, script: str) -> List[Dict[str, Any]]:
        lines = script.split("\n")
        actions: List[Dict[str, Any]] = []

        buffer_narration: List[str] = []

        def flush_narration():
            nonlocal buffer_narration
            if buffer_narration:
                text = " ".join(line.strip() for line in buffer_narration if line.strip())
                if text:
                    actions.append({
                        "type": "narration",
                        "content": text,
                    })
                buffer_narration = []

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue

            match = self.CUE_PATTERN.match(line)
            if match:
                # We hit a cue; flush any narration first
                flush_narration()

                tag = match.group(1).strip().upper()
                content = match.group(2).strip()

                if tag.startswith("INTRO"):
                    actions.append({
                        "type": "music",
                        "mode": "intro",
                        "description": content,
                    })
                elif tag.startswith("MUSIC"):
                    actions.append({
                        "type": "music",
                        "mode": "change",
                        "description": content,
                    })
                elif tag.startswith("B-ROLL") or tag.startswith("BROLL"):
                    actions.append({
                        "type": "broll",
                        "description": content,
                    })
                elif tag.startswith("ON-SCREEN TEXT") or tag.startswith("ON SCREEN TEXT") or tag.startswith("TEXT"):
                    actions.append({
                        "type": "text",
                        "content": content,
                    })
                elif tag.startswith("SFX") or tag.startswith("SOUND"):
                    actions.append({
                        "type": "sfx",
                        "description": content,
                    })
                elif tag.startswith("CUT TO") or tag.startswith("SCENE"):
                    actions.append({
                        "type": "cut",
                        "description": content,
                    })
                else:
                    # Unknown cue type, keep it as a generic action
                    actions.append({
                        "type": "cue",
                        "tag": tag,
                        "description": content,
                    })
            else:
                # Regular narration line
                buffer_narration.append(line)

        # Flush any remaining narration
        flush_narration()

        return actions
