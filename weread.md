# book — 书籍信息与阅读进度

查看书籍详情、章节目录、阅读进度。

## 接口

### `/book/info` — 书籍基本信息

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bookId` | string | 是 | 书籍 ID |

**回包：**

| 字段 | 说明 |
|------|------|
| `bookId` | 书籍 ID |
| `readerLink` | 阅读器跳转链接；展示为 `[打开阅读]({readerLink})` |
| `deepLink` | 书籍详情跳转链接；没有 `readerLink` 时可展示为 `[查看详情]({deepLink})` |
| `title` | 书名 |
| `author` | 作者 |
| `translator` | 译者 |
| `cover` | 封面 URL |
| `intro` | 简介 |
| `category` | 分类 |
| `publisher` | 出版社 |
| `publishTime` | 出版时间 |
| `isbn` | ISBN |
| `wordCount` | 总字数 |
| `newRating` | 评分（百分制） |
| `newRatingCount` | 评分人数 |
| `newRatingDetail` | 评分分布详情 |

### `/book/chapterinfo` — 章节目录

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bookId` | string | 是 | 书籍 ID |

**回包：**

| 字段 | 说明 |
|------|------|
| `bookId` | 书籍 ID |
| `synckey` | 同步 key（版本号） |
| `chapterUpdateTime` | 章节最后更新时间 |
| `chapters` | 章节数组 |
| `chapters[].chapterUid` | 章节 UID（用于其他接口如 underlines） |
| `chapters[].chapterIdx` | 章节序号 |
| `chapters[].title` | 章节标题 |
| `chapters[].wordCount` | 章节字数 |
| `chapters[].level` | 目录层级（1=一级标题, 2=二级…） |
| `chapters[].updateTime` | 章节更新时间 |
| `chapters[].price` | 章节价格（0=免费） |
| `chapters[].paid` | 是否已购买（1=已购买） |
| `chapters[].isMPChapter` | 是否公众号章节（1=是） |
| `chapters[].anchors` | 章节内锚点/子标题数组 |

### `/book/getprogress` — 阅读进度

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bookId` | string | 是 | 书籍 ID |

**回包：**

| 字段 | 说明 |
|------|------|
| `bookId` | 书籍 ID |
| `book.chapterUid` | 当前阅读章节 UID |
| `book.chapterOffset` | 当前章节内偏移 |
| `book.progress` | 阅读进度百分比（整数，0-100）。**注意：1 表示 1%，不是 100%**。0=未读，1-99=部分阅读（如 1=仅翻了几页），100=已读完。只有 100 才代表读完 |
| `book.updateTime` | 最后阅读时间 |
| `book.recordReadingTime` | 累计阅读时长（秒） |
| `book.finishTime` | 读完时间（仅 progress=100 时存在，否则无此字段） |
| `book.isStartReading` | 是否已开始阅读 |
| `timestamp` | 服务端时间戳 |

## 工作流

1. **查看书籍详情**：用户提供 bookId 或书名（书名先调 `/store/search`），调 `/book/info` 获取基本信息。
2. **查看章节目录**：调 `/book/chapterinfo`，按 level 层级缩进展示目录结构。
3. **查看阅读进度**：调 `/book/getprogress`，展示阅读百分比和累计时长。
4. `chapterUid` 是后续查看章节划线热度（`/book/underlines`）和热门划线（`/book/bestbookmarks`）等接口的参数。

## 输出格式
- 书籍详情：展示书名、作者、评分、简介等核心信息
- 章节目录：按层级缩进展示，标注字数和付费状态
- 阅读进度：展示百分比和阅读时长（转为小时/分钟）。**progress 是 0-100 的整数，必须带 % 号展示**（如 progress=1 展示为"1%"，progress=45 展示为"45%"）。只有 progress=100 且有 finishTime 时才表示已读完
- 书籍信息获取失败时回复：`暂时无法获取书籍信息，请稍后再试~`
- 无结果时根据用户问题自然说明没有找到对应书籍或记录，不要编造数据
# discover — 发现推荐好书

## 接口

### `/book/recommend` — 个性化推荐（为你推荐）

基于用户阅读记录的个性化推荐，与 App 首页「为你推荐」一致。

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `count` | int | 否 | 每页数量，默认 12 |
| `maxIdx` | int | 否 | 翻页偏移，默认 0 |

**回包：**

| 字段 | 说明 |
|------|------|
| `books` | 推荐书籍数组 |
| `books[].bookId` | 书籍 ID |
| `books[].readerLink` | 阅读器跳转链接；展示为 `[打开阅读]({readerLink})` |
| `books[].deepLink` | 书籍详情跳转链接；没有 `readerLink` 时可展示为 `[查看详情]({deepLink})` |
| `books[].title` | 书名 |
| `books[].author` | 作者 |
| `books[].cover` | 封面图 URL |
| `books[].intro` | 简介 |
| `books[].category` | 分类 |
| `books[].reason` | 推荐理由 |
| `books[].readingCount` | 在读人数 |
| `books[].searchIdx` | 结果序号（用于翻页） |
| `books[].newRating` | 评分（0-100） |
| `books[].newRatingCount` | 评分人数 |
| `books[].newRatingDetail.title` | 评分标签（如"神作""力荐"） |
| `books[].price` | 价格（分） |
| `books[].payType` | 付费类型 |
| `books[].type` | 书籍类型（0=电子书） |

### `/book/similar` — 相似书推荐

基于某本书推荐相似书籍，与 App 书籍详情页「相似推荐」一致。

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bookId` | string | 是 | 书籍 ID |
| `count` | int | 是 | 每页数量；实际调用必须显式传入，首次推荐传 12，用户明确指定数量时可传对应数量 |
| `maxIdx` | int | 是 | 翻页偏移；实际调用必须显式传入，首次传 0，翻页传上一页最后一条的 `idx` |
| `sessionId` | string | 否 | 翻页会话 ID（首次不传，后续传回包中的值） |

> `/book/similar` 实际转发到 `/book/detailinfo?listtypes=2&synckey=0`。底层要求 `listTypes`、`synckey`、`maxIdx`、`count` 四组参数长度一致，因此调用时不能省略 `count` 和 `maxIdx`，不要依赖接口文档中的默认值。

**回包：**

| 字段 | 说明 |
|------|------|
| `booksimilar.sessionId` | 会话 ID（翻页时传入下次请求） |
| `booksimilar.books` | 推荐书籍数组 |
| `booksimilar.books[].idx` | 结果序号（下次请求 maxIdx 传最后一条的 idx） |
| `booksimilar.books[].book.bookInfo` | 书籍信息（bookId, title, author, cover 等） |
| `booksimilar.books[].book.bookInfo.readerLink` | 阅读器跳转链接；展示为 `[打开阅读]({readerLink})` |
| `booksimilar.books[].book.bookInfo.deepLink` | 书籍详情跳转链接；没有 `readerLink` 时可展示为 `[查看详情]({deepLink})` |

## 工作流

1. **无参数**：调 `/book/recommend` 获取个性化推荐（为你推荐）。
2. **有 bookId**：调 `/book/similar` 推荐相似书，必须显式传 `count` 和 `maxIdx`；首次推荐 `count=12`、`maxIdx=0`。
3. **有关键词**：调 `/store/search` 搜索发现。
4. 用户对推荐的书感兴趣时，调 `/book/info` 获取完整信息。
5. 翻页（recommend）：用 `searchIdx` 作为下次的 `maxIdx`。
6. 翻页（similar）：用最后一条的 `idx` 作为 `maxIdx`，继续显式传 `count`，带上 `sessionId`。

