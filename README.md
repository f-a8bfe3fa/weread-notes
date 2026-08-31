# 📖 微信读书笔记自动同步工具 \(小白专属配置指南\)

## 🌟 **写在前面：**

这是一个专门为**完全不懂计算机的小白**准备的超详细安装指南！

原版文档有很多专业的命令行操作（比如 Git、Pip 等），在这里我们**通通不需要**！你只需要跟着下面的视频步骤，用鼠标点击、复制、粘贴，就能轻松搭建属于你自己的**微信读书 \-\> Notion \+ GitHub 个人私有笔记库**！



## 这个工具能做什么？



简单来说，它能帮你：



- **自动拉取**你在微信读书里做的划线、想法、书评

- **保存到 GitHub** 仓库，永久备份，不怕丢失

- **同步到 Notion**，方便整理、搜索、分享

- **每天自动运行**，自动同步笔记，不用你操心



---



## 🧭 准备工作



在正式开始配置之前，请先注册并登录以下三个账号：

1. **GitHub 账号**（用于存放备份文件和自动运行同步程序）

2. **微信读书账号**（用于获取你的读书笔记）

3. **Notion 账号**（用于精美展示和整理你的笔记）

    

---



## [🎬 详细配置步骤（可以跟随视频一步步来）](https://www.bilibili.com/video/BV19B4X63EcD/?share_source=copy_web&vd_source=7c6ec3f3af94f35847bcff21c07d5800)



### 第一步：创建你自己的 GitHub 私人仓库



为了保护你的阅读隐私，我们需要把代码放到你自己的“私人保险箱”（私有仓库）里。

