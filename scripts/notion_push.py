"""Notion 推送模块 — 将书籍数据推送至 Notion

提供两种使用方式：
1. push_single_book() — 单本书推送（供 sync.py 循环内调用）
2. push_to_notion()     — 批量推送（遍历 index.json，可独立运行）

推送策略：
- 通过 bookId 查询 Notion 数据库
- 不存在 → 创建新页面（全量写入）
- 存在 → 删除旧 blocks + 全量更新（不做时间判断）

用法：
  python scripts/notion_push.py
"""

import json
import logging
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import load_env, get_data_dir, get_index_path, PROJECT_ROOT
from utils import load_json, save_json
from notion_client import NotionClient, NotionAPIError
from md_to_notion import md_to_blocks

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("notion_push")

# 模块级 Notion 客户端（延迟初始化）
_notion_client: NotionClient | None = None

# 推送失败日志文件路径（项目根目录下）
_PUSH_FAIL_LOG_PATH: Path = PROJECT_ROOT / "notion_push_failures.json"
_LOG_RETENTION_DAYS: int = 7


def _load_failure_log() -> list[dict]:
    """加载现有的推送失败日志"""
    if not _PUSH_FAIL_LOG_PATH.exists():
        return []
    data = load_json(_PUSH_FAIL_LOG_PATH)
    if isinstance(data, list):
        return data
    return []


def _save_failure_log(entries: list[dict]):
    """保存推送失败日志"""
    save_json(_PUSH_FAIL_LOG_PATH, entries)


def _cleanup_old_entries(entries: list[dict]) -> list[dict]:
    """清理超过保留期限的旧日志条目"""
    cutoff = datetime.now(timezone.utc) - timedelta(days=_LOG_RETENTION_DAYS)
    kept = []
    for entry in entries:
        ts_str = entry.get("timestamp", "")
        if not ts_str:
            continue
        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            if ts >= cutoff:
                kept.append(entry)
        except (ValueError, TypeError):
            kept.append(entry)
    removed = len(entries) - len(kept)
    if removed > 0:
        logger.info("清理了 %d 条超过 %d 天的推送失败日志", removed, _LOG_RETENTION_DAYS)
    return kept


def record_push_failure(
    book_id: str,
    title: str,
    exception: Exception,
    operation: str = "",
):
    """记录一次推送失败到日志文件

    Args:
        book_id: 书籍 ID
        title: 书籍名称
        exception: 捕获到的异常
        operation: 失败时正在进行的操作（如 create_page / update_page 等）
    """
    try:
        entries = _load_failure_log()
        entries = _cleanup_old_entries(entries)

        error_info = {
            "type": exception.__class__.__name__,
            "message": str(exception),
        }
        if isinstance(exception, NotionAPIError):
            error_info["status_code"] = exception.status_code
            error_info["response_body"] = exception.response_body

        entry = {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "book_id": book_id,
            "title": title,
            "operation": operation,
            "error": error_info,
        }
        entries.append(entry)
        _save_failure_log(entries)
        logger.info("已记录推送失败日志: %s (%s)", title, book_id)
    except Exception as log_err:
        logger.error("记录推送失败日志时出错: %s", log_err)


def _get_notion_client() -> NotionClient:
    """获取或初始化 Notion 客户端（单例）"""
    global _notion_client
    if _notion_client is None:
        load_env()
        _notion_client = NotionClient()
    return _notion_client


# 必需的数据库属性定义（属性名 -> schema）
_REQUIRED_PROPERTIES: dict[str, dict] = {
    "书名": {"title": {}},
    "bookId": {"rich_text": {}},
    "阅读进度": {"select": {"options": [
        {"name": "已读完", "color": "green"},
        {"name": "在读", "color": "yellow"},
        {"name": "未读", "color": "gray"},
    ]}},
    "笔记数": {"number": {"format": "number"}},
}

_OPTIONAL_PROPERTIES: dict[str, dict] = {
    "作者": {"rich_text": {}},
    "译者": {"rich_text": {}},
    "出版社": {"rich_text": {}},
    "分类": {"select": {}},
    "封面": {"files": {}},
    "网页链接": {"url": {}},
}


