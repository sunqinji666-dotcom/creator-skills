#!/usr/bin/env python3
"""
文字校对技能
针对 Whisper 转录的文字进行校对:
- 纠正错别字
- 优化语句通顺度
- 分段整理
- 核实专有名词（配合搜索）
"""

import os
import sys
import argparse
from pathlib import Path


class TextProofreadingSkill:
    def __init__(self):
        self.name = "text_proofreading"
        self.description = "文字校对技能，纠正转录文字中的错别字，优化语句通顺度"

    def proofread_file(self, input_file, output_file=None, auto_format=True):
        """校对单个文件"""
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"❌ 文件不存在: {input_path}")
            return False

        # 默认输出: 原目录下添加 _校对 后缀
        if output_file is None:
            if input_file.endswith('.txt'):
                output_file = input_file.replace('.txt', '_校对.txt')
            else:
                output_file = str(input_path) + '_校对.txt'

        output_path = Path(output_file)

        # 读取原文
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"📄 加载文件: {input_path} ({len(content)} 字符)")
        print("\n" + "="*60)
        print(content[:500] + ("..." if len(content) > 500 else ""))
        print("="*60 + "\n")

        print(f"✏️  校对结果将保存到: {output_path}")
        print("\n校对原则:")
        print("  1. 纠正错别字和识别错误")
        print("  2. 调整不通顺的语句")
        print("  3. 核实专有名词（人名、地名、术语）")
        print("  4. 补充标点符号和合理分段")
        print()

        return True

    def batch_proofread(self, directory, pattern="*.txt"):
        """批量校对目录中的所有 txt 文件"""
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"❌ 目录不存在: {directory}")
            return False

        # 查找所有未校对的 txt 文件
        txt_files = []
        for txt_file in dir_path.rglob(pattern):
            # 跳过已经校对过的文件
            if not txt_file.name.endswith('_校对.txt'):
                # 检查是否已经存在校对版本
                proofread_path = txt_file.parent / (txt_file.stem + '_校对.txt')
                if not proofread_path.exists():
                    txt_files.append(txt_file)

        print(f"📂 找到 {len(txt_files)} 个待校对文件")

        for f in txt_files:
            print(f"  - {f}")

        print()
        return txt_files

    def save_proofread(self, content, output_file):
        """保存校对后的内容"""
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 已保存校对版本: {output_path}")
        return True

    def statistics(self, directory="."):
        """统计校对进度"""
        dir_path = Path(directory)
        total = 0
        proofread = 0

        for txt_file in dir_path.rglob("*.txt"):
            if txt_file.name.endswith('_校对.txt'):
                proofread += 1
            else:
                total += 1

        print(f"📊 校对进度统计 ({dir_path}):")
        print(f"  原始文件: {total}")
        print(f"  已校对: {proofread}")
        print(f"  待校对: {total - proofread}")
        if total > 0:
            print(f"  完成率: {proofread/total*100:.1f}%")

        return total, proofread

    def run_cli(self):
        """命令行入口"""
        parser = argparse.ArgumentParser(description="文字校对技能")
        parser.add_argument("input", nargs="?", help="输入文件或目录")
        parser.add_argument("--output", "-o", help="输出文件")
        parser.add_argument("--stats", "-s", action="store_true", help="统计校对进度")
        parser.add_argument("--batch", "-b", action="store_true", help="批量列出待校对文件")

        args = parser.parse_args()

        if args.stats:
            self.statistics(args.input or ".")
            return True
        elif args.batch:
            files = self.batch_proofread(args.input or ".")
            return True
        elif args.input:
            input_path = Path(args.input)
            if input_path.is_file():
                return self.proofread_file(args.input, args.output)
            else:
                self.batch_proofread(args.input)
                return True
        else:
            parser.print_help()
            return False


if __name__ == "__main__":
    skill = TextProofreadingSkill()
    sys.exit(0 if skill.run_cli() else 1)
