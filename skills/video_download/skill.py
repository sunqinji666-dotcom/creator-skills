#!/usr/bin/env python3
"""
视频下载技能
使用 yt-dlp 下载各种网站的视频
支持：B站（带 Cookie 下载充电视频）、YouTube（带代理）、Twitter、Instagram、TikTok 等 1000+ 网站
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# 配置
DEFAULT_PROXY = "http://127.0.0.1:10809"
DEFAULT_COOKIE_FILE = os.environ.get("VIDEO_DOWNLOAD_COOKIE_FILE", "")


class VideoDownloadSkill:
    def __init__(self):
        self.name = "video_download"
        self.description = "视频下载工具，支持 B 站、YouTube 等 1000+ 网站"

    def download(self, url, output_dir=None, proxy=None, cookies_file=None, quality="best"):
        """
        下载视频
        url: 视频 URL
        output_dir: 输出目录，默认当前目录
        proxy: 代理地址，默认使用配置的 10809 端口
        cookies_file: Cookie 文件，B站需要
        quality: 视频质量，默认 best
        """
        cmd = ["yt-dlp"]

        # 添加代理
        if proxy is True:
            cmd.extend(["--proxy", DEFAULT_PROXY])
        elif proxy:
            cmd.extend(["--proxy", proxy])

        # 添加 Cookie
        if cookies_file is True:
            if Path(DEFAULT_COOKIE_FILE).exists():
                cmd.extend(["--cookies", DEFAULT_COOKIE_FILE])
            else:
                print(f"⚠️ Cookie 文件不存在: {DEFAULT_COOKIE_FILE}")
        elif cookies_file:
            if Path(cookies_file).exists():
                cmd.extend(["--cookies", cookies_file])
            else:
                print(f"⚠️ Cookie 文件不存在: {cookies_file}")

        # 设置质量
        cmd.extend(["-f", quality])

        # 设置输出目录
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            cmd.extend(["-o", str(output_path / "%(title)s.%(ext)s")])

        # 添加 URL
        cmd.append(url)

        print(f"▶️ 执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd)
        return result.returncode == 0

    def info(self, url):
        """查看视频信息"""
        cmd = ["yt-dlp", "-F", url]
        print(f"▶️ 查看格式: {' '.join(cmd)}")
        result = subprocess.run(cmd)
        return result.returncode == 0

    def run_cli(self):
        """命令行入口"""
        parser = argparse.ArgumentParser(description="视频下载技能")
        parser.add_argument("url", help="视频 URL")
        parser.add_argument("--output-dir", "-o", help="输出目录")
        parser.add_argument("--proxy", "-p", action="store_true", help="使用代理")
        parser.add_argument("--cookies", "-c", action="store_true", help="使用 Bilibili Cookie")
        parser.add_argument("--quality", "-q", default="best", help="视频质量")
        parser.add_argument("--info", "-i", action="store_true", help="仅查看格式信息")

        args = parser.parse_args()

        if args.info:
            return self.info(args.url)
        else:
            return self.download(
                args.url,
                output_dir=args.output_dir,
                proxy=args.proxy,
                cookies_file=args.cookies,
                quality=args.quality
            )


if __name__ == "__main__":
    skill = VideoDownloadSkill()
    sys.exit(0 if skill.run_cli() else 1)
