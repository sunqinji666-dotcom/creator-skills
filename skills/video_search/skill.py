#!/usr/bin/env python3
"""
多模态视频向量检索技能
支持语义搜索、相似推荐和自动聚类
使用火山引擎多模态向量化 API
"""

import os
import sys
import json
import argparse
from pathlib import Path

# 导入已有的 VideoSearch 类
from video_search_multimodal import VideoSearch


class VideoSearchSkill:
    def __init__(self):
        self.name = "video_search"
        self.description = "多模态视频向量检索，支持语义搜索、相似推荐和自动聚类"
        self.api_key = os.environ.get("VOLC_API_KEY", "")

    def build_index(self, search_dirs, output_path, mode="text", use_base64=False):
        """构建向量索引"""
        searcher = VideoSearch(search_dirs, api_key=self.api_key)
        searcher.scan_all_files()

        if mode == "text":
            searcher.build_vectors_from_text()
        else:
            searcher.build_vectors_from_video(use_base64=use_base64)

        searcher.save_index(output_path)
        return True

    def interactive_search(self, index_path=None):
        """交互式搜索"""
        if index_path and Path(index_path).exists():
            searcher = VideoSearch([])
            if not searcher.load_index(index_path):
                print(f"❌ 无法加载索引: {index_path}")
                return False
        else:
            print("ℹ️ 请在交互中指定目录，将自动构建索引")

        from video_search_multimodal import main
        return main()

    def search_query(self, index_path, query, top_k=5):
        """直接搜索查询"""
        searcher = VideoSearch([])
        if not searcher.load_index(index_path):
            print(f"❌ 无法加载索引: {index_path}")
            return []

        results = searcher.search(query, top_k=top_k)

        print(f"\n📊 搜索结果 '{query}':")
        for i, (name, score) in enumerate(results, 1):
            source = searcher.file_sources.get(name, "未知")
            print(f"  {i}. {name} (相似度: {score:.4f}) - {source}")

        return results

    def recommend(self, index_path, filename, top_k=3):
        """相似推荐"""
        searcher = VideoSearch([])
        if not searcher.load_index(index_path):
            print(f"❌ 无法加载索引: {index_path}")
            return []

        results = searcher.recommend_similar(filename, top_k=top_k)

        print(f"\n📊 相似推荐 '{filename}':")
        for i, (name, score) in enumerate(results, 1):
            source = searcher.file_sources.get(name, "未知")
            print(f"  {i}. {name} (相似度: {score:.4f}) - {source}")

        return results

    def cluster(self, index_path, n_clusters=5):
        """自动聚类"""
        searcher = VideoSearch([])
        if not searcher.load_index(index_path):
            print(f"❌ 无法加载索引: {index_path}")
            return {}

        clusters = searcher.auto_cluster(n_clusters)

        print(f"\n📊 自动分类 ({n_clusters} 类):")
        for label, files in clusters.items():
            print(f"\n  类别 {label + 1}:")
            for f in files:
                source = searcher.file_sources.get(f, "未知")
                print(f"    - {f} ({source})")

        return clusters

    def run_cli(self):
        """命令行入口"""
        parser = argparse.ArgumentParser(description="多模态视频向量检索技能")
        subparsers = parser.add_subparsers(dest="command", required=True)

        # build 命令
        build_parser = subparsers.add_parser("build", help="构建索引")
        build_parser.add_argument("dirs", nargs="+", help="要索引的目录")
        build_parser.add_argument("--output", "-o", required=True, help="输出索引路径")
        build_parser.add_argument("--mode", "-m", choices=["text", "video"], default="text",
                                 help="构建模式: text=使用转录文字(推荐), video=使用视频文件")
        build_parser.add_argument("--base64", action="store_true", help="使用 Base64 上传视频")

        # search 命令
        search_parser = subparsers.add_parser("search", help="语义搜索")
        search_parser.add_argument("index", help="索引文件路径")
        search_parser.add_argument("query", help="搜索关键词")
        search_parser.add_argument("--top", "-k", type=int, default=5, help="返回结果数量")

        # similar 命令
        similar_parser = subparsers.add_parser("similar", help="相似推荐")
        similar_parser.add_argument("index", help="索引文件路径")
        similar_parser.add_argument("filename", help="文件名")
        similar_parser.add_argument("--top", "-k", type=int, default=3, help="返回结果数量")

        # cluster 命令
        cluster_parser = subparsers.add_parser("cluster", help="自动聚类")
        cluster_parser.add_argument("index", help="索引文件路径")
        cluster_parser.add_argument("n_clusters", "-n", type=int, default=5, help="聚类数量")

        # interactive 命令
        interactive_parser = subparsers.add_parser("interactive", help="交互式搜索")
        interactive_parser.add_argument("index", nargs="?", help="索引文件路径(可选)")

        args = parser.parse_args()

        if args.command == "build":
            return self.build_index(args.dirs, args.output, mode=args.mode, use_base64=args.base64)
        elif args.command == "search":
            self.search_query(args.index, args.query, top_k=args.top)
            return True
        elif args.command == "similar":
            self.recommend(args.index, args.filename, top_k=args.top)
            return True
        elif args.command == "cluster":
            self.cluster(args.index, args.n_clusters)
            return True
        elif args.command == "interactive":
            return self.interactive_search(args.index)
        else:
            print(f"未知命令: {args.command}")
            return False


if __name__ == "__main__":
    skill = VideoSearchSkill()
    sys.exit(0 if skill.run_cli() else 1)
