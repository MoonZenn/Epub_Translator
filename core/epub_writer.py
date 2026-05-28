# core/epub_writer.py
"""EPUB文件写入模块"""

import os
from typing import List

import ebooklib
from ebooklib import epub

from .epub_reader import Chapter


class EpubWriter:
    """EPUB写入器"""

    def __init__(self, title: str = "Translated Book",
                 author: str = "Unknown",
                 language: str = "zh"):
        self.title = title
        self.author = author
        self.language = language
        self.style = self._default_style()

    def write(self, chapters: List[Chapter], output_path: str):
        """写入EPUB文件"""
        book = epub.EpubBook()

        # 设置元数据
        book.set_identifier('translated_book')
        book.set_title(self.title)
        book.set_language(self.language)
        book.add_author(self.author)

        # 添加样式
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=self.style
        )
        book.add_item(nav_css)

        # 创建章节
        epub_chapters = []
        spine = ['nav']

        for idx, chapter in enumerate(chapters):
            epub_chapter = self._create_chapter(chapter, idx, nav_css)
            book.add_item(epub_chapter)
            epub_chapters.append(epub_chapter)
            spine.append(epub_chapter)

        # 设置目录和书脊
        book.toc = tuple(epub_chapters)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        book.spine = spine

        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 写入文件
        epub.write_epub(output_path, book, {})

    def _create_chapter(self, chapter: Chapter, index: int,
                        style: epub.EpubItem) -> epub.EpubHtml:
        """创建单个章节"""
        # 转义HTML特殊字符
        safe_title = self._escape_html(chapter.title)

        # ──────────────── 调试信息 ────────────────
        print(f"[章节 {index + 1:03d}] {chapter.title}")
        print(f"  输入 content 长度: {len(chapter.content):5d} 字符")
        if len(chapter.content.strip()) == 0:
            print("  !!! 警告：章节内容完全为空 !!!")

        # 分段落处理
        paragraphs = chapter.content.split('\n\n')
        valid_paragraphs = [p.strip() for p in paragraphs if p.strip()]

        print(f"  原始段落数: {len(paragraphs)}")
        print(f"  有效段落数 (strip后): {len(valid_paragraphs)}")

        if not valid_paragraphs:
            print("  !!! 该章节无任何有效段落内容，将使用占位 !!!")
            # 防止完全空的 body 导致 lxml 报 "Document is empty"
            p_html = (
                '<p style="color:#888; font-style:italic; text-align:center;">'
                '（本章内容为空或翻译失败，已保留占位）</p>'
            )
        else:
            # 生成段落 HTML
            p_html = ''.join(
                f'<p>{self._escape_html(p)}</p>\n'
                for p in valid_paragraphs
            )

        # 构建完整的 XHTML 内容
        html_content = f'''<?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" lang="{self.language}">
    <head>
        <meta charset="utf-8"/>
        <title>{safe_title}</title>
        <link rel="stylesheet" type="text/css" href="style/nav.css"/>
    </head>
    <body>
        <h1>{safe_title}</h1>
        {p_html}
    </body>
    </html>'''

        # 调试：最终内容长度
        print(f"  生成的 html_content 长度: {len(html_content):5d} 字节")

        # 创建 EpubHtml 对象
        epub_chapter = epub.EpubHtml(
            title=chapter.title,
            file_name=f'text/chapter_{index + 1:03d}.xhtml',  # 推荐使用 text/ 前缀，更符合 EPUB 规范
            lang=self.language,
            content=html_content.encode('utf-8')  # 显式编码为 bytes
        )

        # 添加样式
        epub_chapter.add_item(style)

        return epub_chapter

    def _escape_html(self, text: str) -> str:
        """转义HTML特殊字符"""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))

    def _default_style(self) -> str:
        return '''
        @namespace ur[](http://www.w3.org/1999/xhtml);

        body {
            font-family: "Noto Serif CJK SC", "Source Han Serif SC", "SimSun", "Hiragino Serif", serif;
            font-size: 1.1em;
            line-height: 1.75;
            padding: 4% 5%;
            text-align: justify;
            text-justify: inter-ideograph;
            color: #222;
            background: #fdfdfd;
        }

        h1 {
            font-size: 1.6em;
            font-weight: bold;
            text-align: center;
            letter-spacing: 0.08em;
            margin: 2.2em 0 1.2em;
            page-break-before: always;
        }

        p {
            text-indent: 2em;
            margin: 0.4em 0;
            orphans: 3;
            widows: 3;
            hanging-punctuation: first last;
        }

        ruby rt {
            font-size: 0.55em;
            color: #555;
        }

        blockquote {
            margin: 1.5em 2em;
            padding-left: 1.2em;
            border-left: 3px solid #ccc;
            font-style: italic;
            color: #444;
        }

        .center { text-align: center; }
        .right  { text-align: right; }

        @media (max-width: 480px) {
            body { padding: 6% 8%; font-size: 1.05em; }
        }
        '''