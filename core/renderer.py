import subprocess
import sys
from pathlib import Path
from typing import Optional


class ManimRenderer:
    def __init__(
        self,
        base_dir: Path,
        media_dir: Path,
    ):
        self.base_dir = base_dir
        self.media_dir = media_dir

    def render(
        self,
        python_file: Path,
        quality_flag: str,
    ):
        if quality_flag not in {"-ql", "-qm", "-qh"}:
            raise ValueError("کیفیت Manim معتبر نیست.")

        quality = quality_flag.removeprefix("-q")
        render_settings = {
            "l": ("854,480", "15"),
            "m": ("1280,720", "30"),
            "h": ("1920,1080", "60"),
        }
        resolution, frame_rate = render_settings[quality]
        command = [
            sys.executable,
            "-m",
            "manim",
            "--quality",
            quality,
            "--resolution",
            resolution,
            "--fps",
            frame_rate,
            str(python_file),
            "GeneratedVideo",
        ]

        result = subprocess.run(
            command,
            cwd=str(self.base_dir),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        
        # مهم: اگر Manim خطا داد، مستقیماً آن را پرتاب می‌کنیم تا در UI نمایش داده شود
        if result.returncode != 0:
            raise RuntimeError(f"Manim Rendering Failed:\n{result.stderr}")
            
        return result

    def find_video(self, scene_file_stem: Optional[str] = None) -> Optional[Path]:

        if not self.media_dir.exists():
            return None

        search_dir = self.media_dir / "videos"
        if scene_file_stem:
            search_dir = search_dir / scene_file_stem

        candidates = list(search_dir.rglob("GeneratedVideo.mp4"))

        if not candidates:
            return None

        candidates.sort(
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        return candidates[0]
