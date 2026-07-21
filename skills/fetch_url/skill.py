#!/usr/bin/env python3
"""
无头浏览器获取网页内容技能
支持:
- JS 渲染等待
- 手机端模拟（微信文章必备）
- 代理访问（访问外网）
- Cookie 登录（访问需要认证的页面）
- 截图保存
- 结果保存为 JSON
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# 配置
DEFAULT_PROXY = "http://127.0.0.1:10809"
FETCH_BIN = os.environ.get("FETCH_URL_BIN", "fetch-url")


class FetchUrlSkill:
    def __init__(self):
        self.name = "fetch_url"
        self.description = "无头浏览器获取网页内容，支持 JS 渲染"
        self.bin_path = FETCH_BIN

    def fetch(self, url, output=None, mobile=False, proxy=False, cookie=None,
              screenshot=None, wait=1000, timeout=30000):
        """获取网页内容"""
        if not Path(self.bin_path).exists():
            print(f"❌ 找不到 fetch-url 工具: {self.bin_path}")
            return False

        cmd = [self.bin_path, url]

        if mobile:
            cmd.append("--mobile")

        if proxy is True:
            cmd.extend(["--proxy", DEFAULT_PROXY])
        elif proxy:
            cmd.extend(["--proxy", proxy])

        if cookie:
            if Path(cookie).exists():
                cmd.extend(["--cookie", cookie])
            else:
                print(f"⚠️ Cookie 文件不存在: {cookie}")

        if screenshot:
            cmd.extend(["--screenshot", screenshot])

        if output:
            cmd.extend(["--output", output])

        cmd.extend(["--wait", str(wait)])
        cmd.extend(["--timeout", str(timeout)])

        print(f"▶️ 执行: {' '.join(cmd)}")
        result = subprocess.run(cmd)
        return result.returncode == 0

    def wechat_article(self, url, output=None, proxy=False):
        """获取微信公众号文章（快捷方式，自动启用手机模拟）"""
        return self.fetch(url, output=output, mobile=True, proxy=proxy)

    def youtube_page(self, url, output=None, use_proxy=True):
        """获取 YouTube 页面（快捷方式，自动启用代理）"""
        return self.fetch(url, output=output, mobile=False, proxy=use_proxy)

    def run_cli(self):
        """命令行入口"""
        parser = argparse.ArgumentParser(description="无头浏览器获取网页技能")
        parser.add_argument("url", help="目标 URL")
        parser.add_argument("--output", "-o", help="保存输出文件")
        parser.add_argument("--mobile", "-m", action="store_true", help="模拟手机端（微信文章必备）")
        parser.add_argument("--proxy", "-p", action="store_true", help="使用代理")
        parser.add_argument("--cookie", "-c", help="Cookie 文件路径")
        parser.add_argument("--screenshot", "-s", help="截图保存路径")
        parser.add_argument("--wait", "-w", type=int, default=1000, help="等待 JS 渲染毫秒数，默认 1000")
        parser.add_argument("--wechat", action="store_true", help="微信文章快捷模式")

        args = parser.parse_args()

        if args.wechat:
            args.mobile = True

        return self.fetch(
            args.url,
            output=args.output,
            mobile=args.mobile,
            proxy=args.proxy,
            cookie=args.cookie,
            screenshot=args.screenshot,
            wait=args.wait
        )


if __name__ == "__main__":
    skill = FetchUrlSkill()
    sys.exit(0 if skill.run_cli() else 1)
