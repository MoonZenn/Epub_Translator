# core/translator.py
"""翻译核心模块"""

import re
import time
from dataclasses import dataclass
from typing import Callable, Optional, Tuple


@dataclass
class TranslationResult:
    """翻译结果"""
    text: str
    context: str  # 用于上下文的摘要
    success: bool
    error: Optional[str] = None


class Translator:
    """翻译器基类"""

    def __init__(self, client, model: str = "glm-4.7-flash",
                 max_tokens: int = 4096, temperature: float = 0.3,
                 delay: float = 0.2):
        self.client = client
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.delay = delay

    def translate(self, text: str, prompt_template: str,
                  context: str = "") -> TranslationResult:
        """执行翻译"""
        if not text.strip():
            return TranslationResult(text="", context="", success=True)

        # 构建提示词
        prompt = self._build_prompt(text, prompt_template, context)

        try:
            result = self._call_api(prompt)
            cleaned = self._clean_result(result)
            summary = self._generate_summary(cleaned)

            time.sleep(self.delay)  # 请求间隔

            return TranslationResult(
                text=cleaned,
                context=summary,
                success=True
            )

        except Exception as e:
            return TranslationResult(
                text=text,  # 失败返回原文
                context="",
                success=False,
                error=str(e)
            )

    def _build_prompt(self, text: str, template: str, context: str) -> str:
        """构建提示词"""
        prompt = template.format(text=text)

        if context:
            prompt = f"前文风格参考：{context}\n\n{prompt}"

        return prompt

    def _call_api(self, prompt: str) -> str:
        """调用API"""
        messages = [{"role": "user", "content": prompt}]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )

        return response.choices[0].message.content

    def _clean_result(self, text: str) -> str:
        """清理翻译结果"""
        # 去除常见的解释性前缀
        patterns = [
            r'^翻译[：:]\s*',
            r'^以下是?[：:]\s*',
            r'^译文[：:]\s*',
        ]

        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.MULTILINE)

        return text.strip()

    def _generate_summary(self, text: str, length: int = 80) -> str:
        """生成摘要用于上下文"""
        return text[:length] if len(text) > length else text