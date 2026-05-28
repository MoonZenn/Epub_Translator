# api/zhipu_client.py
"""智谱AI客户端封装"""

from typing import Optional

try:
    from zai import ZhipuAiClient
except ImportError:
    ZhipuAiClient = None


class ZhipuClientError(Exception):
    """智谱客户端错误"""
    pass


def create_client(api_key: str) -> Optional[object]:
    """创建智谱AI客户端"""
    if ZhipuAiClient is None:
        raise ZhipuClientError("zai-sdk库未安装，请运行: pip install zai-sdk")

    if not api_key or len(api_key) < 10:
        raise ZhipuClientError("API Key无效")

    try:
        client = ZhipuAiClient(api_key=api_key)
        return client
    except Exception as e:
        raise ZhipuClientError(f"创建客户端失败: {e}")