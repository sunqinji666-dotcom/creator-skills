#!/usr/bin/env python3
"""
视频转录技能
使用 OpenAI Whisper 将视频语音转录为文字
支持批量并行转录，提高效率
"""

import os
import sys
import subprocess
import argparse
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


class VideoTranscriptionSkill:
    def __init__(self):
        self.name = "video_transcription"
        self.description = "视频语音转录文字，使用 OpenAI Whisper"

    def transcribe_single(self, video_path, model="base", language="zh", output_dir=None):
        """转录单个视频"""
        video_path = Path(video_path)

        if not video_path.exists():
            print(f"❌ 文件不存在: {video_path}")
            return False

        # 使用原视频目录作为输出目录
        if output_dir is None:
            output_dir = video_path.parent
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            "whisper",
            str(video_path),
            "--model", model,
            "--language", language,
            "--output_format", "txt",
            "--output_dir", str(output_dir)
        ]

        print(f"▶️ 开始转录: {video_path.name}")
        result = subprocess.run(cmd, capture_output=False)
        if result.returncode == 0:
            print(f"✅ 完成转录: {video_path.name}")
            return True
        else:
            print(f"❌ 转录失败: {video_path.name}")
            return False

    def transcribe_batch(self, video_paths, model="base", language="zh", output_dir=None, max_workers=4):
        """批量并行转录"""
        if isinstance(video_paths, (str, Path)):
            # 如果是目录，扫描所有视频文件
            video_dir = Path(video_paths)
            if video_dir.is_dir():
                video_paths = []
                for ext in ['*.mp4', '*.mov', '*.avi', '*.mkv', '*.webm', '*.flv']:
                    video_paths.extend(video_dir.glob(ext))
            else:
                video_paths = [video_dir]

        print(f"📋 准备批量转录 {len(video_paths)} 个视频，并行数: {max_workers}")

        success_count = 0
        failed_count = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    self.transcribe_single,
                    vp,
                    model=model,
                    language=language,
                    output_dir=output_dir
                ): vp for vp in video_paths
            }

            for future in as_completed(futures):
                vp = futures[future]
                try:
                    if future.result():
                        success_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    print(f"❌ 异常 {vp.name}: {e}")
                    failed_count += 1

        print(f"\n📊 批量转录完成: 成功 {success_count}, 失败 {failed_count}")
        return failed_count == 0

    def run_cli(self):
        """命令行入口"""
        parser = argparse.ArgumentParser(description="视频转录技能")
        parser.add_argument("input", help="视频文件或目录")
        parser.add_argument("--model", "-m", default="base", help="Whisper 模型 (tiny/base/small/medium/large)")
        parser.add_argument("--language", "-l", default="zh", help="语言代码，默认中文 (zh)")
        parser.add_argument("--output-dir", "-o", help="输出目录，默认原视频目录")
        parser.add_argument("--workers", "-w", type=int, default=4, help="并行转录数量，默认 4")

        args = parser.parse_args()

        input_path = Path(args.input)

        if input_path.is_file():
            success = self.transcribe_single(
                input_path,
                model=args.model,
                language=args.language,
                output_dir=args.output_dir
            )
        else:
            success = self.transcribe_batch(
                input_path,
                model=args.model,
                language=args.language,
                output_dir=args.output_dir,
                max_workers=args.workers
            )

        return success


if __name__ == "__main__":
    skill = VideoTranscriptionSkill()
    sys.exit(0 if skill.run_cli() else 1)
