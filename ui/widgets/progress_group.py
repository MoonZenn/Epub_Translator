# ui/widgets/progress_group.py
"""进度显示组件"""

from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QProgressBar


class ProgressGroup(QGroupBox):
    """进度显示分组组件"""

    def __init__(self, parent=None):
        super().__init__("翻译进度", parent)
        self._setup_ui()
        self.reset()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # 章节信息
        self.chapter_label = QLabel("等待开始...")
        layout.addWidget(self.chapter_label)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        self._apply_style()
        layout.addWidget(self.progress_bar)

        # 状态标签
        self.status_label = QLabel("就绪")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def _apply_style(self):
        """应用样式"""
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)

    def update_progress(self, current: int, total: int, status: str):
        """更新进度"""
        percentage = int((current / total) * 100) if total > 0 else 0
        self.progress_bar.setValue(percentage)
        self.status_label.setText(f"{status} ({current}/{total})")

    def set_chapter(self, chapter_num: int, title: str):
        """设置当前章节"""
        self.chapter_label.setText(f"正在翻译: 第 {chapter_num} 章 - {title[:40]}")

    def reset(self):
        """重置状态"""
        self.chapter_label.setText("等待开始...")
        self.progress_bar.setValue(0)
        self.status_label.setText("就绪")

    def set_completed(self):
        """设置完成状态"""
        self.progress_bar.setValue(100)
        self.status_label.setText("完成")
        self.chapter_label.setText("翻译完成")