from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize

from editingArea import EditingArea
from ui.ui_codeeditor import Ui_CodeEditor


class CodeEditor(QWidget):
    __title__ = 'Code Editor'

    def __init__(self, parent):
        super(CodeEditor, self).__init__()
        self.parent = parent
        self.ui = Ui_CodeEditor()
        self.ui.setupUi(self)
        self.setLayout(self.ui.editorVLayout)
        self.editingArea = EditingArea(self.parent)

    def sizeHint(self) -> QSize:
        return self.parent.size()
