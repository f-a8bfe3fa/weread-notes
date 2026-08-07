"""测试微信读书 API 翻页"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve()."""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"]"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNS"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient
"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('book"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('bookId')}, sort={nb.get('sort')}")

print("\n=== 测试每本书的 get_all_my_reviews"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('bookId')}, sort={nb.get('sort')}")

print("\n=== 测试每本书的 get_all_my_reviews 翻页 ===")
for nb in notebooks:
    book_id = nb.get("bookId"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('bookId')}, sort={nb.get('sort')}")

print("\n=== 测试每本书的 get_all_my_reviews 翻页 ===")
for nb in notebooks:
    book_id = nb.get("bookId", "")
    title = nb.get(""""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('bookId')}, sort={nb.get('sort')}")

print("\n=== 测试每本书的 get_all_my_reviews 翻页 ===")
for nb in notebooks:
    book_id = nb.get("bookId", "")
    title = nb.get("book", {}).get("title", f"未知"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('bookId')}, sort={nb.get('sort')}")

print("\n=== 测试每本书的 get_all_my_reviews 翻页 ===")
for nb in notebooks:
    book_id = nb.get("bookId", "")
    title = nb.get("book", {}).get("title", f"未知_{book_id}")
    print(f""""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('bookId')}, sort={nb.get('sort')}")

print("\n=== 测试每本书的 get_all_my_reviews 翻页 ===")
for nb in notebooks:
    book_id = nb.get("bookId", "")
    title = nb.get("book", {}).get("title", f"未知_{book_id}")
    print(f"\n--- {title} ({book_id})"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('bookId')}, sort={nb.get('sort')}")

print("\n=== 测试每本书的 get_all_my_reviews 翻页 ===")
for nb in notebooks:
    book_id = nb.get("bookId", "")
    title = nb.get("book", {}).get("title", f"未知_{book_id}")
    print(f"\n--- {title} ({book_id}) ---")
    try:
        all_re"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('bookId')}, sort={nb.get('sort')}")

print("\n=== 测试每本书的 get_all_my_reviews 翻页 ===")
for nb in notebooks:
    book_id = nb.get("bookId", "")
    title = nb.get("book", {}).get("title", f"未知_{book_id}")
    print(f"\n--- {title} ({book_id}) ---")
    try:
        all_reviews = []
        synckey = 0"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('bookId')}, sort={nb.get('sort')}")

print("\n=== 测试每本书的 get_all_my_reviews 翻页 ===")
for nb in notebooks:
    book_id = nb.get("bookId", "")
    title = nb.get("book", {}).get("title", f"未知_{book_id}")
    print(f"\n--- {title} ({book_id}) ---")
    try:
        all_reviews = []
        synckey = 0
        page = 0
        seen_sync"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('bookId')}, sort={nb.get('sort')}")

print("\n=== 测试每本书的 get_all_my_reviews 翻页 ===")
for nb in notebooks:
    book_id = nb.get("bookId", "")
    title = nb.get("book", {}).get("title", f"未知_{book_id}")
    print(f"\n--- {title} ({book_id}) ---")
    try:
        all_reviews = []
        synckey = 0
        page = 0
        seen_synckeys = set()
        while True:
"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('bookId')}, sort={nb.get('sort')}")

print("\n=== 测试每本书的 get_all_my_reviews 翻页 ===")
for nb in notebooks:
    book_id = nb.get("bookId", "")
    title = nb.get("book", {}).get("title", f"未知_{book_id}")
    print(f"\n--- {title} ({book_id}) ---")
    try:
        all_reviews = []
        synckey = 0
        page = 0
        seen_synckeys = set()
        while True:
            page += 1
            data = client"""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('bookId')}, sort={nb.get('sort')}")

print("\n=== 测试每本书的 get_all_my_reviews 翻页 ===")
for nb in notebooks:
    book_id = nb.get("bookId", "")
    title = nb.get("book", {}).get("title", f"未知_{book_id}")
    print(f"\n--- {title} ({book_id}) ---")
    try:
        all_reviews = []
        synckey = 0
        page = 0
        seen_synckeys = set()
        while True:
            page += 1
            data = client.get_my_reviews(book_id, synckey="""测试微信读书 API 翻页是否可能出现死循环"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

import os
os.environ["WEREAD_API_KEY"] = "wrk-h1dyGSKNSrqo7ljkJjWqKAAA"

from api import WeReadClient

client = WeReadClient()

print("=== 测试 get_all_notebooks 翻页 ===")
notebooks = client.get_all_notebooks()
print(f"共 {len(notebooks)} 本有笔记的书籍")
for nb in notebooks:
    book = nb.get("book", {})
    print(f"  - {book.get('title', '未知')}: bookId={nb.get('bookId')}, sort={nb.get('sort')}")

print("\n=== 测试每本书的 get_all_my_reviews 翻页 ===")
for nb in notebooks:
    book_id = nb.get("bookId", "")
    title = nb.get("book", {}).get("title", f"未知_{book_id}")
    print(f"\n--- {title} ({book_id}) ---")
    try:
        all_reviews = []
        synckey = 0
        page = 0
        seen_synckeys = set()
        while True:
            page += 1
            data = client.get_my_reviews(book_id, synckey=synckey)
            reviews = data.get("