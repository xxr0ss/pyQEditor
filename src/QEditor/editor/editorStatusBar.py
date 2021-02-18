from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize
from ..ui.ui_editorstatusbar import Ui_editorStatusBar


class EditorStatusBar(QWidget):
    def __init__(self, parent: QWidget):
        super(EditorStatusBar, self).__init__()
        self.parent = parent
        self.ui = Ui_editorStatusBar()
        self.ui.setupUi(self)

    def sizeHint(self) -> QSize:
        return QSize(self.parent.size().width(), 20)

    def updateCursorPos(self, pos: (int, int)):
        # TODO: hande Tab properly
        text = f'{pos[0]}:{pos[1]}'
        self.ui.cursorPos.setText(text)
