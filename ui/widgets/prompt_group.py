# ui/widgets/prompt_group.py
"""提示词设置组件"""

from PyQt6.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout,
                             QLabel, QTextEdit, QComboBox)

from config import PromptTemplates


class PromptGroup(QGroupBox):
    """提示词设置分组组件"""

    def __init__(self, parent=None):
        super().__init__("翻译提示词模板", parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # 预设选择
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("快速选择:"))

        self.preset_combo = QComboBox()
        self.preset_combo.addItems(PromptTemplates.get_preset_names())
        self.preset_combo.currentTextChanged.connect(self._on_preset_changed)
        preset_layout.addWidget(self.preset_combo)
        preset_layout.addStretch()

        layout.addLayout(preset_layout)

        # 提示词编辑
        self.prompt_edit = QTextEdit()
        self.prompt_edit.setPlaceholderText(
            "输入提示词模板，使用 {text} 作为待翻译内容的占位符..."
        )
        self.prompt_edit.setMaximumHeight(120)

        # 默认提示词
        default = PromptTemplates.JAPANESE_HORROR
        self.prompt_edit.setText(default)

        layout.addWidget(self.prompt_edit)
        self.setLayout(layout)

    def _on_preset_changed(self, preset_name: str):
        """预设变更处理"""
        if preset_name == "自定义":
            return

        template = PromptTemplates.get_preset(preset_name)
        if template:
            self.prompt_edit.setText(template)

    def get_prompt(self) -> str:
        return self.prompt_edit.toPlainText().strip()

    def validate(self) -> bool:
        """验证输入"""
        prompt = self.get_prompt()
        return "{text}" in prompt