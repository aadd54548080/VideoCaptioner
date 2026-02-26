import logging
import os
import sys
from pathlib import Path

VERSION = "v1.4.0"
YEAR = 2025
APP_NAME = "VideoCaptioner"
AUTHOR = "Weifeng"

HELP_URL = "https://github.com/WEIFENG2333/VideoCaptioner"
GITHUB_REPO_URL = "https://github.com/WEIFENG2333/VideoCaptioner"
RELEASE_URL = "https://github.com/WEIFENG2333/VideoCaptioner/releases/latest"
FEEDBACK_URL = "https://github.com/WEIFENG2333/VideoCaptioner/issues"

# 路径
# PyInstaller 打包后，_MEIPASS 指向临时解压目录（包含 resource 等打包资源）
# 可执行文件所在目录用于存放用户数据（AppData, work-dir）
if getattr(sys, "frozen", False):
    # PyInstaller frozen mode
    ROOT_PATH = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    _EXE_DIR = Path(sys.executable).parent
else:
    ROOT_PATH = Path(__file__).parent.parent
    _EXE_DIR = ROOT_PATH

RESOURCE_PATH = ROOT_PATH / "resource"
APPDATA_PATH = _EXE_DIR / "AppData"
WORK_PATH = _EXE_DIR / "work-dir"


BIN_PATH = RESOURCE_PATH / "bin"
ASSETS_PATH = RESOURCE_PATH / "assets"
SUBTITLE_STYLE_PATH = RESOURCE_PATH / "subtitle_style"
TRANSLATIONS_PATH = RESOURCE_PATH / "translations"
FONTS_PATH = RESOURCE_PATH / "fonts"

LOG_PATH = APPDATA_PATH / "logs"
LLM_LOG_FILE = LOG_PATH / "llm_requests.jsonl"
SETTINGS_PATH = APPDATA_PATH / "settings.json"
CACHE_PATH = APPDATA_PATH / "cache"
MODEL_PATH = APPDATA_PATH / "models"

FASER_WHISPER_PATH = BIN_PATH / "Faster-Whisper-XXL"

# 日志配置
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 环境变量添加 bin 路径，添加到PATH开头以优先使用
os.environ["PATH"] = str(FASER_WHISPER_PATH) + os.pathsep + os.environ["PATH"]
os.environ["PATH"] = str(BIN_PATH) + os.pathsep + os.environ["PATH"]

# 添加 VLC 路径
os.environ["PYTHON_VLC_MODULE_PATH"] = str(BIN_PATH / "vlc")

# 创建路径
for p in [CACHE_PATH, LOG_PATH, WORK_PATH, MODEL_PATH]:
    p.mkdir(parents=True, exist_ok=True)