[项目地址](https://github.com/f-a8bfe3fa/weread-notes)

1. **下载项目代码：**

    - 访问本项目主页，点击右侧绿色的 **「Code」** 按钮，然后选择 **「Download ZIP」**，将项目下载到本地电脑。

2. **本地解压与清理：**

    - 将下载好的压缩包解压。

    - **重要的一步：** 进入解压后的文件夹，把 `data` 文件夹里的文件（存放书籍数据的文件夹）和 `index.json` 测试文件删掉。因为这些是作者的测试笔记，我们不需要它们，我们要用自己的。

3. **在 GitHub 上新建私人仓库：**

    - 登录你的 GitHub，点击页面右上角的 **「\+」**，选择 **「New repository」**（新建仓库）。

    - **仓库名称（Repository name）：** 可以起一个好记的名字（例如：`weread-notes`）。

    - **可见性（Visibility）：** **一定要选择 「Private」（私有）**！这样别人就看不到你的读书笔记了，安全第一。

    - 点击最下方的绿色 **「Create repository」** 按钮创建成功。

4. **拖拽上传代码文件：**

    - 页面跳转后，点击中间的 **「uploading an existing file」**（上传已有文件）链接。

    - 打开刚才本地解压并清理好的文件夹，**全选里面所有的文件**，直接用鼠标**拖拽**到网页中。

    - 等待所有文件上传完毕后，拉到页面最下方，点击绿色的 **「Commit changes」**（保存更改）按钮。

        

---



### 第二步：获取你的微信读书密钥 \(Key\)



我们需要一把“钥匙”来读取你的微信读书笔记。



1. 登录 [微信读书网页版](https://weread.qq.com/)。

2. 点击你的头像。

3. 再点击 **「微信读书 skill」**

4. 翻到最下面，找到并**复制这一串 Key**。

5. 临时新建一个文本文件（记事本），把这个 Key 粘贴保存好，等会儿要用。

    

---



### 第三步：配置 Notion 模板与集成



让笔记漂亮地同步到你的 Notion 数据库中！

[notion模板](https://bubble-sodium-5ed.notion.site/362e809a4d8b80f89245e3582fded80a?v=364e809a4d8b8034be53000cd463a87d&source=copy_link)

#### 1\. 复制 Notion 模板

- 在原项目网页右侧，找到 **Notion 模板链接** 并点击打开。

- 页面加载完后，点击右上角的 **「Duplicate」**（克隆/复制）按钮，将这个模板复制到你自己的 Notion 工作区中。

    

#### 2\. 清理模板中的测试数据

- 进入你刚刚克隆好的 Notion 页面，你会看到几条作者留下的测试笔记，**直接全选并删除**它们。我们需要一个干净的空白数据库来存放你自己的笔记。

    

#### 3\. 创建 Notion 机器人（集成/Integration）

- 访问 Notion 的开发者门户：[Notion My Integrations](https://www.notion.so/my-integrations)。

- 点击 **「\+ New integration」**（新建集成）。

- 给它起个名字（例如：`微信读书同步`），然后点击 **「Submit」** 提交。

- 提交后，你会看到一串 **「Internal Integration Token」**（内部集成令牌，以 `secret_` 开头）。点击 **「Copy」** 复制它，并记录在你的记事本中，这叫做 **Notion API Key**。

    

#### 4\. 把机器人关联到你的 Notion 页面

- 回到你刚刚克隆的 Notion 数据库页面。

- 点击右上角的 **「\.\.\.」**（省略号按钮）。

- 往下翻，找到 **「Connections」**（连接）或 **「Add connections」**（新增连接）。

- 搜索你刚刚创建的机器人名字（如：`微信读书同步`），点击添加并同意关联。这一步至关重要，否则机器人无法把笔记写进你的页面！

    

#### 5\. 获取 Notion 数据库 ID

- 看看你当前 Notion 数据库页面的浏览器地址栏（URL）。

- 它的格式通常是 `https://www.notion.so/你的用户名/一串字母数字?v=一串字母数字`。

- **斜杠 ****`/`**** 后面、问号 ****`?`**** 之前的这一长串 32 位的字母数字**，就是你的 **Notion Database ID**。把它复制并记录到记事本里。

    

---



### 第四步：配置 GitHub Secrets（填入安全钥匙）



现在我们要把记事本里的“三把安全钥匙”安全地存放到 GitHub 中，让自动运行的程序能够使用它们。



1. 回到你在 GitHub 上刚刚创建的私有仓库页面（可以看到有一个锁的标志，代表私有）。

2. 点击仓库上方的 **「Settings」**（设置）选项卡。

3. 在左侧菜单栏中往下翻，找到 **「Secrets and variables」**，点击展开后选择 **「Actions」**。

4. 点击右上角绿色的 **「New repository secret」**（新建仓库密钥）按钮。

5. 我们需要依次添加以下 **3 个密钥**（每次添加一个，名字填在 `Name` 里，内容填在 `Value` 里，然后点击 Add secret 保存）：

    

|密钥名称（Name）|对应填入的内容（Value）|
|---|---|
|**`WEREAD_API_KEY`**|你在第二步中复制的 **微信读书 Key**|
|**`NOTION_API_KEY`**|你在第三步中获得的 Notion **Internal Integration Token**|
|**`NOTION_DATABASE_ID`**|你在第三步中提取的 Notion **Database ID**|



---



### 第五步：配置自动运行工作流 \(GitHub Actions\)



由于我们是手动拖拽上传的文件，可能漏掉了 GitHub 用来自动定时运行的“工作流”配置文件。我们需要手动在 GitHub 上把它们创建出来。



原项目中有两个自动运行的任务文件，我们都需要复制：

- `daily-sync.yml`（每天自动增量同步）

- `manual-full-sync.yml`（每周自动全量同步）

    

1. **配置每日同步工作流：**

    - 回到原项目的网页，点击进入 `.github/workflows` 文件夹，点击 `daily-sync.yml`。

    - 点击右上角的 **「Copy raw content」**（复制原始文件内容）图标。

    - 回到你自己的 GitHub 仓库，点击 **「Add file」** \-\> **「Create new file」**（创建新文件）。

    - 文件名输入：`.github/workflows/daily-sync.yml`（GitHub 会自动为你创建文件夹路径）。

    - 将刚刚复制的内容粘贴到下方的代码框中。

    - 点击右上角绿色的 **「Commit changes\.\.\.」** 按钮保存。

        

2. **配置每周同步工作流：**

    - 同样地，回到原项目网页，点击进入 `.github/workflows`，点击 `manual-full-sync.yml`。

    - 点击复制内容。

    - 回到你自己的仓库，点击 **「Add file」** \-\> **「Create new file」**。

    - 文件名输入：`.github/workflows/manual-full-sync.yml`（**注意：后缀名 ****`.yml`**** 一定要手动打全哦！**）。

    - 粘贴内容并保存（Commit changes）。

        

---



### 第六步：手动运行一次，开启自动同步之旅！



全部配置完成后，我们需要手动触发一次，让程序进行首次同步，并激活以后的定时自动同步。



1. 在你的 GitHub 仓库上方，点击 **「Actions」**（操作）选项卡。

2. 在左侧菜单中，你会看到我们刚刚创建的两个工作流。

3. **首先点击「每周运行的工作流」**（或全量同步工作流）：

    - 在右侧点击 **「Run workflow」**（运行工作流）按钮，再点击绿色的 **Run workflow** 确认。

    - 页面刷新后，你会看到一个正在运行的任务。如果你的读书笔记比较少，大约 1 分钟就会运行成功（显示绿色对勾）。

    - 此时，去你的 **Notion 页面** 刷新看看，你的微信读书笔记是不是已经神奇地全部排好版、出现在页面里了？

4. **然后点击「每日运行的工作流」**：

    - 同样地，手动点击 **「Run workflow」** 运行一次，完成初始化。

        

🎉 **大功告成！** 

现在，小工具已经彻底配置完毕。以后，它会在每周一凌晨和每天早上**自动帮你把微信读书的新笔记、新划线和想法同步到 Notion 和 GitHub**，你再也不需要手动做任何操作了！



---



## 💡 进阶小贴士（适合笔记超级多的朋友）



如果你的一个非常热爱读书的人，那你微信**读书笔记一定非常多（成千上万条）**，第一次全量同步可能会因为耗时太长而中途断开。



你可以做如下优化：

1. 在你自己的 GitHub 仓库中，找到并点击打开 `.github/workflows/manual-full-sync.yml` 文件。

2. 点击右上角的画笔图标（编辑文件）。

3. 视频中，作者将时间限制设置为了 `60` 分钟。如果你的笔记量极大，建议将这个数值修改为 **`120`**（即 120 分钟/2个小时），这样同步过程就不会因为超时而意外中断，确保所有笔记能一次性顺利拉取下来！

4. 修改后点击 **「Commit changes\.\.\.」** 保存即可。

    



---
## 相关链接

[视频教程](https://www.bilibili.com/video/BV19B4X63EcD/?share_source=copy_web&vd_source=7c6ec3f3af94f35847bcff21c07d5800)

[项目地址](https://github.com/f-a8bfe3fa/weread-notes)

大家可能由于网络原因，没办法正常的使用GitHub。可以下载下面这个加速器，就可以正常访问GitHub。

加速器：[FastGithub](https://cloud.tsinghua.edu.cn/d/df482a15afb64dfeaff8/)

[Notion APP](https://pan.quark.cn/s/08c55de48928)

---


## 效果展示

<img width="1280" height="586" alt="image" src="https://github.com/user-attachments/assets/252a23fc-f02c-4f2c-8427-def2298fbf2f" />




Notion很自由，我们可以个性化的修改我们的页面，让它变得美观

<img width="1911" height="821" alt="image" src="https://github.com/user-attachments/assets/22637faa-a3f2-4f5f-9c30-37427eeaca6d" />


<img width="1878" height="876" alt="image" src="https://github.com/user-attachments/assets/7d3c09de-0083-47a2-bccc-1f99da037746" />



---



祝你使用愉快！如果有问题，可以在项目的 GitHub Issues 中提问。