## 输出格式
- 推荐列表用编号展示，每本书含书名、作者、评分、推荐理由
- 提示用户可选择编号查看详情或继续推荐更多
- 无推荐结果时回复：`暂时没有找到合适的推荐，换个关键词试试？`
- 接口调用失败时回复：`推荐数据获取失败，请稍后再试~`
# notes — 笔记/划线

本文档区分两种口径：

- **统计口径**：笔记数 = 书签数 + 划线数 + 想法/点评数。这里的"想法/点评"对应后端 `reviewCount`，包含划线想法、书评想法/个人点评、书摘、非书籍想法等个人内容。
- **内容导出口径**：当前可导出的单本书笔记内容 = 划线内容 + 想法/点评内容。书签只在统计数量中体现，当前 `/book/bookmarklist` 已过滤书签，不能导出书签内容。

公开的他人点评不属于个人笔记，见 `review.md`。

## 接口

### `/user/notebooks` — 笔记本概览（所有有笔记的书）

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `count` | int | 否 | 每页数量，默认 20 |
| `lastSort` | int | 否 | 翻页游标（上一页最后一条的 `sort` 值） |

**回包：**

| 字段 | 说明 |
|------|------|
| `totalBookCount` | 有笔记的书籍总数 |
| `totalNoteCount` | 笔记总条数，统计口径为 `reviewCount + noteCount + bookmarkCount` 的汇总 |
| `hasMore` | 是否有更多（1=有） |
| `books[].bookId` | 书籍 ID |
| `books[].book` | 书籍信息（title, author, cover 等） |
| `books[].reviewCount` | 想法/点评数：包含划线想法、书评想法/个人点评、书摘、非书籍想法等个人内容 |
| `books[].noteCount` | 划线数（高亮标注的原文条数） |
| `books[].bookmarkCount` | 书签数（标记阅读位置的条数；只作为数量统计，当前不导出书签内容） |
| `books[].readingProgress` | 阅读进度 |
| `books[].markedStatus` | 标记状态（1=读完, 0=在读） |
| `books[].sort` | 排序值（最近笔记时间，用于翻页） |

#### 概念解释
- 用户问“有多少笔记”时，使用统计口径：`reviewCount + noteCount + bookmarkCount`。
- `noteCount` 字段名容易误读：它不是单本书总笔记数，而是划线/高亮原文条数；单本书总笔记数必须自行计算。
- `/user/notebooks` 不返回 `highlightCount` 字段；如果用户或上游说“高亮数/划线数”，对应字段是 `noteCount`。
- `reviewCount` 已包含个人点评/书评想法，因此计算总笔记数时不要再额外加“点评数”，否则会重复计算。
- `/user/notebooks` 概览无法把 `reviewCount` 拆成“划线想法”和“个人点评”的独立数量；如需内容明细，需继续查询 `/review/list/mine`。

#### 分页规则
- `/user/notebooks` 使用基于时间排序值的游标分页，不支持 `offset`/`limit` 分页。
- 第一次请求只传 `count`；如果 `hasMore` 为 1，取本页 `books` 最后一项的 `sort`，下一次作为 `lastSort` 传入。
- 所有业务参数必须平铺在 JSON body 顶层，和 `api_name`、`skill_version` 同级；不要包在 `params` 对象里。
- 不要传 `offset`、`limit`、`start`、`size`；这些参数不会被后端分页逻辑读取，可能导致重复第一页或结果不符合预期。
- 拉取完整列表时循环请求直到 `hasMore` 为 0，再按 `reviewCount + noteCount + bookmarkCount` 计算并降序排序。

#### 分页 few-shot

正确：首页请求，参数平铺。
```json
{"api_name":"/user/notebooks","count":20,"skill_version":"1.0.5"}
```

正确：下一页请求，`lastSort` 取上一页 `books` 最后一项的 `sort`。
```json
{"api_name":"/user/notebooks","count":20,"lastSort":1778312777,"skill_version":"1.0.5"}
```

错误：不要使用 `params` 包裹业务参数，否则后端收不到 `count` 和 `lastSort`。
```json
{"api_name":"/user/notebooks","params":{"count":20,"lastSort":1778312777},"skill_version":"1.0.5"}
```

错误：不要使用 `offset`/`limit`，这些字段不是本接口分页参数。
```json
{"api_name":"/user/notebooks","offset":20,"limit":20,"skill_version":"1.0.5"}
```

### `/book/bookmarklist` — 单本书的划线内容列表（不含书签内容）

> 自动过滤书签（type=0），只返回划线（type=1）。

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bookId` | string | 是 | 书籍 ID |

**回包：**

| 字段 | 说明 |
|------|------|
| `updated` | 划线数组 |
| `updated[].bookmarkId` | 划线唯一 ID |
| `updated[].bookId` | 书籍 ID |
| `updated[].chapterUid` | 所在章节 UID |
| `updated[].markText` | 划线原文 |
| `updated[].createTime` | 创建时间（Unix 时间戳） |
| `updated[].type` | 类型 |
| `updated[].range` | 位置范围 |
| `updated[].colorStyle` | 划线颜色样式 |
| `chapters` | 章节信息数组（用于定位划线所属章节） |
| `chapters[].chapterUid` | 章节 UID |
| `chapters[].chapterIdx` | 章节序号 |
| `chapters[].title` | 章节标题 |
| `book` | 书籍信息 |

### `/review/list/mine` — 单本书的个人想法与点评

> 返回当前用户在该书上的所有个人内容，包括划线想法、章节点评和整本书评。

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bookid` | string | 是 | 书籍 ID |
| `synckey` | int | 否 | 翻页游标，默认 0 |
| `count` | int | 否 | 每页数量，默认 20 |

**回包：**

| 字段 | 说明 |
|------|------|
| `reviews` | 想法/点评数组 |
| `reviews[].review.reviewId` | 唯一 ID |
| `reviews[].review.content` | 内容文本 |
| `reviews[].review.abstract` | 想法对应的划线原文。仅划线想法等能定位到原文的内容有值，整本书评或章节点评可能为空或不存在 |
| `reviews[].review.range` | 划线原文位置范围，格式如 `"2959-3007"`。仅能定位到原文的内容有值 |
| `reviews[].review.chapterUid` | 章节 UID。章节相关内容可能有值 |
| `reviews[].review.chapterIdx` | 章节序号。章节相关内容可能有值 |
| `reviews[].review.createTime` | 创建时间 |
| `reviews[].review.star` | 评分（0-5，-1=无评分） |
| `reviews[].review.chapterName` | 所在章节名（章节点评时有值，书评为空） |
| `reviews[].review.isFinish` | 是否读完（书评时有值） |
| `totalCount` | 总条数 |
| `hasMore` | 是否有更多（1=有） |
| `synckey` | 翻页游标（下次请求传入） |

> `abstract` 和 `range` 是条件字段：如果想法是针对某段划线/原文发表的，应优先用它们展示"原文 + 想法"；如果是整本书评、章节点评或普通想法，可能没有对应原文。

### `/book/underlines` — 章节划线热度统计

