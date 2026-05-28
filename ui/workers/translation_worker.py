# ui/workers/translation_worker.py
"""翻译工作线程"""

from PyQt6.QtCore import QThread, pyqtSignal

from core.epub_reader import EpubReader
from core.epub_writer import EpubWriter
from core.text_splitter import TextSplitter
from core.translator import Translator
from core.epub_reader import Chapter
from utils.logger import Logger


class TranslationWorker(QThread):
    """翻译工作线程"""

    # 信号定义
    progress_updated = pyqtSignal(int, int, str)  # 当前, 总数, 状态
    chapter_started = pyqtSignal(int, str)  # 章节号, 标题
    chapter_finished = pyqtSignal(int)  # 章节号
    translation_completed = pyqtSignal(bool, str)  # 成功, 消息
    log_message = pyqtSignal(str)  # 日志消息

    def __init__(self, input_file: str, output_dir: str,
                 api_key: str, prompt_template: str,
                 model: str = "glm-4-flash", batch_size: int = 3000):
        super().__init__()

        self.input_file = input_file
        self.output_dir = output_dir
        self.api_key = api_key
        self.prompt_template = prompt_template
        self.model = model
        self.batch_size = batch_size

        self.is_running = True
        self.logger = Logger(callback=self._on_log)

        # 组件初始化（延迟到run中）
        self.reader: EpubReader = None
        self.splitter: TextSplitter = None
        self.translator: Translator = None
        self.writer: EpubWriter = None

    def _on_log(self, message: str):
        """日志回调"""
        self.log_message.emit(message)

    def run(self):
        """执行翻译任务"""
        try:
            self._initialize()
            chapters = self._read_chapters()
            translated = self._translate_chapters(chapters)
            self._save_result(translated)

        except Exception as e:
            self.logger.log(f"错误: {str(e)}")
            self.translation_completed.emit(False, str(e))

    def _initialize(self):
        """初始化组件"""
        self.logger.log("初始化组件...")

        # API客户端
        from api.zhipu_client import create_client
        client = create_client(self.api_key)

        # 核心组件
        self.reader = EpubReader(self.input_file)
        self.splitter = TextSplitter(self.batch_size)
        self.translator = Translator(client, model=self.model)
        self.writer = EpubWriter(title="Translated Book", language="zh")

        self.logger.log("初始化完成")

    def _read_chapters(self) -> list:
        """读取章节"""
        self.logger.log(f"读取文件: {self.input_file}")
        chapters = self.reader.read()

        if not chapters:
            raise ValueError("未找到可翻译的章节")

        self.logger.log(f"找到 {len(chapters)} 个章节")
        return chapters

    def _translate_chapters(self, chapters: list) -> list:
        """翻译所有章节"""
        translated_chapters = []
        total_chunks = self._calculate_total_chunks(chapters)
        current_chunk = 0

        for idx, chapter in enumerate(chapters):
            if not self.is_running:
                raise InterruptedError("用户取消")

            self._translate_single_chapter(
                chapter, idx, translated_chapters,
                current_chunk, total_chunks
            )
            current_chunk += len(self.splitter.split(chapter.content))

        return translated_chapters

    def _calculate_total_chunks(self, chapters: list) -> int:
        """计算总块数"""
        return sum(
            len(self.splitter.split(c.content))
            for c in chapters
        )

    def _translate_single_chapter(self, chapter: Chapter, idx: int,
                                  result_list: list, current_chunk: int,
                                  total_chunks: int):
        """翻译单个章节"""
        self.chapter_started.emit(idx + 1, chapter.title)
        self.logger.log(f"开始翻译章节 {idx + 1}: {chapter.title[:30]}...")

        # 分段
        chunks = self.splitter.split(chapter.content)
        translated_parts = []
        context = ""

        for chunk in chunks:
            if not self.is_running:
                raise InterruptedError("用户取消")

            # 更新进度
            current_chunk += 1
            self.progress_updated.emit(
                current_chunk, total_chunks,
                f"段落 {chunk.index}/{chunk.total}"
            )

            # 翻译
            result = self.translator.translate(
                chunk.content, self.prompt_template, context
            )

            if result.success:
                translated_parts.append(result.text)
                context = result.context
            else:
                self.logger.log(f"翻译失败，保留原文: {result.error}")
                translated_parts.append(chunk.content)

        # 合并
        full_text = '\n\n'.join(translated_parts)
        result_list.append(Chapter(
            title=chapter.title,
            content=full_text,
            index=idx
        ))

        self.chapter_finished.emit(idx + 1)
        self.logger.log(f"章节 {idx + 1} 完成")

    def _save_result(self, chapters: list):
        """保存结果"""
        import os
        filename = os.path.basename(self.input_file)
        output_path = os.path.join(self.output_dir, f"translated_{filename}")

        self.logger.log("生成EPUB文件...")
        self.writer.write(chapters, output_path)

        self.translation_completed.emit(True, output_path)

    def stop(self):
        """停止翻译"""
        self.is_running = False
        self.logger.log("正在停止...")