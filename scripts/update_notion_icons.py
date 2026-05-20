#!/usr/bin/env python3
"""为 Notion 数据库中的书籍页面添加封面图标

工作流程：
1. 读取 index.json 获取书籍列表
2. 调用微信读书 API 获取每本书的封面 URL
3. 查询 Notion 数据库找到对应页面
4. 使用封面 URL 设置页面图标

用法：
    export WEREAD_API_KEY=<key>
    export NOTION_API_KEY=<key>
    export NOTION_DATABASE_ID=<id>
    python scripts/update_notion_icons.py
"""

import json
import logging
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from api import WeReadClient
from notion_client import NotionClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("update_icons")


def load_index(index_path: Path) -> dict:
    """加载 index.json"""
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_book_cover(weread_client: WeReadClient, book_id: str) -> str | None:
    """从微信读书 API 获取书籍封面 URL"""
    try:
        info = weread_client.get_book_info(book_id)
        cover = info.get("cover", "")
        if cover and cover.startswith("http"):
            return cover
        return None
    except Exception as e:
        logger.warning("获取书籍 %s 封面失败: %s", book_id, e)
        return None


def build_icon(cover_url: str) -> dict | None:
    """构建 Notion 图标对象"""
    if cover_url and cover_url.startswith("http"):
        return {"type": "external", "external": {"url": cover_url}}
    return None


def update_page_icon(notion_client: NotionClient, page_id: str, icon: dict) -> bool:
    """更新 Notion 页面图标"""
    try:
        notion_client._request("PATCH", f"/pages/{page_id}", json={"icon": icon})
        return True
    except Exception as e:
        logger.warning("更新页面 %s 图标失败: %s", page_id, e)
        return False


def main():
    # 检查环境变量
    required_envs = ["WEREAD_API_KEY", "NOTION_API_KEY", "NOTION_DATABASE_ID"]
    for env in required_envs:
        if not os.environ.get(env):
            logger.error("环境变量 %s 未设置", env)
            sys.exit(1)

    # 初始化客户端
    weread_client = WeReadClient()
    notion_client = NotionClient()

    # 加载 index.json
    index_path = Path(__file__).resolve().parent.parent / "index.json"
    if not index_path.exists():
        logger.error("index.json 不存在: %s", index_path)
        sys.exit(1)

    index_data = load_index(index_path)
    books = index_data.get("books", {})
    total = len(books)
    logger.info("共 %d 本书需要处理", total)

    success_count = 0
    skip_count = 0
    fail_count = 0

    for idx, (book_id, book_info) in enumerate(books.items(), 1):
        title = book_info.get("title", f"未知_{book_id}")
        logger.info("[%d/%d] 处理: %s (ID: %s)", idx, total, title, book_id)

        # 1. 获取封面 URL
        cover = get_book_cover(weread_client, book_id)
        if not cover:
            logger.info("  无封面，跳过")
            skip_count += 1
            continue

        # 2. 查找 Notion 页面
        page = notion_client.find_page_by_book_id(book_id)
        if not page:
            logger.info("  Notion 页面不存在，跳过")
            skip_count += 1
            continue

        page_id = page["id"]

        # 3. 检查是否已有图标
        existing_icon = page.get("icon")
        if existing_icon and existing_icon.get("type") == "external":
            logger.info("  已有图标，跳过")
            skip_count += 1
            continue

        # 4. 设置图标
        icon = build_icon(cover)
        if update_page_icon(notion_client, page_id, icon):
            logger.info("  图标更新成功")
            success_count += 1
        else:
            fail_count += 1

        # 速率限制：Notion API 每秒最多 3 次
        time.sleep(0.35)

    logger.info(
        "处理完成: 成功 %d, 跳过 %d, 失败 %d",
        success_count, skip_count, fail_count
    )


if __name__ == "__main__":
    main()