> 获取某章节每条划线的热度统计（人数/得分/类型），**不含划线文本**，主要用于阅读器内显示"X人划线"热度标签。

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bookId` | string | 是 | 书籍 ID |
| `chapterUid` | int | 是 | 章节 UID（从 `/book/chapterinfo` 获取） |
| `synckey` | int | 否 | 增量同步 key，默认 0 |

**回包：**

| 字段 | 说明 |
|------|------|
| `bookId` | 书籍 ID |
| `chapterUid` | 章节 UID |
| `underlines` | 划线热度统计数组 |
| `underlines[].range` | 划线位置范围（如 "393-401"） |
| `underlines[].count` | 划线人数 |
| `underlines[].score` | 热度分数 |
| `underlines[].type` | 划线类型 |
| `synckey` | 同步 key |

### `/book/bestbookmarks` — 书籍热门划线

> 获取全书的 Popular Highlights，**包含划线原文和划线人数**，按热度排序。服务端固定返回前 20 条（`count=20, maxIdx=0`），不支持分页。

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bookId` | string | 是 | 书籍 ID |
| `chapterUid` | int | 否 | 章节 UID（0=全部章节，从 `/book/chapterinfo` 获取），默认 0 |
| `synckey` | int | 否 | 增量同步 key，默认 0 |

**回包：**

| 字段 | 说明 |
|------|------|
| `synckey` | 同步 key（数据版本号） |
| `totalCount` | 热门划线总数 |
| `items` | 热门划线数组 |
| `items[].bookId` | 书籍 ID |
| `items[].userVid` | 代表用户 VID |
| `items[].bookmarkId` | 划线唯一 ID |
| `items[].chapterUid` | 所在章节 UID |
| `items[].range` | 划线位置范围（如 "393-401"） |
| `items[].markText` | 划线原文文本 |
| `items[].totalCount` | 划线人数 |
| `items[].simplifiedRange` | 简体书籍的 range（繁简体书专属） |
| `items[].traditionalRange` | 繁体书籍的 range（繁简体书专属） |
| `chapters` | 章节信息数组（用于定位划线所属章节） |
| `chapters[].bookId` | 书籍 ID |
| `chapters[].chapterUid` | 章节 UID |
| `chapters[].chapterIdx` | 章节序号 |
| `chapters[].title` | 章节标题 |