def _ensure_database_properties(client: NotionClient, book_data: dict):
    """检查并自动创建缺失的数据库属性

    Args:
        client: Notion 客户端
        book_data: 书籍 JSON 数据（用于判断需要哪些可选属性）
    """
    try:
        existing = client.get_database_properties()
    except Exception as e:
        logger.warning("获取数据库属性失败，跳过自动创建: %s", e)
        return

    # 合并必需和可选属性
    meta = book_data.get("meta", {})
    required = dict(_REQUIRED_PROPERTIES)
    optional = dict(_OPTIONAL_PROPERTIES)

    # 根据数据内容决定需要哪些可选属性
    if meta.get("author"):
        required["作者"] = optional.pop("作者")
    if meta.get("translator"):
        required["译者"] = optional.pop("译者")
    if meta.get("publisher"):
        required["出版社"] = optional.pop("出版社")
    if meta.get("category"):
        required["分类"] = optional.pop("分类")
    if meta.get("cover", "").startswith("http"):
        required["封面"] = optional.pop("封面")
    if meta.get("webLink", "").startswith("http"):
        required["网页链接"] = optional.pop("网页链接")

    missing = []
    for name, schema in required.items():
        if name not in existing:
            missing.append((name, schema))

    if not missing:
        return

    logger.info("检测到 %d 个缺失的数据库属性，正在自动创建...", len(missing))
    for name, schema in missing:
        try:
            client.add_database_property(name, schema)
        except Exception as e:
            logger.error("创建属性失败 [%s]: %s", name, e)
            raise


def build_page_properties(book_data: dict) -> dict:
    """构建 Notion 数据库页面属性

    Args:
        book_data: 书籍 JSON 数据

    Returns:
        Notion properties dict
    """
    meta = book_data.get("meta", {})
    title = meta.get("title", "")
    book_id = meta.get("bookId", "")
    author = meta.get("author", "")
    translator = meta.get("translator", "")
    category = meta.get("category", "")
    publisher = meta.get("publisher", "")
    cover = meta.get("cover", "")
    reading_progress = meta.get("readingProgress", "")
    note_count = meta.get("noteCount", 0)
    review_count = meta.get("reviewCount", 0)
    bookmark_count = meta.get("bookmarkCount", 0)
    total_notes = note_count + review_count + bookmark_count

    # 阅读进度映射
    progress_val = meta.get("readingProgress", "")
    if progress_val == "100%":
        progress_select = "已读完"
    elif progress_val == "0%":
        progress_select = "未读"
    else:
        progress_select = "在读"

    properties = {
        "书名": {"title": [{"text": {"content": title}}]},
        "bookId": {"rich_text": [{"text": {"content": book_id}}]},
        "阅读进度": {"select": {"name": progress_select}},
        "笔记数": {"number": total_notes},
    }

    # 仅在非空时添加属性
    if author:
        properties["作者"] = {"rich_text": [{"text": {"content": author}}]}
    if translator:
        properties["译者"] = {"rich_text": [{"text": {"content": translator}}]}
    if publisher:
        properties["出版社"] = {"rich_text": [{"text": {"content": publisher}}]}
    if category:
        properties["分类"] = {"select": {"name": category}}

    # 清理 None 值
    properties = {k: v for k, v in properties.items() if v is not None}

    # 封面（仅在有有效 URL 时添加）
    if cover and cover.startswith("http"):
        properties["封面"] = {
            "files": [{"name": f"{title}_cover", "external": {"url": cover}}]
        }

    # 网页链接（仅在有有效 URL 时添加）
    web_link = meta.get("webLink", "")
    if web_link and web_link.startswith("http"):
        properties["网页链接"] = {"url": web_link}

    return properties


def _get_icon(cover_url: str) -> dict | None:
    """构建 Notion 图标对象

    Args:
        cover_url: 封面图片 URL

    Returns:
        Notion 图标对象，或 None（如果 URL 无效）
    """
    if cover_url and cover_url.startswith("http"):
        return {"type": "external", "external": {"url": cover_url}}
    return None


