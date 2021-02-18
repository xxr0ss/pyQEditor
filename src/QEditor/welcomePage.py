from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize
from .ui.ui_welcomepage import Ui_welcomePage


class WelcomePage(QWidget):
    def __init__(self, parent):
        super(WelcomePage, self).__init__()
        self.ui = Ui_welcomePage()
        self.ui.setupUi(self)
        self.parent = parent
        self.setLayout(self.ui.verticalLayout)

    def sizeHint(self) -> QSize:
        return self.parent.size()
