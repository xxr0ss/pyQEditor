from PySide6.QtCore import Qt # for enum flags
from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtWidgets import QDockWidget
from codeEditor import CodeEditor

from ui.ui_main import Ui_mainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        dock_editor = QDockWidget(CodeEditor.__title__, self)
        dock_editor.setWidget(CodeEditor(self))
        self.addDockWidget(Qt.TopDockWidgetArea, dock_editor)
        