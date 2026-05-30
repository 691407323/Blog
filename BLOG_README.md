# 简单博客模板使用说明

一个极简静态博客生成器，将 Markdown 文章渲染为纯 HTML 静态站点。

## 文件结构

```
Blog/
├── build.py                  # 构建脚本
├── requirements.txt          # Python 依赖
├── BLOG_README.md            # 本说明
├── .gitignore                # Git 忽略规则
├── .github/workflows/
│   └── deploy.yml            # GitHub Pages 自动部署
├── content/posts/
│   └── *.md                  # Markdown 博客文章（YAML front matter）
├── templates/
│   ├── base.html             # 基础骨架（header/导航/footer）
│   ├── index.html            # 首页模板（文章列表）
│   └── post.html             # 文章详情页模板
└── static/
    └── css/
        └── style.css         # 全局样式
```

## 如何添加文章

在 [content/posts/](content/posts/) 新建 `.md` 文件，开头添加 YAML front matter。

### 示例：一篇完整的文章

```markdown
---
title: 使用 Docker 部署 Python 应用
date: 2026-05-28
slug: docker-python-deploy
---

本文演示如何使用 Docker 容器化部署一个 Python Web 应用。

## Python 代码示例

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

## Dockerfile 示例

FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]

## Shell 命令

`# 构建并运行
docker build -t myapp:latest .
docker run -d -p 8080:8080 --name myapp myapp:latest`

## 小结

Docker 让 Python 应用的部署变得简单可靠。
```

### 支持的 Markdown 语法

| 语法 | 写法 | 说明 |
|------|------|------|
| 标题 | `## 二级标题`、`### 三级标题` | 最多六级，`#` 保留给页面标题 |
| 粗体 | `**粗体**` | 也支持 `__粗体__` |
| 斜体 | `*斜体*` | 也支持 `_斜体_` |
| 删除线 | `~~删除线~~` | |
| 行内代码 | `` `print("hello")` `` | 灰色背景高亮 |
| 代码块 | ` ```python ` … ` ``` ` | 带语言标记，自动语法高亮 |
| 无序列表 | `- 项目` 或 `* 项目` | 支持嵌套缩进 |
| 有序列表 | `1. 项目` | 数字自动递增 |
| 任务列表 | `- [ ] 待办` / `- [x] 已完成` | 复选框样式 |
| 引用 | `> 引用文字` | 支持 `>>` 多层嵌套 |
| 表格 | `\| 列A \| 列B \|` | 支持对齐（`:---`、`:---:`、`---:`） |
| 链接 | `[文字](https://url)` | 支持引用式链接 |
| 图片 | `![替代文字](image.png)` | |
| 分隔线 | `---` 或 `***` | 水平分割线 |
| 脚注 | `[^1]` + `[^1]: 内容` | 自动渲染到页面底部 |
| HTML | `<details>`、`<kbd>` 等 | 原生 HTML 标签可直接嵌入 |

### Front Matter 字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | 否 | 文章标题，默认取文件名 |
| `date` | 否 | 发布日期（YYYY-MM-DD），用于排序降序 |
| `slug` | 否 | URL 友好标识，默认取文件名 |

### 现有示例文章

| 文件 | 说明 |
|------|------|
| [hello-world.md](content/posts/hello-world.md) | 入门示例，简单展示基本语法 |
| [markdown-guide.md](content/posts/markdown-guide.md) | Markdown 语法全面演示 |
| [docker-python-deploy.md](content/posts/docker-python-deploy.md) | 多语言代码高亮 + 表格 + 引用 |

## 构建站点

```bash
# 创建虚拟环境并安装依赖
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 构建
python build.py
```

构建完成后，`_site/` 目录即为完整静态站点：

- `_site/index.html` — 首页（文章列表）
- `_site/posts/<slug>.html` — 各文章详情页
- `_site/static/css/style.css` — 样式文件

## 本地预览

直接用浏览器打开 `_site/index.html`，或使用简易 HTTP 服务器：

```bash
cd _site && python3 -m http.server 8000
# 浏览器访问 http://localhost:8000
```

## 部署到 GitHub Pages

推送到 `main` 分支即自动触发 [deploy.yml](.github/workflows/deploy.yml)，将 `_site/` 部署到 `gh-pages` 分支。

需要在仓库 Settings → Pages 中将 Source 设为 "Deploy from a branch"，分支选 `gh-pages`、目录选 `/ (root)`。

## 代码高亮

代码块会自动使用 Pygments 进行语法高亮，`<code>` 标签会带上 `class="language-xxx"` 便于 CSS 选择器做语言特定样式。

## 样式说明

- header 标题居中，Home 链接靠左（内联 flex 布局）
- footer 版权信息居中
- 页面背景统一为 `#f9f9f9`，无默认 margin
