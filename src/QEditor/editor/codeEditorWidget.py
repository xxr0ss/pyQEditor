import os
from PySide6.QtWidgets import QWidget, QPlainTextEdit
from PySide6.QtCore import QSize, Slot, Signal

from ..ui.ui_codeeditor import Ui_CodeEditor


class CodeEditorWidget(QWidget):
    content_status_changed = Signal(bool)  # self._need_saving

    _new_file_count = 0

    @classmethod
    def reset_new_file_count(cls):
        cls._new_file_count = 0

    def __init__(self, parent=None, filepath=None):
        super(CodeEditorWidget, self).__init__()
        self.parent = parent    # for sizeHint only
        self.ui = Ui_CodeEditor()
        self.ui.setupUi(self)
        self.setLayout(self.ui.editorVLayout)
        self._editingArea: QPlainTextEdit = self.ui.codeEditingArea
        self.statusBar = self.ui.statusBar
        self.editingArea.cursorPositionChanged.connect(self.update_statusbar_cursor_pos)

        self._need_saving = False
        self.editingArea.textChanged.connect(lambda: self.content_status_changed.emit(True))
        self.content_status_changed[bool].connect(self.content_status_change)

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

        # keep file path '/'-style in CodeEditor
        # because both Windows and Linux are happy to use it
        if '\\' in self._filepath:
            self._filepath = self._filepath.replace('\\', '/')

        self.setWindowTitle(self.get_file_base_name())

    def new_file(self):
        CodeEditorWidget._new_file_count += 1
        self.setWindowTitle('untitled-%d' % CodeEditorWidget._new_file_count)

    def sizeHint(self) -> QSize:
        return self.parent.size()

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self._filepath = value

    @property
    def need_saving(self):
        return self._need_saving

    @need_saving.setter
    def need_saving(self, value):
        self._need_saving = value

    @property
    def editingArea(self):
        return self._editingArea

    def get_content(self) -> bytes:
        content = self.editingArea.toPlainText()
        # TODO 这里要判断吗
        if isinstance(content, str):
            content = content.encode()
        return content

    def get_file_base_name(self) -> str:
        """
        get file base name\n
        for example 'D:/a/b/c.txt' will return 'c.txt'. useful when being used as window title

        use `widget.windowTitle()` instead if it's for display purposes

        :return: if editor have associated file path, then return fileBaseName, otherwise return ''
        """
        if self._filepath is None:
            return ''
        return self._filepath.split('/')[-1]

    def is_new_file(self) -> bool:
        return self._filepath is None

    @Slot()
    def update_statusbar_cursor_pos(self):
        cursor = self.editingArea.textCursor()
        row, col = cursor.blockNumber() + 1, cursor.columnNumber() + 1
        self.statusBar.updateCursorPos((row, col))

    @Slot()
    def content_status_change(self, need_saving: bool):
        self._need_saving = need_saving
