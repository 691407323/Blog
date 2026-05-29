#!/usr/bin/env python3
"""
Simple static blog builder:
- Reads markdown files from content/posts/*.md (YAML front matter supported)
- Renders posts with Jinja2 templates in templates/
- Outputs static site to _site/
"""
from pathlib import Path
import shutil
import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader


def load_posts(dirpath):
    p = Path(dirpath)
    posts = []
    if not p.exists():
        return posts
    for md_file in sorted(p.glob('*.md')):
        post = frontmatter.load(md_file)
        meta = dict(post.metadata)
        meta.setdefault('title', md_file.stem)
        meta.setdefault('date', '')
        meta.setdefault('slug', meta.get('slug', md_file.stem))
        html = markdown.markdown(post.content, extensions=['fenced_code', 'toc', 'codehilite'])
        posts.append({'meta': meta, 'content': html, 'src': md_file})
    posts.sort(key=lambda x: x['meta'].get('date', ''), reverse=True)
    return posts


def build():
    root = Path(__file__).resolve().parent
    env = Environment(loader=FileSystemLoader(root / 'templates'))
    out = root / '_site'
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    # copy static
    static_dir = root / 'static'
    if static_dir.exists():
        shutil.copytree(static_dir, out / 'static')

    posts = load_posts(root / 'content/posts')

    # render posts
    for p in posts:
        tpl = env.get_template('post.html')
        html = tpl.render(post=p['meta'], content=p['content'], site_title='My Blog')
        slug = p['meta'].get('slug') or p['meta'].get('title', '').lower().replace(' ', '-')
        dest = out / 'posts' / f"{slug}.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding='utf-8')

    # render index
    tpl = env.get_template('index.html')
    index_html = tpl.render(posts=[{'title': p['meta']['title'], 'date': p['meta'].get('date', ''), 'slug': p['meta'].get('slug')} for p in posts], site_title='My Blog')
    (out / 'index.html').write_text(index_html, encoding='utf-8')

    print('Built site -> _site/')


if __name__ == '__main__':
    build()
