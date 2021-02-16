from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize, Slot

from editingArea import EditingArea
from editorStatusBar import EditorStatusBar
from ui.ui_codeeditor import Ui_CodeEditor


class CodeEditor(QWidget):
    __title__ = 'Code Editor'

    def __init__(self, parent):
        super(CodeEditor, self).__init__()
        self.parent = parent
        self.ui = Ui_CodeEditor()
        self.ui.setupUi(self)
        self.setLayout(self.ui.editorVLayout)
        self.editingArea = self.ui.codeEditingArea
        self.statusBar = self.ui.statusBar
        self.editingArea.cursorPositionChanged.connect(self.update_statusbar_cursor_pos)

    def sizeHint(self) -> QSize:
        return self.parent.size()

    @Slot()
    def update_statusbar_cursor_pos(self):
        cursor = self.editingArea.textCursor()
        row, col = cursor.blockNumber() + 1, cursor.columnNumber() + 1
        self.statusBar.updateCursorPos((row, col))
