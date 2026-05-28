# ui/main_window.py
"""主窗口"""

import os

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QMessageBox,
                             QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from config import config
from ui.widgets import FileGroup, ApiGroup, PromptGroup, ProgressGroup
from ui.workers import TranslationWorker
from utils.logger import Logger


class MainWindow(QMainWindow):
    """应用程序主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setMinimumSize(
            config.WINDOW_MIN_WIDTH,
            config.WINDOW_MIN_HEIGHT
        )

        self.worker: TranslationWorker = None
        self.logger = Logger()

        self._setup_ui()
        self._apply_fonts()

    def _setup_ui(self):
        """设置UI"""
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        layout.addLayout(self._create_header())

        # 功能组件
        self.file_group = FileGroup()
        self.api_group = ApiGroup()
        self.prompt_group = PromptGroup()
        self.progress_group = ProgressGroup()

        layout.addWidget(self.file_group)
        layout.addWidget(self.api_group)
        layout.addWidget(self.prompt_group)
        layout.addWidget(self.progress_group)

        # 日志区域
        layout.addWidget(self._create_log_group())

        # 按钮区域
        layout.addLayout(self._create_buttons())

    def _create_header(self):
        """创建标题栏"""
        from PyQt6.QtWidgets import QLabel
        from PyQt6.QtCore import Qt

        layout = QVBoxLayout()
        title = QLabel("📚 EPUB小说翻译工具")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        return layout

    def _create_log_group(self):
        """创建日志区域"""
        from PyQt6.QtWidgets import QGroupBox

        group = QGroupBox("运行日志")
        layout = QVBoxLayout()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)

        # 连接日志
        self.logger.callback = self._on_log

        layout.addWidget(self.log_text)
        group.setLayout(layout)
        return group

    def _create_buttons(self):
        """创建按钮区域"""
        layout = QHBoxLayout()

        # 开始按钮
        self.btn_start = QPushButton("🚀 开始翻译")
        self.btn_start.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        self._style_start_button()
        self.btn_start.clicked.connect(self._start_translation)
        layout.addWidget(self.btn_start)

        # 停止按钮
        self.btn_stop = QPushButton("⏹ 停止")
        self.btn_stop.setFont(QFont("Microsoft YaHei", 12))
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self._stop_translation)
        layout.addWidget(self.btn_stop)

        layout.addStretch()

        # 清空日志
        btn_clear = QPushButton("清空日志")
        btn_clear.clicked.connect(self._clear_log)
        layout.addWidget(btn_clear)

        return layout

    def _style_start_button(self):
        """设置开始按钮样式"""
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:disabled { background-color: #cccccc; }
        """)

    def _apply_fonts(self):
        """应用字体"""
        font = QFont("Microsoft YaHei", 9)
        self.setFont(font)

    def _on_log(self, message: str):
        """日志回调"""
        self.log_text.append(message)

    def _validate_inputs(self) -> bool:
        """验证输入"""
        if not self.file_group.validate():
            QMessageBox.warning(self, "警告", "请选择输入文件和输出目录！")
            return False

        if not os.path.exists(self.file_group.get_input_file()):
            QMessageBox.warning(self, "警告", "输入文件不存在！")
            return False

        if not self.api_group.validate():
            QMessageBox.warning(self, "警告", "请输入有效的API Key！")
            return False

        if not self.prompt_group.validate():
            QMessageBox.warning(self, "警告",
                                "提示词模板必须包含 {text} 占位符！")
            return False

        return True

    def _start_translation(self):
        """开始翻译"""
        if not self._validate_inputs():
            return

        # 更新UI状态
        self._set_running_state(True)
        self.progress_group.reset()
        self.logger.log("开始翻译任务...")

        # 创建工作线程
        self.worker = TranslationWorker(
            input_file=self.file_group.get_input_file(),
            output_dir=self.file_group.get_output_dir(),
            api_key=self.api_group.get_api_key(),
            prompt_template=self.prompt_group.get_prompt(),
            model=self.api_group.get_model()
        )

        # 连接信号
        self.worker.progress_updated.connect(
            self.progress_group.update_progress
        )
        self.worker.chapter_started.connect(
            self.progress_group.set_chapter
        )
        self.worker.log_message.connect(self.logger.log)
        self.worker.translation_completed.connect(
            self._on_translation_completed
        )

        self.worker.start()

    def _stop_translation(self):
        """停止翻译"""
        if self.worker:
            self.worker.stop()

    def _on_translation_completed(self, success: bool, message: str):
        """翻译完成回调"""
        self._set_running_state(False)

        if success:
            QMessageBox.information(self, "完成",
                                    f"翻译成功！\n保存至: {message}")
            self.progress_group.set_completed()
        else:
            QMessageBox.critical(self, "错误", message)
            self.progress_group.reset()

        self.logger.log(message)

    def _set_running_state(self, running: bool):
        """设置运行状态"""
        self.btn_start.setEnabled(not running)
        self.btn_stop.setEnabled(running)

        # 禁用输入组件
        self.file_group.setEnabled(not running)
        self.api_group.setEnabled(not running)
        self.prompt_group.setEnabled(not running)

    def _clear_log(self):
        """清空日志"""
        self.log_text.clear()
        self.logger.clear()