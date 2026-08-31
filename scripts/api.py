"""微信读书 Agent API 封装

统一入口：POST https://i.weread.qq.com/api/agent/gateway
- 业务参数平铺在 body 顶层，与 api_name、skill_version 同级
- 严禁包在 params、data、body 等对象里
- 每次请求必须带 skill_version
"""

import logging
import time

import requests

from config import load_config, get_env

logger = logging.getLogger(__name__)


class WeReadAPIError(Exception):
    """微信读书 API 错误"""

    def __init__(self, api_name: str, errcode: int, errmsg: str):
        self.api_name = api_name
        self.errcode = errcode
        self.errmsg = errmsg
        super().__init__(f"[{api_name}] errcode={errcode}, errmsg={errmsg}")


class UpgradeRequiredError(Exception):
    """API 需要升级"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"API 升级要求: {message}")


class WeReadClient:
    """微信读书 API 客户端"""

    def __init__(self):
        config = load_config()
        self.base_url = config["weread"]["base_url"]
        self.skill_version = config["weread"]["skill_version"]
        self.timeout = config["sync"]["timeout_seconds"]
        self.retry_times = config["sync"]["retry_times"]

        api_key = get_env("WEREAD_API_KEY")
        if not api_key:
            raise ValueError(
                "WEREAD_API_KEY 未设置，请执行: export WEREAD_API_KEY=<你的apikey>"
            )
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/128.0.0.0 Safari/537.36"
                ),
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }
        )

    def _request(self, api_name: str, **params) -> dict:
        """发送 API 请求，带重试和升级检测

        Args:
            api_name: 接口路径，如 /user/notebooks
            **params: 业务参数，平铺传入

        Returns:
            API 回包 dict

        Raises:
            WeReadAPIError: API 返回错误
            UpgradeRequiredError: API 要求升级
        """
        body = {"api_name": api_name, "skill_version": self.skill_version}
        body.update(params)

        last_exc = None
        for attempt in range(1, self.retry_times + 1):
            try:
                resp = self.session.post(
                    self.base_url, json=body, timeout=self.timeout
                )
                resp.raise_for_status()
                data = resp.json()

                # 检查升级信息
                if "upgrade_info" in data:
                    upgrade_msg = data["upgrade_info"].get("message", "请升级")
                    raise UpgradeRequiredError(upgrade_msg)

                # 检查错误码
                errcode = data.get("errcode", 0)
                if errcode != 0:
                    errmsg = data.get("errmsg", "未知错误")
                    raise WeReadAPIError(api_name, errcode, errmsg)

                return data

            except UpgradeRequiredError:
                raise
            except WeReadAPIError as e:
                last_exc = e
                logger.warning(
                    "[%s] 请求失败 (第%d/%d次): %s",
                    api_name, attempt, self.retry_times, e,
                )
                if attempt < self.retry_times:
                    time.sleep(2 ** attempt)
            except requests.HTTPError as e:
                last_exc = e
                resp_text = ""
                try:
                    resp_text = e.response.text[:500]
                except Exception:
                    pass
                logger.warning(
                    "[%s] HTTP 错误 (第%d/%d次): %s | 响应体: %s",
                    api_name, attempt, self.retry_times, e, resp_text,
                )
                if attempt < self.retry_times:
                    time.sleep(2 ** attempt)
            except requests.RequestException as e:
                last_exc = e
                logger.warning(
                    "[%s] 网络错误 (第%d/%d次): %s",
                    api_name, attempt, self.retry_times, e,
                )
                if attempt < self.retry_times:
                    time.sleep(2 ** attempt)

        raise last_exc  # type: ignore

    # ── 笔记本 ──────────────────────────────────────────────

    def get_notebooks(self, count: int = 100, last_sort: int = 0) -> dict:
        """获取有笔记的书籍列表（游标分页）

        Args:
            count: 每页数量
            last_sort: 翻页游标，首次传 0

        Returns:
            包含 books, hasMore, totalBookCount 等字段
        """
        params: dict = {"count": count}
        if last_sort > 0:
            params["lastSort"] = last_sort
        return self._request("/user/notebooks", **params)

    def get_all_notebooks(self) -> list:
        """获取所有有笔记的书籍（自动翻页）

        Returns:
            完整的书籍列表
        """
        config = load_config()
        page_size = config["sync"]["notebooks_page_size"]
        all_books = []
        last_sort = 0

        while True:
            data = self.get_notebooks(count=page_size, last_sort=last_sort)
            books = data.get("books", [])
            all_books.extend(books)

            if not data.get("hasMore"):
                break

            if books:
                last_sort = books[-1].get("sort", 0)
            else:
                break

        return all_books

    # ── 书籍信息 ──────────────────────────────────────────────

    def get_book_info(self, book_id: str) -> dict:
        """获取书籍基本信息"""
        return self._request("/book/info", bookId=book_id)

    def get_chapter_info(self, book_id: str) -> dict:
        """获取章节目录"""
        return self._request("/book/chapterinfo", bookId=book_id)

    def get_book_progress(self, book_id: str) -> dict:
        """获取阅读进度"""
        return self._request("/book/getprogress", bookId=book_id)

    # ── 划线 ──────────────────────────────────────────────

    def get_bookmark_list(self, book_id: str) -> dict:
        """获取单本书的划线列表（不含书签，无分页）"""
        return self._request("/book/bookmarklist", bookId=book_id)

    def get_best_bookmarks(self, book_id: str, chapter_uid: int = 0) -> dict:
        """获取书籍热门划线（可选，固定返回前20条）"""
        return self._request(
            "/book/bestbookmarks",
            bookId=book_id,
            chapterUid=chapter_uid,
        )

    # ── 想法/点评 ──────────────────────────────────────────────

    def get_my_reviews(self, book_id: str, synckey: int = 0) -> dict:
        """获取单本书的个人想法与点评（synckey 分页）

        Args:
            book_id: 书籍 ID
            synckey: 翻页游标，首次传 0

        Returns:
            包含 reviews, hasMore, synckey 等字段
        """
        config = load_config()
        page_size = config["sync"]["reviews_page_size"]
        return self._request(
            "/review/list/mine",
            bookid=book_id,
            synckey=synckey,
            count=page_size,
        )

    def get_all_my_reviews(self, book_id: str) -> list:
        """获取单本书的所有个人想法与点评（自动翻页）

        Returns:
            完整的点评列表
        """
        all_reviews = []
        synckey = 0

        while True:
            data = self.get_my_reviews(book_id, synckey=synckey)
            reviews = data.get("reviews", [])
            all_reviews.extend(reviews)

            if not data.get("hasMore"):
                break

            synckey = data.get("synckey", 0)
            if synckey == 0:
                break

        return all_reviews
