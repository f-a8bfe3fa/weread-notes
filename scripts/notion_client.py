"""Notion API 封装"""

import logging
import time
from datetime import datetime

import requests

from config import load_config, get_env

logger = logging.getLogger(__name__)

# Notion API 速率限制：每秒最多 3 次请求
_NOTION_RATE_LIMIT = 3
_last_request_times: list[float] = []


class NotionAPIError(Exception):
    """Notion API 请求异常，携带 HTTP 响应详情"""

    def __init__(self, message: str, status_code: int | None = None, response_body: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self) -> str:
        parts = [super().__str__()]
        if self.status_code is not None:
            parts.append(f"status={self.status_code}")
        if self.response_body is not None:
            parts.append(f"body={self.response_body}")
        return " | ".join(parts)


def _rate_limit():
    """Notion API 速率限制：每秒最多 3 次请求"""
    now = time.time()
    # 清理 1 秒前的记录
    global _last_request_times
    _last_request_times = [t for t in _last_request_times if now - t < 1.0]
    if len(_last_request_times) >= _NOTION_RATE_LIMIT:
        sleep_time = 1.0 - (now - _last_request_times[0]) + 0.05
        if sleep_time > 0:
            time.sleep(sleep_time)
    _last_request_times.append(time.time())


class NotionClient:
    """Notion API 客户端"""

    def __init__(self):
        config = load_config()
        self.base_url = config["notion"]["base_url"]
        self.database_id = get_env("NOTION_DATABASE_ID") or config["notion"].get(
            "database_id", ""
        )

        api_key = get_env("NOTION_API_KEY")
        if not api_key:
            raise ValueError(
                "NOTION_API_KEY 未设置，请在 .env 中配置"
            )

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            }
        )

    def _request(self, method: str, path: str, **kwargs) -> dict:
        """发送 Notion API 请求"""
        _rate_limit()
        url = f"{self.base_url}{path}"
        resp = self.session.request(method, url, **kwargs)
        if not resp.ok:
            body = None
            try:
                body = resp.text
            except Exception:
                pass
            raise NotionAPIError(
                f"Notion API {method} {path} 失败",
                status_code=resp.status_code,
                response_body=body,
            )
        return resp.json()

    def query_database(self, filter_clause: dict | None = None, 
                        page_size: int = 100, start_cursor: str | None = None) -> dict:
        """查询数据库

        Args:
            filter_clause: Notion filter 对象
            page_size: 每页数量
            start_cursor: 分页游标

        Returns:
            查询结果
        """
        body: dict = {"page_size": page_size}
        if filter_clause:
            body["filter"] = filter_clause
        if start_cursor:
            body["start_cursor"] = start_cursor
        return self._request("POST", f"/databases/{self.database_id}/query", json=body)

    def find_page_by_book_id(self, book_id: str) -> dict | None:
        """通过 bookId 查找 Notion 页面

        Args:
            book_id: 微信读书 bookId

        Returns:
            页面数据或 None
        """
        result = self.query_database(
            filter_clause={
                "property": "bookId",
                "rich_text": {"equals": book_id},
            }
        )
        results = result.get("results", [])
        if results:
            return results[0]
        return None

    def create_page(self, properties: dict, children: list | None = None) -> dict:
        """创建数据库页面

        Args:
            properties: 页面属性
            children: 页面内容 blocks

        Returns:
            创建的页面数据
        """
        body: dict = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
        }
        if children:
            body["children"] = children
        return self._request("POST", "/pages", json=body)

    def update_page_properties(self, page_id: str, properties: dict) -> dict:
        """更新页面属性

        Args:
            page_id: Notion 页面 ID
            properties: 要更新的属性

        Returns:
            更新后的页面数据
        """
        return self._request(
            "PATCH",
            f"/pages/{page_id}",
            json={"properties": properties},
        )

    def append_blocks(self, page_id: str, children: list) -> dict:
        """追加 blocks 到页面

        Args:
            page_id: Notion 页面 ID
            children: 要追加的 blocks

        Returns:
            追加结果
        """
        return self._request(
            "PATCH",
            f"/blocks/{page_id}/children",
            json={"children": children},
        )

    def get_page_blocks(self, page_id: str) -> list:
        """获取页面的 blocks

        Args:
            page_id: Notion 页面 ID

        Returns:
            blocks 列表
        """
        result = self._request("GET", f"/blocks/{page_id}/children")
        return result.get("results", [])

    def get_page_last_sync(self, page_id: str) -> str:
        """获取页面的最后同步时间

        Args:
            page_id: Notion 页面 ID

        Returns:
            最后同步时间字符串，或空字符串
        """
        page = self._request("GET", f"/pages/{page_id}")
        date_prop = (
            page.get("properties", {})
            .get("最后同步", {})
            .get("date", {})
        )
        if date_prop and date_prop.get("start"):
            return date_prop["start"]
        return ""

    def get_database_properties(self) -> dict:
        """获取数据库的属性（schema）

        Returns:
            数据库属性字典，key 为属性名
        """
        db = self._request("GET", f"/databases/{self.database_id}")
        return db.get("properties", {})

    def add_database_property(self, name: str, property_schema: dict):
        """向数据库添加新属性

        Args:
            name: 属性名
            property_schema: 属性 schema，例如 {"rich_text": {}}
        """
        body = {"properties": {name: property_schema}}
        self._request("PATCH", f"/databases/{self.database_id}", json=body)
        logger.info("数据库属性已创建: %s", name)
