#!/usr/bin/env python3
import os
import platform
import sys

from PIL import ImageFile
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from mdcx.consts import IS_DOCKER, IS_MAC, IS_NFC, IS_PYINSTALLER, IS_WINDOWS, MAIN_PATH
from mdcx.controllers.main_window.main_window import MyMAinWindow
from mdcx.i18n import install_translator
from mdcx.i18n.tooltips import apply_tooltips
from mdcx.controllers.main_window.responsive import make_window_scrollable
from mdcx.controllers.main_window.english_layout import widen_english_text_columns
from mdcx.controllers.main_window.style import apply_application_palette
from mdcx.utils.video import VIDEO_BACKEND

ImageFile.LOAD_TRUNCATED_IMAGES = True


def show_constants():
    """显示所有运行时常量"""
    constants = {
        "MAIN_PATH": MAIN_PATH,
        "IS_WINDOWS": IS_WINDOWS,
        "IS_MAC": IS_MAC,
        "IS_DOCKER": IS_DOCKER,
        "IS_NFC": IS_NFC,
        "IS_PYINSTALLER": IS_PYINSTALLER,
        "VIDEO_BACKEND": VIDEO_BACKEND,
    }
    print("Run time constants:")
    for key, value in constants.items():
        print(f"\t{key}: {value}")


show_constants()


if os.path.isfile("highdpi_passthrough"):
    # Qt6 默认启用高 DPI，这里仅保留非整数缩放策略开关，避免 150% 缩放被取整。
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

app = QApplication(sys.argv)
app.setStyle("Fusion")
apply_application_palette(False)
if platform.system() != "Windows":
    app.setWindowIcon(QIcon("resources/Img/MDCx.ico"))  # 设置任务栏图标
# Install the interface translation before any window is built, so the generated
# retranslateUi() picks it up. With no mapping for MDCX_LANG the app stays Chinese.
install_translator(app)
ui = MyMAinWindow()
# Short hover descriptions so every function is discoverable, including the
# tools Zak had never used because the labels were Chinese. Applied after the
# window exists; it only calls setToolTip, so nothing else is affected.
apply_tooltips(ui)
# Let the window be resized freely: the four pages whose content is absolutely
# positioned get a scroll area, matching what page_tool and page_setting
# already do. Without this, shrinking the window puts controls outside it.
make_window_scrollable(ui)
widen_english_text_columns(ui.page_main)
ui.show()
app.installEventFilter(ui)
# newWin2 = CutWindow()
try:
    sys.exit(app.exec())
except Exception as e:
    print(e)
