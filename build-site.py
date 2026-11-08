#!/usr/bin/env python3
"""Wraps index.html (Artifact format, no document tags) into docs/index.html for GitHub Pages."""
import shutil
from pathlib import Path

HEAD = """<!doctype html>
<html lang="ru">
<head>
<meta name="description" content="Шеф Вера учит ребёнка готовить по-настоящему: вид от первого лица, холодильник, шаги по порядку.">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Готовлю сам">
<meta name="theme-color" content="#cfe5d8">
"""
root = Path(__file__).parent
page = (root / "index.html").read_text(encoding="utf-8")
head, body = page.split('<div class="wrap">', 1)
(root / "docs").mkdir(exist_ok=True)
(root / "docs" / "index.html").write_text(
    HEAD + head + '</head>\n<body>\n<div class="wrap">' + body + "</body>\n</html>\n", encoding="utf-8"
)
shutil.copytree(root / "art", root / "docs" / "art", dirs_exist_ok=True)
