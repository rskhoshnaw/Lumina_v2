"""Main execution pipeline for Lumina Studio."""
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, Optional

from core.gemini_provider import GeminiProvider
from core.content_planner import ContentPlanner
from core.code_generator import CodeGenerator
from core.code_repair import CodeRepairer
from core.validator import validate_code
from core.renderer import ManimRenderer

class LuminaPipeline:
    def __init__(self, api_key: Optional[str] = None, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path.cwd()
        self.media_dir = self.base_dir / "media"
        
        self.provider = GeminiProvider(api_key=api_key)
        
        self.planner = ContentPlanner(self.provider, self.base_dir / "prompts" / "planner.txt")
        self.generator = CodeGenerator(self.provider, self.base_dir / "prompts" / "code_generator.txt")
        self.repairer = CodeRepairer(self.provider, self.base_dir / "prompts" / "code_repair.txt")
        self.renderer = ManimRenderer(base_dir=self.base_dir, media_dir=self.media_dir)

    def run(
        self,
        prompt: str,
        category: str,
        language: str,
        audience: str,
        style: str,
        duration_seconds: int,
        quality: str = "qm",
        output_dir: str = "generated",
        max_retries: int = 2
    ) -> Dict[str, Any]:
        
        out_path = self.base_dir / output_dir
        out_path.mkdir(parents=True, exist_ok=True)
        
        # 1. Plan Content
        settings = {
            "category": category, "language": language, "audience": audience,
            "style": style, "duration_seconds": duration_seconds
        }
        blueprint = self.planner.create_blueprint(user_request=prompt, settings=settings)
        
        # 2. Initial Code Generation
        code = self.generator.generate(blueprint)
        
        # 3. Validation & Render Loop (The Repair Loop)
        for attempt in range(max_retries + 1):
            is_valid, errors = validate_code(code)
            error_log = ""
            
            if not is_valid:
                error_log = "VALIDATION ERRORS:\n" + "\n".join(errors)
            else:
                scene_file = out_path / "auto_scene.py"
                scene_file.write_text(code, encoding="utf-8")
                
                try:
                    self.renderer.render(python_file=scene_file, quality_flag=f"-{quality}")
                    
                    video_path = self.renderer.find_video(scene_file.stem)
                    if not video_path:
                        raise FileNotFoundError("Render finished but MP4 was not found.")
                        
                    # اگر رندر موفق بود، مستقیماً خروجی را برمی‌گردانیم
                    return {
                        "blueprint": blueprint,
                        "code_file": str(scene_file),
                        "video_file": str(video_path),
                        "retries_used": attempt
                    }
                except Exception as e:
                    error_log = f"RUNTIME ERROR (Manim Failed):\n{str(e)}"
            
            # اگر به اینجا رسیدیم یعنی خطایی در ولیدیشن یا رندر رخ داده است
            if attempt < max_retries:
                print(f"[Repair Loop] Error detected. Attempting repair {attempt + 1}/{max_retries}...")
                code = self.repairer.repair(blueprint, bad_code=code, error_log=error_log)
            else:
                # اگر تلاش‌ها تمام شد، متوقف می‌شویم
                raise RuntimeError(f"Pipeline failed after {max_retries} repair attempts.\nFinal Error:\n{error_log}")
