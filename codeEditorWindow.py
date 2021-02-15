import PySide6
from ui.ui_codeEditor import *

from codeEditor import CodeEditor

class CodeEditorWindow(QWidget):
    __title__ = 'Editor'

    def __init__(self, parent: QWidget):
        super().__init__()
        self.parent = parent
        self.ui = Ui_codeEditor()
        self.ui.setupUi(self)
        
        self.setLayout(CodeEditor())
        self.loadStyleSheet()
        
    def loadStyleSheet(self):
        with open('ui/stylesheet.css', 'r') as f:
            self.setStyleSheet(f.read())
    
    def sizeHint(self) -> PySide6.QtCore.QSize:
        return PySide6.QtCore.QSize(self.parent.size())