### `/book/readreviews` — 划线下的想法/评论

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bookId` | string | 是 | 书籍 ID |
| `chapterUid` | int | 是 | 章节 UID |
| `reviews` | array | 是 | 要查询的划线范围数组 |
| `reviews[].range` | string | 是 | 划线位置范围（从 `/book/bestbookmarks` 获取） |
| `reviews[].maxIdx` | int | 否 | 翻页偏移，默认 0 |
| `reviews[].count` | int | 否 | 每页数量，服务端上限 20，超过自动截断 |
| `reviews[].synckey` | int | 否 | 翻页游标，默认 0 |

**回包：**

| 字段 | 说明 |
|------|------|
| `bookId` | 书籍 ID |
| `chapterUid` | 章节 UID |
| `reviews` | 每个 range 的想法列表 |
| `reviews[].range` | 划线范围 |
| `reviews[].totalCount` | 该范围下想法总数 |
| `reviews[].hasMore` | 是否有更多（1=有） |
| `reviews[].maxIdx` | 翻页偏移 |
| `reviews[].synckey` | 翻页游标 |
| `reviews[].pageReviews` | 想法数组 |
| `reviews[].pageReviews[].reviewId` | 想法 ID |
| `reviews[].pageReviews[].review` | 想法详情对象 |
| `reviews[].pageReviews[].review.abstract` | 划线原文（想法对应的划线内容） |
| `reviews[].pageReviews[].review.content` | 想法内容 |
| `reviews[].pageReviews[].review.range` | 划线位置范围 |
| `reviews[].pageReviews[].review.createTime` | 创建时间 |
| `reviews[].pageReviews[].review.author` | 作者信息 |

### `/review/single` — 单条想法详情

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `reviewId` | string | 是 | 想法/评论 ID |
| `commentsCount` | int | 否 | 拉取评论数量，默认 10 |
| `commentsDirection` | int | 否 | 评论排序方向：0=倒序, 1=正序 |
| `likesCount` | int | 否 | 拉取点赞数量，默认 10 |
| `likesDirection` | int | 否 | 点赞排序方向：0=倒序 |
| `synckey` | int | 否 | 增量同步 key，默认 0 |

**回包：**

| 字段 | 说明 |
|------|------|
| `reviewId` | 想法 ID |
| `review` | 想法详情对象（content, bookId, chapterUid, createTime, author 等） |
| `htmlContent` | 富文本内容 |
| `synckey` | 同步 key |

## 工作流

1. **无参数/问笔记数量排行**：调 `/user/notebooks` 展示笔记本概览；如需完整排行，必须按 `count` + `lastSort` 遍历到 `hasMore=0`，且所有分页参数平铺在 body 顶层；每本书笔记数按 `reviewCount + noteCount + bookmarkCount` 计算并排序。
2. **有 bookId 或书名，问单本书笔记内容**：同时调 `/book/bookmarklist`（划线内容）和 `/review/list/mine`（想法/点评内容），合并展示当前可导出的笔记内容。
3. **明确要求书签内容**：说明当前接口只在 `/user/notebooks` 提供书签数量，不能导出书签内容；不要把划线误当书签。
4. 用户从概览中选择某本书后，同样调上述两个接口。
5. 通过 `chapters` 中的 `chapterUid`/`title` 将划线按章节分组。
6. 翻页（notebooks）：只使用顶层平铺的 `count` + `lastSort` 游标分页；`hasMore` 为 1 时，用最后一条的 `sort` 值作为下一页 `lastSort`；禁止使用 `params` 嵌套或 `offset`/`limit`。
7. **查看书籍热门划线及想法**：
   - 调 `/book/bestbookmarks` 获取热门划线列表（含划线原文和人数）
   - 调 `/book/underlines` 获取章节内划线热度统计（人数/得分，无文本，用于展示"X人划线"标签）
   - 用 `/book/bestbookmarks` 返回的 `range` 值调 `/book/readreviews` 获取每条划线下的想法
   - 如需查看单条想法完整详情（含评论/点赞），调 `/review/single`

## 输出格式
- 笔记本概览：编号列表，每本书显示书名、作者、总笔记数、想法/点评数、划线数、书签数、阅读进度
- 单本笔记内容：按章节分组展示当前可导出的内容
  - 划线：用引用格式 `>` 标注原文
  - 想法/点评：区分划线想法、章节点评、整本书评；能关联划线时放在对应划线下方，不能关联时单独列出
  - 书签：只展示数量（来自 `/user/notebooks` 的 `bookmarkCount`），不展示内容

## 概念理清

- **统计笔记数 = `reviewCount + noteCount + bookmarkCount`**；不要把 `noteCount` 单独当作总笔记数。
- **内容导出 = 划线内容 + 想法/点评内容**；当前不能导出书签内容。
- `reviewCount` 已包含个人点评/书评想法，计算总笔记数时不要再额外加“点评数”。
- 当用户说“所有笔记内容”时，必须同时查询 `/book/bookmarklist` 和 `/review/list/mine`，不能只返回划线。
# profile — 用户信息与阅读统计

## 说明

通过组合 `/shelf/sync`、`/book/getprogress`、`/user/notebooks` 获取用户阅读概况。

## 核心约束

1. 所有回复必须基于接口返回数据，不编造、不推断。
2. 禁止输出中间推理过程，不暴露接口选择、参数拼装等内部过程。
3. 书架数量必须按 `books.length + albums.length + (mp 非空 ? 1 : 0)` 计算；`albums[]` 是专辑/有声书，也属于书架里的书，不能只统计 `books[]`。
4. 阅读进度只查最近 5 本电子书：从 `books[]` 按 `readUpdateTime` 降序取前 5 本，逐个调 `/book/getprogress`，避免大书架导致过多调用。
5. 阅读时长字段单位为秒，展示时转为"X小时Y分钟"格式；Unix 时间戳展示为 `YYYY-MM-DD`。
6. 展示书籍时，优先将回包中的 `readerLink` 展示为 `[打开阅读]({readerLink})`；没有 `readerLink` 但有 `deepLink` 时，展示为 `[查看详情]({deepLink})`；不要手动拼接链接。

## 工作流

### 1. 获取书架
调 `/shelf/sync`，了解用户在读什么书、总数等。
书架数量必须按 `books.length + albums.length + (mp 非空 ? 1 : 0)` 计算；`albums[]` 是专辑/有声书，也属于书架里的书，不能只统计 `books[]`。
具体逻辑参考 `shelf.md`。

### 2. 获取阅读进度
从 `books[]` 中按 `readUpdateTime` 降序取最近阅读的前 5 本书，分别调 `/book/getprogress` 获取进度和累计阅读时长，具体见 `book.md`。

注意：
- 只对 `books[]` 中的电子书调 `/book/getprogress`，不要对 `albums[]` 专辑/有声书调用该接口。
- `book.progress` 是 0-100 的整数，展示时必须带 `%`；只有 `progress=100` 且存在 `finishTime` 时才表示已读完。
- `book.recordReadingTime` 是累计阅读时长，单位为秒。

### 3. 获取笔记
调 `/user/notebooks` 获取笔记概览，展示有笔记的书籍数和总笔记数。这里只做概览，不导出单本书笔记内容。

如果用户要查看某本书的具体笔记内容，再按 `notes.md` 调 `/book/bookmarklist` 和 `/review/list/mine`。

### 4. 综合展示
汇总书架总数、最近阅读进度和笔记概况。

## 输出格式
- 无参数时展示阅读概况：书架总数 + 最近阅读的前 5 本进度 + 笔记概况。
- 书架总数第一句给出可见条目数，并拆分电子书、专辑/有声书、文章收藏入口数量。
- 每本书显示：书名、作者、进度百分比、累计阅读时长、最近阅读时间；优先附 `[打开阅读]({readerLink})`，没有 `readerLink` 时可附 `[查看详情]({deepLink})`。
- 笔记概况显示：有笔记的书籍数、总笔记数。
- 书架为空时回复：`你的书架还没有书哦，要不要去发现页看看推荐？`
- 接口调用失败时回复：`阅读概况暂时无法获取，请稍后再试~`
# readdata — 阅读统计

查看个人阅读数据统计，包含阅读时长、天数、读书排行、偏好分析等。

> **⚠️ 使用前必须阅读本文件字段说明。** 阅读统计字段容易因字段名产生误判，尤其是所有阅读时长字段的单位。调用 `/readdata/detail` 前必须先确认本文件中的参数、字段单位和统计口径；禁止凭字段名或数值大小推断单位。

## 接口

### `/readdata/detail` — 阅读统计详情

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `mode` | string | 否 | 统计维度：`weekly`=本周, `monthly`=本月, `annually`=本年, `overall`=总计。默认 `monthly`。|
| `baseTime` | int | 否 | 基准时间戳（0=当前周期），此时服务端会归一化到周期起点：周一、月初、年初；`overall` 固定为 0。传历史时间戳可查看该时间戳所在周期的数据；`annually` 只返回 `baseTime` 所在自然年的数据，不会自动包含后续年份 |

**回包字段说明（字段按 `mode` 和数据条件可选返回）：**

| 字段 | 说明 |
|------|------|
| `baseTime` | 统计周期的基准时间戳：`weekly` 为周一 00:00，`monthly` 为月初 00:00，`annually` 为年初 00:00，`overall` 为 0 |
| `readTimes` | 分桶阅读/收听总时长（对象，key 为分桶起始时间戳，value 为秒数）。`weekly`/`monthly` 通常按天分桶，`annually` 按月分桶，`overall` 按年分桶 |
| `dailyReadTimes` | 年度模式可能返回的每日阅读时长明细（对象，key 为日期时间戳，value 为秒数）；用于日历明细展示，不应替代 `totalReadTime` 作为总量口径 |
| `readDays` | 有效阅读天数。服务端按有效阅读规则计算，当前规则为单日阅读满 1 分钟 |
| `totalReadTime` | 当前请求周期的总阅读/收听时长（**秒**）。统计总时长时优先使用该字段，`readTimes` 仅用于明细展示或交叉校验；**禁止误当成分钟或小时** |
| `dayAverageReadTime` | 日均阅读/收听时长（秒），分母是当前周期已过去的自然日数或历史完整周期自然日数，不是 `readDays` |
| `compare` | 与上一周期的日均时长对比比例；正数表示增长，负数表示下降。该字段只在当前周期且上一周期数据足够时返回，`0.2` 表示约增长 20% |
| `readLongest` | 读得最多的书/有声内容排行数组，最多 10 条，按 `readTime` 降序；低于 5 分钟的条目会被过滤 |
| `readLongest[].book` | 书籍信息对象（电子书/出版书），包含 `bookId`、`title`、`author`、`cover` 等 |
| `readLongest[].albumInfo` | 有声内容信息对象；当排行条目是有声书/专辑时返回 |
| `readLongest[].readTime` | 该书或有声内容在当前统计范围内的阅读/收听时长（秒） |
| `readLongest[].recordReadingTime` | 该书的朗读/记录类阅读时长（秒），存在时才返回 |
| `readLongest[].tags` | 标签数组，目前常见值包括 `笔记最多`、`单日阅读最久` |
| `readStat` | 阅读统计摘要数组 |
| `readStat[].stat` | 统计项名称，常见为 `读过`、`读完`、`阅读`、`笔记` |
| `readStat[].counts` | 统计值文案，如 `12本`、`45天`、`120条` |
| `readStat[].scheme` | 对应统计项的 App 跳转链接，可能为空 |
| `preferCategory` | 偏好阅读分类数组，最多 8 个；不足时可能补充默认分类占位 |
| `preferCategory[].categoryId` | 分类 ID |
| `preferCategory[].categoryTitle` | 分类名称 |
| `preferCategory[].parentCategoryId` | 父分类 ID |
| `preferCategory[].parentCategoryTitle` | 父分类名称 |
| `preferCategory[].val` | 分类偏好权重，按最高分类阅读时长归一化后的相对值，用于图表展示 |
| `preferCategory[].readingTime` | 该分类阅读时长（秒） |
| `preferCategory[].readingCount` | 该分类阅读本数 |
| `preferCategory[].categoryType` | 分类类型标记，普通分类为 0，部分特殊分类会返回 1 或 2 |
| `preferCategoryWord` | 偏好分类文案，如 `偏好阅读文学`；年度报告场景可能改为固定文案 `偏好阅读` |
| `preferTime` | 24 小时阅读时段分布数组，值为秒数。注意输出顺序从 6 点开始，依次到次日 5 点，不是从 0 点开始 |
| `preferTimeWord` | 偏好时段文案。总偏好时段数据不足 10 小时时可能不返回；常见文案如 `偏好上午阅读`、`偏好白天阅读`、`偏好夜间阅读`、`汲取新知，昼夜不倦` |
| `preferAuthor` | 偏好作者数组。只有作者数据达到展示阈值时返回 |
| `preferAuthor[].authorId` | 作者 ID |
| `preferAuthor[].name` | 作者名 |
| `preferAuthor[].count` | 阅读该作者的书本数 |
| `preferAuthor[].readTime` | 阅读该作者作品的时长，格式化字符串，如 `5小时30分钟`，不是秒数 |
| `preferAuthor[].user` | 作者关联用户信息，存在时返回 |
| `authorCount` | 符合统计条件的作者总数，不一定等于 `preferAuthor` 返回条数 |
| `preferPublisher` | 偏好出版社数组。至少 3 个出版社且最高出版社阅读本数达到阈值时返回 |
| `preferPublisher[].name` | 出版社名 |
| `preferPublisher[].count` | 阅读该出版社书籍的本数 |
| `preferCp` | 偏好版权方数组。满足展示阈值时返回 |
| `preferCp[].count` | 阅读该版权方书籍的本数 |
| `preferCp[].copyrightInfo` | 版权方信息，包括名称、用户 VID、头像、角色等 |
| `readRate` | 文字阅读占比百分比，计算口径约为 `wrReadTime / (wrReadTime + wrListenTime) * 100`。当总时长不足 1 小时或文字阅读占比过高时不返回 |
| `wrReadTime` | 文字阅读时长（秒），通常为 `totalReadTime - wrListenTime`；仅在 `readRate` 可展示时返回 |
| `wrListenTime` | 听书/TTS/有声内容时长（秒）；仅在 `readRate` 可展示时返回 |
| `rank` | 本周好友阅读排行信息；仅当前周且未隐藏排行时返回 |
| `rank.text` | 排行文案，如 `朋友中排第3名` |
| `rank.scheme` | 排行跳转链接 |
| `registTime` | 用户注册时间戳 |
| `medals` | 勋章数组；可展示勋章不少于 3 个时返回 |
| `preferBooks` | 偏好阅读书籍卡片数组，包含书籍、推荐理由和偏好类型等信息 |
| `yearReport` | 年度报告入口数组。`overall` 可能返回多年的入口，`annually` 可能返回当前年份入口；`times` 为该年 12 个月阅读/收听时长数组 |
| `recordReadingTime` | 总朗读/记录类阅读时长（秒），目前主要在 `overall` 模式下汇总返回 |
| `readRecordsWord` | 书籍分布模块标题文案，当前固定为 `书籍分布` |
| `readDistributionWord` | 点评分布模块标题文案，当前固定为 `点评分布` |
| `readTimeGears` | 阅读时长档位数组，当前为 `[60, 1800, 3600, 10800, 18000]`，用于前端展示分段 |
| `styleType` | 样式类型，常见为 `normal`；年度报告场景可能返回特殊样式 |

> 年度报告相关字段（如 `annualList2023`、`preferBooks2023`、2025 年报模块字段等）会随活动配置变化，不作为通用阅读统计字段依赖。

## 周期特点与区间组合

`/readdata/detail` 只支持按固定自然周期查询，不支持直接传任意起止日期。遇到"某天至今"、"某月中旬到现在"、"跨年区间"这类请求时，应通过多个固定周期结果组合计算。

| mode | 周期粒度 | baseTime 行为 | 适合用途 |
|------|----------|---------------|----------|
| `weekly` | 自然周 | 归一到该周周一 00:00 | 本周、某历史周 |
| `monthly` | 自然月 | 归一到该月 1 日 00:00 | 本月、某历史月、区间边界扣减 |
| `annually` | 自然年 | 归一到该年 1 月 1 日 00:00 | 某年全年、今年至今、跨年区间拼接 |
| `overall` | 全部历史 | 固定为 0 | 总计，不适合拆任意日期区间 |

**组合原则：**

1. 优先用较大周期减少调用次数：整年用 `annually`，整月用 `monthly`。
2. 跨年区间按自然年拆分：历史整年 + 当前年至今。
3. 起点落在年/月中间时，可用"大周期 - 起点之前的完整小周期"近似组合；如果接口返回 `dailyReadTimes`，可对边界日期做日级精确扣减。
4. **完整周期**使用该周期回包的 `totalReadTime`；**不完整边界周期**优先使用 `dailyReadTimes` 精确扣除起点前/终点后的日期。若没有日级明细，只能使用月级/年级近似，并在回答中说明口径。
5. 不要把截断展示的 `readTimes` 当作主结果；`readTimes` 仅用于明细展示或交叉校验。

**Few-shot：**

- 用户问："2024 年 1 月 31 日至今，我的总阅读时长是多少？"
  - 推荐做法：查询 `2024` 至当前年份的 `annually`，累加年度 `totalReadTime`；再查询 `2024-01` 的 `monthly`，从总和中扣除 2024 年 1 月的 `totalReadTime`，得到近似的 `2024-02-01 至今` 口径。
  - 若年度返回 `dailyReadTimes` 且需要精确到 1 月 31 日，则只扣除 `2024-01-01` 至 `2024-01-30` 的日级时长，保留 1 月 31 日。
- 用户问："2025 年以来读了多久？"
  - 查询 `mode=annually`，`baseTime` 取 2025 年内任一时间戳；如果当前年份大于 2025，再继续查询后续每个自然年并累加。
- 用户问："去年 3 月到今年 2 月读了多久？"
  - 查询去年 3-12 月各月 `monthly`，再查询今年 1-2 月各月 `monthly`，累加 `totalReadTime`。

## 工作流

1. **默认**：调 `/readdata/detail`，不传参数使用默认 `mode=monthly` 展示本月阅读数据。
2. **用户问本周/今年/总共**：对应传 `mode=weekly`/`annually`/`overall`。
3. **用户问历史数据**：如"上个月读了多少"，将上月某天的时间戳作为 `baseTime` 传入；如"2025 年读了多久"，传 `mode=annually` 且 `baseTime` 取 2025 年内任一时间戳。
4. **用户问跨年区间**：如"2024 年至今""2025 年以来"，必须按自然年逐年查询：从起始年份到当前年份分别调用 `mode=annually`，每次 `baseTime` 取该年份内时间戳；历史年份返回的是该自然年全年数据，当前年份返回的是本年至今数据。不要把 `2025` 年度结果标注为"2025 年至今"，也不要漏查当前年份。
5. **用户问任意起止日期区间**：先判断是否能拆成完整自然年/月/周；完整周期使用 `totalReadTime` 累加，不完整边界优先使用 `dailyReadTimes` 做日级扣减；如果没有日级明细，则使用月级近似并说明口径。例如"2024 年 1 月 31 日至今"可用 2024 年至今的年度数据合计，减去 2024 年 1 月月度数据，得到 `2024-02-01 至今` 口径；若有日级明细，则只扣除 1 月 1-30 日，保留 1 月 31 日。
6. **总时长口径**：单个完整周期优先采用回包 `totalReadTime`；跨周期区间按"完整周期 `totalReadTime` 累加/相减 + 边界周期 `dailyReadTimes` 日级修正"计算。不要手动把截断输出里的 `readTimes` 相加作为主结果；回答时明确标注使用了哪些完整周期，以及是否使用了日级边界扣减或月级近似。
7. **日均口径**：`dayAverageReadTime` 是按自然日平均，不是按阅读天数平均；如果需要“阅读日均”，必须说明该字段不是接口直接返回值，需要用 `totalReadTime / readDays` 另行计算。
8. 综合展示：总时长、阅读天数、自然日均时长、与上期对比，读得最多的书，偏好分类和作者。

## 输出格式

- **总览**：阅读天数、总时长（转为 x 小时 y 分钟）、自然日均时长、与上期对比（增长/下降百分比）
- **读书排行**：列出读得最多的书/有声内容，书名或专辑名 + 阅读/收听时长
- **阅读统计**：读过本数、读完本数、阅读天数、笔记数等
- **偏好分析**：偏好分类、偏好时段、偏好作者、偏好出版社/版权方（如有）
- 时长单位统一转换：所有阅读时长字段均按秒处理，秒 → "x 小时 y 分钟"格式；不得把 `totalReadTime` 当成分钟或小时
- 接口调用失败时回复：`阅读数据暂时无法获取，请稍后再试~`
# review — 书籍点评

书籍的公开点评（区别于个人笔记/划线，个人笔记见 `notes.md`）。

## 核心约束

1. 所有回复必须基于接口返回数据，不编造、不推断。
2. 公开点评不属于个人笔记，是其他读者对书籍的评价；个人笔记/划线见 `notes.md`。
3. 评分转换：20=一星，40=二星，60=三星，80=四星，100=五星。
4. 禁止输出中间推理过程，不暴露接口选择、参数拼装等内部过程。

## 接口

### `/review/list` — 书籍公开点评

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bookId` | string | 是 | 书籍 ID |
| `reviewListType` | int | 否 | 筛选类型：0=全部, 1=推荐, 2=不行, 3=最新, 4=一般。默认 0 |
| `count` | int | 否 | 每页数量，默认 20 |
| `maxIdx` | int | 否 | 翻页偏移，默认 0 |
| `synckey` | int | 否 | 翻页游标，默认 0 |

