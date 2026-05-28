# core/epub_reader.py
"""EPUB文件读取模块"""

import re
from dataclasses import dataclass
from typing import List, Optional

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


@dataclass
class Chapter:
    """章节数据类"""
    title: str
    content: str
    index: int = 0


class EpubReader:
    """EPUB阅读器"""

    # 标题匹配模式
    TITLE_PATTERNS = [
        r'^[一二三四五六七八九十百千]+[、．.,\s]',  # 一、二、
        r'^第[一二三四五六七八九十百千]+[章节]',  # 第一章
        r'^\d+[、．.,\s]',  # 1. 2.
        r'^Chapter\s+\d+',  # Chapter 1
    ]

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.book: Optional[epub.EpubBook] = None

    def read(self) -> List[Chapter]:
        """读取EPUB所有章节"""
        self.book = epub.read_epub(self.file_path)
        chapters = []
        index = 0

        for item in self.book.get_items():
            if item.get_type() != ebooklib.ITEM_DOCUMENT:
                continue

            try:
                chapter = self._parse_item(item, index)
                if chapter:
                    chapters.append(chapter)
                    index += 1
            except Exception as e:
                print(f"解析章节失败: {e}")
                continue

        return chapters

    def _parse_item(self, item, index: int) -> Optional[Chapter]:
        """解析单个文档项"""
        content = item.get_content().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')

        # 提取文本
        body_text = soup.get_text(separator='\n').strip()
        if not body_text:
            return None

        # 提取标题
        title = self._extract_title(body_text) or f"章节{index + 1}"

        return Chapter(title=title, content=body_text, index=index)

    def _extract_title(self, text: str) -> Optional[str]:
        """从文本中提取标题"""
        lines = text.split('\n')

        for line in lines[:5]:  # 只检查前5行
            line = line.strip()
            for pattern in self.TITLE_PATTERNS:
                if re.match(pattern, line):
                    return line

        return None

    def get_metadata(self) -> dict:
        """获取书籍元数据"""
        if not self.book:
            return {}

        return {
            'title': self.book.get_metadata('DC', 'title'),
            'author': self.book.get_metadata('DC', 'creator'),
            'language': self.book.get_metadata('DC', 'language'),
        }