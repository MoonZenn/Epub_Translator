# core/text_splitter.py
"""文本分段模块"""

import re
from dataclasses import dataclass
from typing import List


@dataclass
class TextChunk:
    """文本块数据类"""
    content: str
    index: int
    total: int


class TextSplitter:
    """智能文本分段器"""

    def __init__(self, max_length: int = 3000):
        self.max_length = max_length

    def split(self, text: str) -> List[TextChunk]:
        """将文本分割为多个块"""
        # 清理空行
        text = self._clean_text(text)

        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        chunk_index = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # 超长段落单独处理
            if len(para) > self.max_length:
                if current_chunk:
                    chunks.append(self._create_chunk(current_chunk, chunk_index))
                    chunk_index += 1
                    current_chunk = ""

                # 强制分段
                sub_chunks = self._force_split(para)
                for sub in sub_chunks:
                    chunks.append(self._create_chunk(sub, chunk_index))
                    chunk_index += 1
                continue

            # 正常累加
            if self._should_split(current_chunk, para):
                chunks.append(self._create_chunk(current_chunk, chunk_index))
                chunk_index += 1
                current_chunk = para
            else:
                current_chunk = self._merge_paragraphs(current_chunk, para)

        # 添加最后一块
        if current_chunk:
            chunks.append(self._create_chunk(current_chunk, chunk_index))

        # 更新总数
        total = len(chunks)
        for i, chunk in enumerate(chunks):
            chunk.total = total
            chunk.index = i + 1

        return chunks

    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 合并多个空行
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        # 去除行首行尾空白
        lines = [line.strip() for line in text.split('\n')]
        return '\n'.join(lines)

    def _force_split(self, text: str) -> List[str]:
        """强制分段超长文本"""
        chunks = []
        for i in range(0, len(text), self.max_length):
            chunk = text[i:i + self.max_length]
            chunks.append(chunk)
        return chunks

    def _should_split(self, current: str, new_para: str) -> bool:
        """判断是否应该分割"""
        if not current:
            return False
        return len(current) + len(new_para) > self.max_length

    def _merge_paragraphs(self, current: str, new_para: str) -> str:
        """合并段落"""
        if not current:
            return new_para
        return current + "\n\n" + new_para

    def _create_chunk(self, content: str, index: int) -> TextChunk:
        """创建文本块"""
        return TextChunk(content=content.strip(), index=index, total=0)