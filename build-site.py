#!/usr/bin/env python3
"""Wraps index.html (Artifact format, no document tags) into docs/index.html for GitHub Pages."""
from pathlib import Path

HEAD = """<!doctype html>
<html lang="ru">
<head>
<meta name="description" content="Бельчата Коко и Орео готовят 20 блюд по шагам, а муха, лягушка и кот пытаются испортить еду.">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Коко и Орео">
<meta name="theme-color" content="#cfe5d8">
"""
root = Path(__file__).parent
page = (root / "index.html").read_text(encoding="utf-8")
head, body = page.split('<div class="wrap">', 1)
(root / "docs").mkdir(exist_ok=True)
(root / "docs" / "index.html").write_text(
    HEAD + head + '</head>\n<body>\n<div class="wrap">' + body + "</body>\n</html>\n", encoding="utf-8"
)
