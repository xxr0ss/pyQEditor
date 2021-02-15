import PySide6
from ui.ui_codeEditor import *

class CodeEditor(QWidget):
    __title__ = 'Editor'

    def __init__(self, parent: QWidget):
        super().__init__()
        self.parent = parent
        self.ui = Ui_codeEditor()
        self.ui.setupUi(self)
        
        self.setLayout(self.ui.horizontalLayout)
        self.loadStyleSheet()
        
    def loadStyleSheet(self):
        with open('ui/stylesheet.css', 'r') as f:
            self.setStyleSheet(f.read())
    
    def sizeHint(self) -> PySide6.QtCore.QSize:
        return PySide6.QtCore.QSize(self.parent.size())