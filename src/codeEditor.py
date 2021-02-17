import os
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize, Slot

from ui.ui_codeeditor import Ui_CodeEditor


class CodeEditor(QWidget):
    __title__ = 'Code Editor'

    def __init__(self, parent, filename=None):
        super(CodeEditor, self).__init__()
        self.parent = parent
        self.ui = Ui_CodeEditor()
        self.ui.setupUi(self)
        self.setLayout(self.ui.editorVLayout)
        self.editingArea = self.ui.codeEditingArea
        self.statusBar = self.ui.statusBar
        self.editingArea.cursorPositionChanged.connect(self.update_statusbar_cursor_pos)

        self.filename = filename
        if filename is not None:
            self.load_file()
        else:
            self.new_file()

    def load_file(self):
        # if it's None, self.new_file rather than self.load_file should be called
        assert self.filename is not None
        # file's existence should be checked before calling this method
        assert os.path.exists(self.filename)

        with open(self.filename, 'r') as f:
            content = f.read()
            self.editingArea.setPlainText(content)
        if '/' in self.filename:
            self.__title__ = self.filename.split('/')[-1]
        elif '\\' in self.filename:
            self.__title__ = self.filename.split('\\')[-1]
        else:
            self.__title__ = self.filename

        self.setWindowTitle(self.__title__)

    def new_file(self):
        self.__title__ = 'untitled'
        self.setWindowTitle(self.__title__)

    def sizeHint(self) -> QSize:
        return self.parent.size()

    @Slot()
    def update_statusbar_cursor_pos(self):
        cursor = self.editingArea.textCursor()
        row, col = cursor.blockNumber() + 1, cursor.columnNumber() + 1
        self.statusBar.updateCursorPos((row, col))
