import os
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize, Slot

from ui.ui_codeeditor import Ui_CodeEditor


class CodeEditor(QWidget):
    __title__ = 'Code Editor'
    untitled = 'untitled'

    # TODO: 使得必要的变量为私有，限制访问，比如self.filename

    def __init__(self, parent, filename=None):
        super(CodeEditor, self).__init__()
        self.parent = parent
        self.ui = Ui_CodeEditor()
        self.ui.setupUi(self)
        self.setLayout(self.ui.editorVLayout)
        self.editingArea = self.ui.codeEditingArea
        self.statusBar = self.ui.statusBar
        self.editingArea.cursorPositionChanged.connect(self.update_statusbar_cursor_pos)

        self.filepath = filename
        if filename is not None:
            self.load_file()
        else:
            self.new_file()

    def load_file(self):
        # if it's None, self.new_file rather than self.load_file should be called
        assert self.filepath is not None
        # file's existence should be checked before calling this method
        assert os.path.exists(self.filepath)

        with open(self.filepath, 'r') as f:
            content = f.read()
            self.editingArea.setPlainText(content)
        if '/' in self.filepath:
            self.__title__ = self.filepath.split('/')[-1]
        elif '\\' in self.filepath:
            self.__title__ = self.filepath.split('\\')[-1]
        else:
            self.__title__ = self.filepath

        self.setWindowTitle(self.filepath)

    def new_file(self):
        self.__title__ = self.untitled
        self.setWindowTitle('new file')

    def sizeHint(self) -> QSize:
        return self.parent.size()

    def get_content(self) -> bytes:
        content = self.editingArea.toPlainText()
        # TODO 这里要判断吗
        if isinstance(content, str):
            content = content.encode()
        return content

    @Slot()
    def update_statusbar_cursor_pos(self):
        cursor = self.editingArea.textCursor()
        row, col = cursor.blockNumber() + 1, cursor.columnNumber() + 1
        self.statusBar.updateCursorPos((row, col))
