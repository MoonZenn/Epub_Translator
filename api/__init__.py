# api/__init__.py
"""API客户端模块"""

from .zhipu_client import create_client

__all__ = ['create_client']