**回包（经裁剪）：**

| 字段 | 说明 |
|------|------|
| `synckey` | 翻页游标（下次请求传入） |
| `reviewsCnt` | 点评总数 |
| `recentTotalCnt` | 最新点评数 |
| `reviewsHasMore` | 是否有更多点评（1=有） |
| `reviewsHas5Star` | 是否有五星推荐点评（1=有） |
| `reviewsHas1Star` | 是否有一星差评（1=有） |
| `reviewsHasRecent` | 是否有最新点评（1=有） |
| `friendCommentCount` | 好友点评数 |
| `friendUniqueCount` | 点评好友数 |
| `friendCommentUsers` | 点评好友信息数组 |
| `friendCommentUsers[].userVid` | 好友 vid |
| `friendCommentUsers[].name` | 好友昵称 |
| `friendCommentUsers[].avatar` | 好友头像 |
| `deepVRecommendInfo` | 资深会员推荐摘要 |
| `deepVRecommendInfo.title` | 如"2337 个资深会员点评" |
| `deepVRecommendInfo.subtitle` | 如"其中 2015 人(86.2%)推荐本书" |
| `deepVRecommendValue` | 资深会员推荐比例（862 = 86.2%） |
| `deepVUniqueCount` | 点评资深会员数 |
| `reviews` | 点评数组 |
| `reviews[].idx` | 序号（用于翻页，下次 maxIdx 传最后一条的 idx） |
| `reviews[].review.reviewId` | 点评唯一 ID |
| `reviews[].review.review.content` | 点评文本内容 |
| `reviews[].review.review.htmlContent` | 点评 HTML 内容（富文本） |
| `reviews[].review.review.star` | 评分（20=一星, 40=二星, 60=三星, 80=四星, 100=五星） |
| `reviews[].review.review.isFinish` | 是否读完此书 |
| `reviews[].review.review.createTime` | 创建时间 |
| `reviews[].review.review.chapterName` | 所在章节名（章节点评时有值） |
| `reviews[].review.review.author.userVid` | 评论者 vid |
| `reviews[].review.review.author.name` | 评论者昵称 |
| `reviews[].review.review.author.avatar` | 评论者头像 |
| `reviews[].review.review.book.bookId` | 书籍 ID |
| `reviews[].review.review.book.title` | 书名 |
| `reviews[].review.review.book.author` | 书籍作者 |

