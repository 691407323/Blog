# 博客系统实现说明

## 概述

这是一个极简静态博客系统，核心思路是 **Markdown → HTML**。由 Python 脚本一键将 Markdown 文章渲染为完整的 HTML 静态站点，无需数据库、无需后端运行时。

## 实现架构

```
content/posts/*.md  ──┐
templates/*.html    ──┼──► build.py ──► _site/
static/css/*.css    ──┘                  ├── index.html
                                         ├── posts/<slug>.html
                                         └── static/css/style.css
```

## 各文件职责

### 1. [build.py](build.py) — 构建入口

核心流程分三步：

**Step 1: 读取文章** (`load_posts`)
- 扫描 `content/posts/*.md`，用 `python-frontmatter` 解析 YAML 头信息
- 用 `markdown` 库（扩展：`fenced_code`、`toc`、`codehilite`）将 Markdown 转 HTML
- 正则后处理：从原始 Markdown 中提取代码块语言标识（如 ````python`），注入到生成的 `<code>` 标签的 `class="language-xxx"` 属性中
- 按 `date` 降序排列文章

**Step 2: 渲染模板**
- [templates/base.html](templates/base.html) — HTML 骨架，使用 Jinja2 `{% block content %}` 定义内容插槽
  - header：flex 布局实现标题居中，Home 链接 `position: absolute; left: 0` 靠左
  - footer：`text-align: center` 居中版权信息
  - 所有内联样式直接写在标签 `style` 属性中，不依赖额外 CSS class
- [templates/index.html](templates/index.html) — 继承 base，渲染文章列表（标题、日期、slug 链接）
- [templates/post.html](templates/post.html) — 继承 base，渲染单篇文章详情

**Step 3: 复制静态资源**
- 将 `static/` 目录完整复制到 `_site/static/`

### 2. [templates/base.html](templates/base.html) — 页面骨架

```html
<header>
  <div style="position:relative; display:flex; justify-content:center; align-items:center;">
    <a href="/" style="position:absolute; left:0;">Home</a>
    <h1>ScvReady Blog.</h1>  <!-- 居中 -->
  </div>
</header>
<main class="container">{% block content %}{% endblock %}</main>
<footer class="container">
  <p style="text-align:center;">Copyright © ...</p>
</footer>
```

设计要点：
- **标题居中**：通过 flex `justify-content: center` 实现，同时 Home 链接用绝对定位靠左，两者互不影响
- **内联样式**：header 和 footer 的关键样式写在 `style` 属性中，避免 CSS class 优先级和继承问题
- 模板变量：`site_title`、`title`、`start_year`、`current_year`

### 3. [static/css/style.css](static/css/style.css) — 全局样式

- `html { background: #f9f9f9 }` — 统一页面和视口背景色，防止内容不足时露出白色
- `body { margin: 0 }` — 消除默认 margin
- `.container { max-width: 800px; margin: 0 auto; padding: 24px }` — 内容区域居中、限宽
- `.posts` — 文章列表样式（无列表符号、底部分割线）
- `pre` — 代码块深色背景
- `footer p { text-align: center }` — 页脚文字居中

### 4. [content/posts/*.md](content/posts/) — 文章源文件

YAML front matter 支持的字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | 否 | 文章标题，未填则使用文件名 |
| `date` | 否 | 发布日期（YYYY-MM-DD），用于排序 |
| `slug` | 否 | URL 标识，未填则使用文件名 |

Markdown 支持：
- 标准 Markdown 语法（标题、列表、链接、图片等）
- 围栏代码块（```` ```language ````），自动语法高亮并保留语言标记

### 5. [requirements.txt](requirements.txt) — 依赖

| 包 | 用途 |
|---|---|
| `Jinja2` | HTML 模板引擎 |
| `Markdown` | Markdown → HTML 转换 |
| `python-frontmatter` | 解析 YAML front matter |
| `Pygments` | 代码语法高亮 |

### 6. [.github/workflows/deploy.yml](.github/workflows/deploy.yml) — CI/CD

触发条件：推送到 `main` 分支

流程：
1. 检出代码
2. 设置 Python 环境
3. 自动检测 `build.py` 所在目录（支持根目录或 `blog/` 子目录）
4. 安装依赖并执行 `python build.py`
5. 将 `_site/` 部署到 `gh-pages` 分支（GitHub Pages）

## 构建产物

`_site/` 目录结构：

```
_site/
├── index.html              # 首页（文章列表，按日期倒序）
├── posts/
│   └── <slug>.html         # 文章详情页
└── static/
    └── css/
        └── style.css       # 样式文件（复制自 static/）
```

## 技术选型理由

- **内联样式 vs CSS class**：header 居中布局依赖 flex + absolute 定位组合，用内联样式避免了 `.container` 基类的 `padding` 和 `max-width` 干扰居中效果。简单的全局样式（如 `.container`、`.posts`）保留在 CSS 文件中便于维护。
- **代码块语言标记**：Pygments 的 `codehilite` 扩展生成的 `<code>` 默认不带语言 class。正则后处理从原始 Markdown 提取语言标识注入，使 `<code class="language-python">` 可用于额外的 CSS 定制。
- **无 JS、无框架**：纯静态 HTML + CSS，加载极快，适合 GitHub Pages 托管。