def push_single_book(client: NotionClient, book_data: dict, json_path: Path) -> bool:
    """推送单本书到 Notion（直接覆盖）

    通过 bookId 查询 Notion 数据库：
    - 不存在 → 创建新页面（全量写入）
    - 存在 → 删除旧 blocks + 全量更新

    Args:
        client: Notion 客户端
        book_data: 书籍 JSON 数据
        json_path: JSON 文件路径（用于定位 .md 文件）

    Returns:
        是否成功
    """
    meta = book_data.get("meta", {})
    book_id = meta.get("bookId", "")
    title = meta.get("title", f"未知_{book_id}")
    cover = meta.get("cover", "")

    try:
        # 检查并自动创建缺失的数据库属性
        _ensure_database_properties(client, book_data)

        # 查询 Notion 是否已存在
        page = client.find_page_by_book_id(book_id)

        properties = build_page_properties(book_data)

        # 读取 Markdown 并转换为 blocks
        md_path = json_path.with_suffix(".md")
        children = []
        if md_path.exists():
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
            children = md_to_blocks(md_content)

        # 构建图标（使用封面作为页面图标）
        icon = _get_icon(cover)

        if page is None:
            # 不存在 → 创建新页面（带图标）
            first_batch = children[:100] if len(children) > 100 else children
            new_page = client.create_page(properties, children=first_batch, icon=icon)

            # 追加剩余 blocks
            if len(children) > 100 and new_page:
                page_id = new_page["id"]
                for i in range(100, len(children), 100):
                    batch = children[i:i + 100]
                    client.append_blocks(page_id, batch)

            logger.info("Notion 新建: %s", title)
        else:
            # 存在 → 更新属性 + 全量替换内容 + 更新图标
            page_id = page["id"]
            client.update_page_properties(page_id, properties)

            # 更新页面图标（如果封面有效）
            if icon:
                try:
                    client._request("PATCH", f"/pages/{page_id}", json={"icon": icon})
                except Exception as e:
                    logger.warning("更新页面图标失败: %s - %s", title, e)

            if children:
                # 删除旧 blocks
                try:
                    existing_blocks = client.get_page_blocks(page_id)
                    for block in existing_blocks:
                        block_id = block.get("id")
                        if block_id:
                            try:
                                client._request("DELETE", f"/blocks/{block_id}")
                            except Exception:
                                pass
                except Exception:
                    pass

                # 添加新 blocks（分批）
                for i in range(0, len(children), 100):
                    batch = children[i:i + 100]
                    client.append_blocks(page_id, batch)

            logger.info("Notion 更新: %s", title)

        return True

    except Exception as e:
        logger.error("Notion 推送失败: %s - %s", title, e)
        record_push_failure(
            book_id=book_id,
            title=title,
            exception=e,
            operation="push_single_book",
        )
        return False


def push_to_notion(book_ids: list[str] | None = None):
    """批量推送书籍到 Notion

    Args:
        book_ids: 指定推送的书籍 ID 列表。为 None 时推送 index.json 中所有书籍。
    """
    client = _get_notion_client()

    # 加载索引
    index_path = get_index_path()
    index = load_json(index_path)
    if not index:
        logger.info("无索引数据，跳过 Notion 推送")
        return

    books = index.get("books", {})
    if not books:
        logger.info("索引中无书籍数据，跳过 Notion 推送")
        return

    # 确定推送范围
    if book_ids:
        target_books = {bid: books[bid] for bid in book_ids if bid in books}
    else:
        target_books = books

    data_dir = get_data_dir()
    created = 0
    updated = 0
    failed = 0

    for book_id, book_info in target_books.items():
        title = book_info.get("title", f"未知_{book_id}")

        # 加载本地 JSON
        json_path = data_dir / book_info.get("path", "")
        if not json_path.exists():
            found = list(data_dir.rglob(f"{book_id}.json"))
            if found:
                json_path = found[0]
            else:
                logger.warning("找不到 JSON 文件: %s", book_id)
                failed += 1
                continue

        book_data = load_json(json_path)
        if not book_data:
            logger.warning("JSON 文件为空: %s", json_path)
            failed += 1
            continue

        # 判断是新建还是更新
        try:
            page = client.find_page_by_book_id(book_id)
            is_new = page is None
        except Exception:
            is_new = True

        success = push_single_book(client, book_data, json_path)
        if success:
            if is_new:
                created += 1
            else:
                updated += 1
        else:
            failed += 1

    logger.info(
        "Notion 推送完成: 新建 %d, 更新 %d, 失败 %d",
        created, updated, failed,
    )


if __name__ == "__main__":
    push_to_notion()