> 注意：返回结构中存在双层 `review` 嵌套。`reviews[].review` 是列表条目包装对象；点评内容字段（如 `content`、`htmlContent`、`star`、`author`、`book`）位于内层 `reviews[].review.review.xxx`。

## 工作流

1. 确定书籍：用户提供 bookId 直接使用，提供书名则先调 `/store/search` 获取 bookId。
2. 调 `/review/list` 获取公开点评列表。
   - 默认 `reviewListType=0` 看全部
   - 用户要看推荐的传 `reviewListType=1`
   - 用户要看最新的传 `reviewListType=3`
   - 用户要看差评的传 `reviewListType=2`
   - 用户要看一般的传 `reviewListType=4`
3. 每条点评展示：评论者昵称、评分星级、点评内容（长内容截取摘要）。
4. 翻页：用上一页最后一条的 `idx` 作为 `maxIdx`，带上 `synckey`。

## 输出格式
- 点评列表每条清晰分隔
- 评分转为星级展示（100=⭐⭐⭐⭐⭐，80=⭐⭐⭐⭐，60=⭐⭐⭐，40=⭐⭐，20=⭐）
- 长点评截取前 200 字，提示可展开
- 时间戳展示时转为 `YYYY-MM-DD`，不要直接展示原始 Unix 时间戳
- 无结果时回复：`这本书暂时还没有公开点评哦~`
- 接口调用失败时回复：`点评数据获取失败，请稍后再试~`
# search — 搜索

支持多种搜索类型，通过 `scope` 参数切换 tab，来指定不同的搜索结果 tab 页面。

## 核心约束

1. 所有回复必须基于接口返回数据，不编造、不推断、不补充接口未返回的信息。
2. `scope` 选择必须基于用户意图，不要默认全部使用 `scope=10`。
3. 始终显式传 `scope`，不要依赖服务端默认值。
4. 禁止输出中间推理过程，不要在回复中暴露 scope 选择逻辑、参数拼装思路等内部过程。
5. 搜索结果是分页片段，不代表全量结果；回复中使用"为您找到"，不要使用"共有""一共""总共"等暗示结果完整的措辞。
6. 请求参数 `scope` 和回包字段 `results[].scope` 不是同一个语义：找书时仍传 `scope=10`，但电子书分组回包可能是 `results[].scope=17`；不要用 `results[].scope == 10` 过滤电子书结果。

## 接口

