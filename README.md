<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/GUI-PyQt6-green?style=flat-square&logo=qt" alt="PyQt6">
  <img src="https://img.shields.io/badge/AI-智谱AI-purple?style=flat-square" alt="ZhipuAI">
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey?style=flat-square&logo=windows" alt="Windows">
  <img src="https://img.shields.io/badge/license-MIT-yellow?style=flat-square" alt="License">
</p>

<h1 align="center">📖 EPUB 小说翻译工具</h1>

<p align="center">
  <em>翻遍了全网也找不到中文版的那本冷门轻小说？<br>丢进来，选个风格，AI 帮你从头翻到尾——排版都帮你调好了。</em>
</p>

---

## 🤔 这是什么？

一个基于**智谱AI**的桌面端 EPUB 翻译器。不是什么通用翻译软件，它就是专门为了一件事做的：

> **把你看不懂的外文小说 EPUB，变成排版精美的中文 EPUB。**

目前支持日语、英语、韩语小说的中文化翻译，内置了针对不同类型小说的翻译风格模板——恐怖小说就该有恐怖的氛围，轻小说就该有轻小说的调调，而不是千篇一律的机翻味儿。

<p align="center">
  <kbd>拖入 EPUB</kbd> → <kbd>选个模板</kbd> → <kbd>点一下按钮</kbd> → <kbd>扔进阅读器开看</kbd>
</p>

---

## ✨ 凭什么选它？

<table>
  <tr>
    <td>🧠 <b>懂章节</b></td>
    <td>不管你是「第一章」「一、」「Chapter 1」还是韩式编号，自动识别，不丢一个章节</td>
  </tr>
  <tr>
    <td>✂️ <b>会分段</b></td>
    <td>按段落边界智能切割，不会把一句话拦腰截断，每段最多 3000 字</td>
  </tr>
  <tr>
    <td>🔗 <b>有记忆</b></td>
    <td>翻译后面章节时会把前面的风格摘要传给 AI，全书语气统一不跳戏</td>
  </tr>
  <tr>
    <td>🎨 <b>有审美</b></td>
    <td>导出的 EPUB 自带中文排版样式——首行缩进、两端对齐、标点悬挂，不是白板一张</td>
  </tr>
  <tr>
    <td>🎭 <b>懂风格</b></td>
    <td>恐怖小说、轻小说、推理小说……不同题材配不同翻译提示词，告别千篇一律</td>
  </tr>
  <tr>
    <td>🖥️ <b>有界面</b></td>
    <td>PyQt6 写的正经桌面 GUI，进度条、日志、实时状态一览无余，不是命令行黑框框</td>
  </tr>
  <tr>
    <td>🛑 <b>能反悔</b></td>
    <td>翻到一半不想翻了？点「停止」就行，随时喊停</td>
  </tr>
</table>

---

## 🚀 快速开始

### 你需要准备

- Windows 10 或 11
- Python 3.10 以上
- 一个[智谱AI 的 API Key](https://open.bigmodel.cn/)（注册就送额度，够翻好几本了）

### 三步跑起来

```bash
# 1. 装依赖
pip install -r requirements.txt
pip install zai-sdk

# 2. 启动
python main.py

# 3. 填上 API Key，选本 EPUB，点「开始翻译」
```

---

## 🎯 内置翻译模板

| 模板 | 适合什么样的书 |
|:---|:---|
| 🎃 日本恐怖小说 | 日式怪谈、心理恐怖——那种细思极恐的味儿 |
| ✨ 日本轻小说 | 校园恋爱异世界——对话多、语气活 |
| 🔍 日本推理小说 | 本格派社会派——逻辑严密悬疑拉满 |
| 📚 英文小说 | 欧美文学通用——忠实原文不添油加醋 |
| 🇰🇷 韩文小说 | 韩语文学——语调自然不端着 |
| ✏️ 自定义 | 自己写 prompt，想怎么翻就怎么翻 |

> ⚠️ 自定义模板里别忘了放 `{text}`，那才是要被翻译的内容。

---

## 📁 项目结构

```
epub_translator/
├── main.py                  # 🚪 入口
├── config.py                # ⚙️ 配置 & 提示词模板
├── build.py                 # 📦 PyInstaller 打包脚本
├── requirements.txt         # 📋 依赖清单
│
├── api/
│   └── zhipu_client.py      # 🔌 智谱AI SDK 封装
│
├── core/
│   ├── epub_reader.py       # 📖 读 EPUB，拆章节
│   ├── epub_writer.py       # ✍️ 写 EPUB，调排版
│   ├── text_splitter.py     # ✂️ 文本分段
│   └── translator.py        # 🌐 调用 AI 做翻译
│
├── ui/
│   ├── main_window.py       # 🪟 主窗口
│   ├── widgets/             # 🧩 界面小组件
│   └── workers/             # 🧵 后台翻译线程
│
└── utils/
    └── logger.py            # 📝 日志
```

---

## 🧬 数据流

```
  EPUB 文件
     │
     ▼
  EpubReader        ← ebooklib + BeautifulSoup
     │
     ▼
  [Chapter] × N     章节列表
     │
     ▼
  TextSplitter      ← 按段落边界切块（≤3000字）
     │
     ▼
  [TextChunk] × M   文本块列表
     │
     ▼
  Translator         ← 智谱AI Chat API + 上下文传递
     │
     ▼
  [Chapter] × N     翻译后的章节
     │
     ▼
  EpubWriter         ← 嵌入式 CJK 排版 CSS
     │
     ▼
  translated_xxx.epub ✅
```

---

## 🔧 可调配置

打开 [config.py](file:///d:/item/PyCharm/epub_translator/config.py)，这几个参数你可能会想改：

| 配置项 | 默认值 | 改它干嘛 |
|:---|:---|:---|
| `DEFAULT_MODEL` | `glm-4.7-flash` | 换个模型试试翻译质量 |
| `DEFAULT_BATCH_SIZE` | `3000` | 改大 = 更快但上下文可能溢出；改小 = 更稳但更慢 |
| `TEMPERATURE` | `0.3` | 调高 = 翻译更有"创意"（也可能是乱翻） |
| `REQUEST_DELAY` | `0.2` | API 限流时调大保平安 |

---

## 📦 打包成 exe

```bash
python build.py
```

`dist/EPUB翻译工具.exe` —— 单文件，双击即用，发给不用 Python 的朋友也毫无压力。

---

## 🤝 贡献

Bug 报告、功能建议、PR 都欢迎。如果你有更好的翻译 prompt，也欢迎提交——让模板库越来越丰富。

---

## � 隐私审计

本项目已完成代码隐私审查，结论如下：

| 检查项 | 结果 |
|:---|:---|
| API Key 硬编码 | ✅ 未发现 — 密钥通过 GUI 密码框输入，运行时传入，不落盘 |
| 密码 / Token | ✅ 未发现 |
| 邮箱地址 | ✅ 未发现 |
| IP 地址 | ✅ 未发现 |
| 个人文件路径 | ✅ 未发现（源码中） |
| `.env` 文件 | ✅ 未发现 |

> 🛡️ `build/` 和 `dist/` 目录（PyInstaller 构建产物）中包含构建机器的用户目录路径（`C:\Users\<USERNAME>\...`），已通过 `.gitignore` 排除，不会提交到仓库。

---

## �📄 许可

MIT License · 仅供学习与研究使用 · 请遵守智谱AI开放平台服务条款
