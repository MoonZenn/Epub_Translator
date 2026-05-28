# ui/widgets/file_group.py
"""文件选择组件"""

from PyQt6.QtWidgets import (QGroupBox, QGridLayout, QLabel,
                             QLineEdit, QPushButton, QFileDialog)


class FileGroup(QGroupBox):
    """文件选择分组组件"""

    def __init__(self, parent=None):
        super().__init__("文件设置", parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QGridLayout()

        # 输入文件
        layout.addWidget(QLabel("待翻译EPUB:"), 0, 0)
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("选择要翻译的EPUB文件...")
        layout.addWidget(self.input_path, 0, 1)

        btn_input = QPushButton("浏览...")
        btn_input.clicked.connect(self._browse_input)
        layout.addWidget(btn_input, 0, 2)

        # 输出目录
        layout.addWidget(QLabel("保存到文件夹:"), 1, 0)
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("选择翻译后文件的保存位置...")
        layout.addWidget(self.output_path, 1, 1)

        btn_output = QPushButton("浏览...")
        btn_output.clicked.connect(self._browse_output)
        layout.addWidget(btn_output, 1, 2)

        self.setLayout(layout)

    def _browse_input(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择EPUB文件", "",
            "EPUB files (*.epub);;All files (*.*)"
        )
        if file_path:
            self.input_path.setText(file_path)
            # 自动设置输出目录
            if not self.output_path.text():
                import os
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                self.output_path.setText(desktop)

    def _browse_output(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择保存文件夹", ""
        )
        if dir_path:
            self.output_path.setText(dir_path)

    def get_input_file(self) -> str:
        return self.input_path.text().strip()

    def get_output_dir(self) -> str:
        return self.output_path.text().strip()

    def validate(self) -> bool:
        """验证输入"""
        return bool(self.get_input_file() and self.get_output_dir())