`/store/search`

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keyword` | string | 是 | 搜索关键词 |
| `scope` | int | 否 | 搜索类型。接口层可省略，但 Agent 必须按下方“scope 选择指引”显式选择；未传时服务端默认 10（电子书） |
| `maxIdx` | int | 否 | 翻页偏移，默认 0 |
| `count` | int | 否 | 每页数量，不传则服务端默认 15。用户未指定数量时不要传此参数 |

**scope 对应关系：**

| scope | 名称 | 说明 |
|-------|------|------|
| `0` | 全部 | 综合搜索，results 中包含多个分组；适合用户只说“搜一下”且未限定类型 |
| `10` | 电子书 | 只搜电子书（不含网文小说）；适合用户明确“搜书/找书/搜某本书” |
| `16` | 网文小说 | 只搜网文小说 |
| `14` | 微信听书 | 有声书/专辑/播客（三者同义） |
| `6` | 作者 | 搜索作者 |
| `12` | 全文 | 搜索书籍正文内容 |
| `13` | 书单 | 搜索书单 |
| `2` | 公众号 | 搜索公众号 |
| `4` | 文章 | 搜索公众号文章 |

> `scope=17` 是服务端回包中电子书分组常见的加载/分页标识，不是 Agent 的首选请求参数。用户找书时仍按 `scope=10` 请求。

**scope 选择指引（Agent 根据用户意图自动选择）：**
- 用户明确说"搜书""找书""查某本书"或请求获取 bookId → `scope=10`（电子书）
- 用户只说"搜一下 xx"，未说明要搜书/作者/文章/公众号等具体类型 → `scope=0`（全部）
- 用户说"网文""网络小说" → `scope=16`（网文小说）；如果只是普通语义中的"小说"且想找书，仍用 `scope=10`
- 用户说"听书""有声书""播客""专辑" → `scope=14`
- 用户说"搜一下 xx 作者""查作者 xx" → `scope=6`
- 用户说"书里提到了 xx""全文搜索" → `scope=12`
- 用户说"有什么书单""推荐书单" → `scope=13`
- 用户说"搜公众号" → `scope=2`
- 用户说"搜文章" → `scope=4`
- 不要把"没特别指定"同时解释成 `scope=10` 和 `scope=0`；判断标准是：有明确找书意图用 `scope=10`，泛搜索用 `scope=0`。

## 参数提取规则

从用户输入中提取 `keyword` 时：

1. 去掉"帮我""搜一下""找一下""有没有""请问"等口语化前缀/后缀，只保留核心检索词。
2. 保留真正要搜索的实体或主题：
   - "帮我搜一下三体" → `keyword=三体`
   - "有没有刘慈欣的书" → `keyword=刘慈欣`
   - "找一本关于量子力学的入门书" → `keyword=量子力学入门`
3. 用户使用"这个作者""他的其他书"等代词时，结合对话上下文补全为实际实体名称再搜索。
4. 同时提到书名和作者时，优先使用更具区分度的词作为 `keyword`，如"刘慈欣的三体"优先搜 `三体`。

**回包（V3 格式）：**

| 字段 | 说明 |
|------|------|
| `sid` | 搜索会话 ID |
| `hasMore` | 是否有更多（1=有, 0=无） |
| `results` | 搜索结果分组数组 |
| `results[].title` | 分组标题（如"电子书""作者"） |
| `results[].scope` | 回包分组类型，不保证等于请求参数 `scope`。例如请求 `scope=10` 搜电子书时，电子书分组可能返回 `scope=17` |
| `results[].scopeCount` | 该分组总结果数 |
| `results[].currentCount` | 本次返回数量 |
| `results[].books` | 书籍/结果数组 |
| `results[].books[].searchIdx` | 搜索序号（用于翻页） |
| `results[].books[].bookInfo` | 书籍信息对象 |
| `results[].books[].bookInfo.bookId` | 书籍唯一标识 |
| `results[].books[].bookInfo.readerLink` | 阅读器跳转链接；展示为 `[打开阅读]({readerLink})` |
| `results[].books[].bookInfo.deepLink` | 书籍详情跳转链接；没有 `readerLink` 时可展示为 `[查看详情]({deepLink})` |
| `results[].books[].bookInfo.title` | 书名 |
| `results[].books[].bookInfo.author` | 作者 |
| `results[].books[].bookInfo.cover` | 封面图 URL |
| `results[].books[].bookInfo.intro` | 书籍简介 |
| `results[].books[].bookInfo.publisher` | 出版社 |
| `results[].books[].bookInfo.category` | 分类 |
| `results[].books[].bookInfo.payType` | 付费类型 |
| `results[].books[].bookInfo.price` | 价格（分） |
| `results[].books[].bookInfo.soldout` | 是否下架 |
| `results[].books[].readingCount` | 在读人数 |
| `results[].books[].newRating` | 评分（0-100） |
| `results[].books[].newRatingCount` | 评分人数 |
| `results[].books[].newRatingDetail` | 评分标签（如 `{"title":"神作"}` ） |

> `scope=0`（全部）时 results 会返回多个分组（电子书、作者、书单等），每个分组有自己的 title 和 scope。展示时按回包内容处理，不要把请求 scope 当作分组过滤条件。

## 工作流

1. 根据用户意图选择 `scope`，调 `/store/search`，并显式传入 `scope`。
2. 从 `results` 取搜索结果。单 tab 模式（scope>0）可能返回多个同类分组；全部模式（scope=0）有多个分组。
3. 展示结果：书名、作者、评分、在读人数、分类。已下架（soldout=1）需标注；如有 `readerLink`，展示为 `[打开阅读]({readerLink})`；否则如有 `deepLink`，展示为 `[查看详情]({deepLink})`。
4. 用户选择某本书后，调 `/book/info` 获取完整信息。
5. 翻页：`hasMore` 为 1 时，用最后一条的 `searchIdx` 作为下一页的 `maxIdx`。

### 结果处理细则

- 用户找书时请求 `scope=10`；回包中标题为"电子书"或包含 `books` 的分组都可以展示，不要要求 `results[].scope == 10`。

## 输出格式
- 搜索结果用编号列表展示，方便用户通过数字选择
- scope=0 时按分组标题（电子书/作者/书单…）分区展示
- 重点展示：书名、作者、评分、在读人数、分类
- 空结果（`results` 为空数组或无匹配项）时回复：`抱歉，没有找到与"{keyword}"相关的结果。你可以换个关键词、检查错别字，或尝试更简短的关键词。`
- 接口调用失败时回复：`搜索服务暂时不可用，请稍后再试。如果持续出现问题，可以换个关键词尝试。`
# shelf — 书架管理

## 重要概念

**专辑 = 有声书**，两者是同一概念。微信读书中，有声书/听书内容以"专辑"形式存在，存放在书架的 `albums` 字段中，与 `books`（电子书）完全独立。

**书架里的“书”包含电子书和专辑/有声书。** 当用户问“我的书架里有多少本书”“书架有多少本”“书架总数”时，不能只数 `books[]`，必须同时计入 `albums[]`。

常见错误：
- ⚠️ **不要**通过遍历 `books` 逐个调 `/book/info` 检查 `format` 来判断有声书——`/book/info` 不返回 format 字段，且效率极低。直接使用 `albums` 字段即可。
- ⚠️ 书架数量必须用实际返回数组计算，且必须包含 `albums[]`；不要只用 `books.length` 回答“书架里有多少本书”。
- ⚠️ 公开/私密阅读数量也必须遍历实际返回条目，不能使用任何未出现在数组中的补丁项。

## 接口

`/shelf/sync`

**请求参数：** 无（用户身份通过 API Key 自动识别）

**回包：**

| 字段 | 说明 |
|------|------|
| `books[]` | 可枚举的电子书/导入书/公众号类书籍条目数组，不含 `albums[]`，也不含 `mp` 文章收藏入口 |
| `books[].bookId` | 书籍唯一标识 |
| `books[].readerLink` | 阅读器跳转链接；展示为 `[打开阅读]({readerLink})` |
| `books[].deepLink` | 书籍详情跳转链接；没有 `readerLink` 时可展示为 `[查看详情]({deepLink})` |
| `books[].title` | 书名 |
| `books[].author` | 作者 |
| `books[].cover` | 封面图 URL |
| `books[].category` | 分类 |
| `books[].readUpdateTime` | 最近阅读时间（Unix 时间戳） |
| `books[].finishReading` | 是否读完（1=读完） |
| `books[].updateTime` | 书籍更新时间 |
| `books[].isTop` | 是否置顶 |
| `books[].secret` | 是否私密（1=私密） |
| `albums[]` | 专辑/有声书数组（与 books 完全独立） |
| `albums[].albumInfo.albumId` | 专辑唯一标识 |
| `albums[].albumInfo.name` | 专辑名称 |
| `albums[].albumInfo.authorName` | 演播/作者 |
| `albums[].albumInfo.cover` | 封面图 URL |
| `albums[].albumInfo.trackCount` | 音频集数 |
| `albums[].albumInfo.finishStatus` | 完结状态（如"已完结"） |
| `albums[].albumInfo.finish` | 是否完结（1=完结） |
| `albums[].albumInfo.payType` | 付费类型 |
| `albums[].albumInfo.intro` | 专辑简介 |
| `albums[].albumInfo.updateTime` | 更新时间（Unix 时间戳） |
| `albums[].albumInfoExtra.secret` | 是否私密 |
| `albums[].albumInfoExtra.lecturePaid` | 是否已购买（1=已购买） |
| `albums[].albumInfoExtra.lectureReadUpdateTime` | 最近收听时间 |
| `albums[].albumInfoExtra.isTop` | 是否置顶 |
| `mp` | 文章收藏入口对象；只表示“文章收藏”目录入口，不包含具体文章内容；非空时表示书架界面有 1 个“文章收藏”条目，不包含在 `books[]`/`albums[]` 中 |
| `archive[].name` | 书单名称 |
| `archive[].bookIds` | 书单内的 bookId 列表 |
| `bookCount` | 可枚举电子书数量，通常等于 `books[].length`；不含 `albums[]` 和 `mp` |

## 数量口径

| 用户问题/指标 | 正确计算方式 | 说明 |
|------|------|------|
| 书架界面有多少本/多少条目 | `books.length + albums.length + (mp 非空 ? 1 : 0)` | 默认回答这个口径；用户说“书架里的书”时也包含专辑/有声书 |
| 电子书数 | `bookCount` 或 `books.length` | 仅 `books[]`，不含专辑和文章收藏；只有用户明确问“电子书”时才用这个口径 |
| 有声书/专辑数 | `albums.length` | 专辑按有声书管理，也是书架总数的一部分 |
| 是否有文章收藏 | `mp 非空 ? 1 : 0` | `mp` 是单独入口，但其中不包含文章收藏的具体内容 |

**⚠️ 强制回答规则**：当用户问任何书架数量问题时，必须使用实际可枚举数组计算：`books.length + albums.length + (mp 非空 ? 1 : 0)`。其中 `albums.length` 必须计入，因为专辑/有声书在书架里也按“书”管理。不要使用其他服务端内部计数字段或基于内部计数字段的公式。

### Few-shot：正确计算书架总数

**例 1：有电子书和专辑，无文章收藏**

回包关键信息：
- `books.length = 10`
- `albums.length = 3`
- `mp` 为空

用户问：“我的书架里有多少本书？”

正确回答：
> 你的书架共有 **13 个条目**：10 本电子书 + 3 个专辑/有声书。

错误回答：
> 你的书架共有 10 本书，另外还有 3 个有声书。

错误原因：用户问的是书架里的书，专辑/有声书也在书架里按“书”管理，必须计入总数，不能“另外还有”。

**例 2：无专辑，有文章收藏**

回包关键信息：
- `books.length = 15`
- `albums.length = 0`
- `mp` 非空
- 统计出 `books` 中包含 13 个公开阅读书籍 + 2 个私密阅读书籍


用户问：“我的书架有多少本书？”

正确回答：
> 你的书架共有 **16 个条目**：15 个书籍条目 + 1 个文章收藏；其中公开阅读 13 个、私密阅读 3 个。
解释：`mp` 非空时，文章收藏计入书架总数，并固定计入私密阅读数量。

错误回答：
> 你的书架共有 15 本纯书籍，另外还有 1 个文章收藏。
错误原因：用户问的是书架总数，文章收藏必须计入总数，不能用“另外还有”把它排除在总数之外。

**例 3：有专辑，有文章收藏**

回包关键信息：
- `books.length = 130`
- `albums.length = 3`
- `mp` 非空

用户问：“我的书架一共有多少本？”

正确回答：
> 你的书架可见条目共有 **134 个**：130 个书籍条目 + 3 个专辑/有声书 + 1 个文章收藏。

错误回答：
> 你的书架共有 133 个条目，另外还有 1 个文章收藏。

错误原因：文章收藏必须计入书架总数，不能用“另外还有”把它排除在总数之外。

## 公开/私密阅读数量

公开/私密阅读必须遍历实际返回条目：

- **私密阅读数** = `books[].secret == 1` 的数量 + `albums[].albumInfoExtra.secret == 1` 的数量 + (`mp` 非空 ? 1 : 0)
- **公开阅读数** = `books[].secret == 0` 的数量 + `albums[].albumInfoExtra.secret == 0` 的数量
- `mp` 只表示文章收藏目录入口，不包含具体内容；如果 `mp` 不存在则不影响公开/私密数量，如果 `mp` 非空则私密阅读数量固定 +1。

注意：只统计 `books[]`、`albums[]` 和 `mp` 这些实际返回的可见条目；未出现在数组中的服务端补丁项不能纳入公开/私密分组。

## 工作流

1. 调 `/shelf/sync` 获取书架列表。
2. 如果用户问“书架有多少本书/多少条目”，先计算可见条目数：`total = books.length + albums.length + (mp 非空 ? 1 : 0)`；注意 `albums[]` 是专辑/有声书，也必须计入书架里的书。
3. 如果用户问公开/私密阅读数量，遍历 `books[]` 和 `albums[]` 的 `secret` 字段分组计数；`mp` 不看 `secret`，只要非空就给私密阅读数量 +1。
4. 展示：书名、作者、分类，置顶书籍（`isTop`）标记提示，显示总数。
5. 查询有声书/专辑数量：直接读取 `albums` 数组长度即可，无需额外接口调用。
6. 用户选择某本书后，调 `/book/info` 获取详情。
7. 调 `/book/getprogress` 可查看某本书的阅读进度。

## 输出格式
- 书架列表用编号展示，支持通过编号选择查看详情
- 无参数时显示书架全览，第一句给出可见书架条目数：`books.length + albums.length + (mp 非空 ? 1 : 0)`；其中 `albums[]` 必须作为专辑/有声书计入书架总数
- 如果展示分类构成，各分类数量相加必须等于可见书架条目数；`mp` 非空时，文章收藏作为 1 个书架条目计入总数
- 公开/私密阅读数量必须展示为遍历 `books[]`、`albums[]` 后得到的分组计数，并在 `mp` 非空时给私密阅读数量 +1
- 传书名/bookId 时查看该书详情或进度
- 涉及有声书/专辑/听书的问题，直接使用 `albums` 字段回答
- 接口调用失败时回复：`书架信息暂时没拉到，请稍后再试~`
