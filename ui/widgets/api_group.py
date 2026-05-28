# ui/widgets/api_group.py
"""API设置组件"""

from PyQt6.QtWidgets import QGroupBox, QGridLayout, QLabel, QLineEdit, QComboBox

from config import config


class ApiGroup(QGroupBox):
    """API设置分组组件"""

    def __init__(self, parent=None):
        super().__init__("API设置", parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QGridLayout()

        # API Key
        layout.addWidget(QLabel("API Key:"), 0, 0)
        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key.setPlaceholderText("输入智谱AI API Key...")
        layout.addWidget(self.api_key, 0, 1)

        # 模型选择
        layout.addWidget(QLabel("模型:"), 1, 0)
        self.model_combo = QComboBox()
        self.model_combo.addItems(config.AVAILABLE_MODELS)
        layout.addWidget(self.model_combo, 1, 1)

        self.setLayout(layout)

    def get_api_key(self) -> str:
        return self.api_key.text().strip()

    def get_model(self) -> str:
        return self.model_combo.currentText()

    def validate(self) -> bool:
        """验证输入"""
        key = self.get_api_key()
        return len(key) > 10  # 简单验证