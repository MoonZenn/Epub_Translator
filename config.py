# config.py - 配置管理
"""应用程序配置管理"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class AppConfig:
    """应用配置类"""
    # 默认路径
    DEFAULT_OUTPUT_DIR: str = os.path.join(os.path.expanduser("~"), "Desktop")

    # API配置
    DEFAULT_MODEL: str = "glm-4.7-flash"
    AVAILABLE_MODELS: tuple = ("glm-4.7-flash", "", "")

    # 翻译配置
    DEFAULT_BATCH_SIZE: int = 3000
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.3
    REQUEST_DELAY: float = 0.2  # 请求间隔秒数

    # UI配置
    WINDOW_TITLE: str = "EPUB小说翻译工具"
    WINDOW_MIN_WIDTH: int = 800
    WINDOW_MIN_HEIGHT: int = 600

    # 文件配置
    SUPPORTED_INPUT_FORMATS: str = "EPUB files (*.epub);;All files (*.*)"
    OUTPUT_FILENAME_PREFIX: str = "translated_"


@dataclass
class PromptTemplates:
    """提示词模板管理"""

    # 占位符
    CONTENT_PLACEHOLDER: str = "{text}"

    # 预设模板
    JAPANESE_HORROR: str = """这是一本日本恐怖小说的翻译。

请将以下日文翻译成流畅的中文，保持恐怖小说的紧张氛围和叙事节奏：

{text}"""

    JAPANESE_LIGHT_NOVEL: str = """这是一本日本轻小说的翻译。

请将以下日文翻译成流畅的中文，保持轻小说的风格和人物对话特色：

{text}"""

    JAPANESE_MYSTERY: str = """这是一本日本推理小说的翻译。

请将以下日文翻译成流畅的中文，保持推理小说的逻辑性和悬疑感：

{text}"""

    ENGLISH_NOVEL: str = """这是一本英文小说的翻译。

请将以下英文翻译成流畅的中文，保持原著的文学风格：

{text}"""

    KOREAN_NOVEL: str = """这是一本韩文小说的翻译。

请将以下韩文翻译成流畅的中文，保持小说的情感表达：

{text}"""

    @classmethod
    def get_preset(cls, name: str) -> Optional[str]:
        """获取预设模板"""
        presets = {
            "日本恐怖小说": cls.JAPANESE_HORROR,
            "日本轻小说": cls.JAPANESE_LIGHT_NOVEL,
            "日本推理小说": cls.JAPANESE_MYSTERY,
            "英文小说": cls.ENGLISH_NOVEL,
            "韩文小说": cls.KOREAN_NOVEL,
        }
        return presets.get(name)

    @classmethod
    def get_preset_names(cls) -> list:
        """获取所有预设名称"""
        return ["自定义", "日本恐怖小说", "日本轻小说", "日本推理小说", "英文小说", "韩文小说"]


# 全局配置实例
config = AppConfig()