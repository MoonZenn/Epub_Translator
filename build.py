# build.py
"""打包脚本"""

import PyInstaller.__main__


def build():
    """构建可执行文件"""

    args = [
        'main.py',
        '--name=EPUB翻译工具',
        '--windowed',
        '--onefile',
        '--clean',
        '--noconfirm',

        # 核心模块
        '--hidden-import=core.epub_reader',
        '--hidden-import=core.epub_writer',
        '--hidden-import=core.text_splitter',
        '--hidden-import=core.translator',

        # API客户端
        '--hidden-import=api.zhipu_client',
        '--hidden-import=zai',  # 添加
        '--hidden-import=zai.ZhipuAiClient',  # 添加

        # UI模块
        '--hidden-import=ui.main_window',
        '--hidden-import=ui.widgets.file_group',
        '--hidden-import=ui.widgets.api_group',
        '--hidden-import=ui.widgets.prompt_group',
        '--hidden-import=ui.widgets.progress_group',
        '--hidden-import=ui.workers.translation_worker',

        # 工具模块
        '--hidden-import=utils.logger',
        '--hidden-import=config',

        # 第三方库
        '--hidden-import=ebooklib',
        '--hidden-import=ebooklib.epub',
        '--hidden-import=bs4',
        '--hidden-import=bs4.BeautifulSoup',  # 添加
        '--hidden-import=lxml',
        '--hidden-import=tqdm',
    ]

    PyInstaller.__main__.run(args)
    print("打包完成！文件在 dist/ 目录")


if __name__ == "__main__":
    build()