import webbrowser

try:
    from PyQt6.QtWidgets import QDialog
except ImportError:
    from PyQt5.QtWidgets import QDialog

from aqt.browser.browser import Browser
from aqt.gui_hooks import browser_menus_did_init

from .tag_ui import tag_start
from .text_ui import text_start
from .audio_ui import audio_start

def __init__(self, browser):
    QDialog.__init__(self, parent=browser)
    self.browser = browser

def open_help_page():
    webbrowser.open_new("https://ankiweb.net/shared/info/1609139780")
    
def setup_menu(self: Browser):
    menubar = self.form.menubar
    menu = menubar.addMenu("Batch Edit Tools")

    tag = menu.addAction("Batch Add Tag")
    tag.triggered.connect(lambda _: tag_start())
    
    text = menu.addAction("Batch Replace Text")
    text.triggered.connect(lambda _: text_start())
    
    audio = menu.addAction("Batch Add Audio")
    audio.triggered.connect(lambda _: audio_start())
    
    h = menu.addAction("Help")
    h.triggered.connect(lambda _: open_help_page())

browser_menus_did_init.append(setup_menu)