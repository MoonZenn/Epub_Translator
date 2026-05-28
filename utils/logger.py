# utils/logger.py
"""日志工具"""

import time
from typing import Callable, Optional


class Logger:
    """简单日志记录器"""

    def __init__(self, callback: Optional[Callable[[str], None]] = None):
        self.callback = callback
        self.logs: list = []

    def log(self, message: str):
        """记录日志"""
        timestamp = time.strftime('%H:%M:%S')
        formatted = f"[{timestamp}] {message}"

        self.logs.append(formatted)

        if self.callback:
            self.callback(formatted)

        # 同时打印到控制台
        print(formatted)

    def clear(self):
        """清空日志"""
        self.logs.clear()

    def get_logs(self) -> list:
        """获取所有日志"""
        return self.logs.copy()