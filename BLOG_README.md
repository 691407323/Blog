# 简单博客模板使用说明

已为你生成了一个极简静态博客模板。主要文件：

- [build.py](build.py)：构建脚本，会把 `content/posts/*.md` 转为 HTML 输出到 `_site/`。
- [templates/](templates/)：Jinja2 模板，包含 `base.html`, `index.html`, `post.html`。
- [content/posts/](content/posts/)：放置 Markdown 博客文章（带 YAML front matter）。示例：[content/posts/hello-world.md](content/posts/hello-world.md#L1)
- [static/](static/)：静态资源（CSS 等），会被复制到 `_site/static/`。

如何添加文章（Markdown）：

1. 在 `content/posts/` 新建一个 `.md` 文件，例如 `my-first-post.md`。
2. 在文件开头添加 YAML front matter，至少包含 `title` 和可选的 `date` 与 `slug`，例如：

```
---
title: 我的第一篇博客
date: 2026-05-28
slug: my-first-post
---

这里写你的 Markdown 内容。
```

构建站点：

```bash
# macOS / Linux 示例
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build.py

# 生成后，打开 _site/index.html 查看首页，文章在 _site/posts/*.html
```

说明：
- 模板使用 Jinja2 渲染；Markdown 支持代码高亮（需要 Pygments）。
- 若要部署到 GitHub Pages，提交 `_site/` 到 gh-pages 分支或使用其他静态主机。
