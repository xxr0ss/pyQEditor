from PySide6.QtCore import Qt  # for enum flags
from PySide6.QtWidgets import QMainWindow, QWidget, QDockWidget
from codeEditor import CodeEditor

from ui.ui_main import Ui_mainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.codeEditor = CodeEditor(self)
        dock_editor = QDockWidget(self.codeEditor.__title__, self)
        dock_editor.setWidget(self.codeEditor)

        self.addDockWidget(Qt.TopDockWidgetArea, dock_editor)
