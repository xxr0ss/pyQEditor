import os
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize, Slot

from ui.ui_codeeditor import Ui_CodeEditor


class CodeEditor(QWidget):
    def __init__(self, parent, filepath=None):
        super(CodeEditor, self).__init__()
        self.parent = parent
        self.ui = Ui_CodeEditor()
        self.ui.setupUi(self)
        self.setLayout(self.ui.editorVLayout)
        self.editingArea = self.ui.codeEditingArea
        self.statusBar = self.ui.statusBar
        self.editingArea.cursorPositionChanged.connect(self.update_statusbar_cursor_pos)

        self._filepath = filepath
        if filepath is not None:
            self.load_file()
        else:
            self.new_file()

    def load_file(self):
        # if it's None, self.new_file rather than self.load_file should be called
        assert self._filepath is not None
        # file's existence should be checked before calling this method
        assert os.path.exists(self._filepath)

        with open(self._filepath, 'r') as f:
            content = f.read()
            self.editingArea.setPlainText(content)

        # always make file path '/'-style in CodeEditor
        # because both Windows and Linux are happy to use it
        if '\\' in self._filepath:
            self._filepath = self._filepath.replace('\\', '/')

        self.setWindowTitle(self.get_file_base_name())

    def new_file(self):
        self.setWindowTitle('new file')

    def sizeHint(self) -> QSize:
        return self.parent.size()

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self._filepath = value

    def get_content(self) -> bytes:
        content = self.editingArea.toPlainText()
        # TODO 这里要判断吗
        if isinstance(content, str):
            content = content.encode()
        return content

    # get file base name, for example 'D:/a/b/c.txt' will return 'c.txt'.
    # useful when being used as window title
    def get_file_base_name(self) -> str:
        if self._filepath is None:
            return 'New File'
        return self._filepath.split('/')[-1]

    # check if code editor is using a new file that haven't been saved
    # (so its filepath is None)
    def is_new_file(self) -> bool:
        return self._filepath is None

    @Slot()
    def update_statusbar_cursor_pos(self):
        cursor = self.editingArea.textCursor()
        row, col = cursor.blockNumber() + 1, cursor.columnNumber() + 1
        self.statusBar.updateCursorPos((row, col))
