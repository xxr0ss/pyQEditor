from PySide6.QtWidgets import QWidget, QToolBar, QStackedWidget, QVBoxLayout, QSplitter
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtCore import Signal, Slot
from .folderExplorer import FolderExplorer
from ..rc_icons import *

class SideBar(QToolBar):
    request_explorer = Signal()

    def __init__(self, parent):
        super(SideBar, self).__init__(parent)
        self.parent = parent
        self.setMovable(False)
        self.folder_explorer = FolderExplorer(self.parent)
        self.stacked_widget = QStackedWidget(self)
        self.widget_current = QWidget()
        self.tool_layout = QVBoxLayout(self)
        self.tool_layout.setContentsMargins(0,0,0,0)
        self.tool_layout.addWidget(self.stacked_widget)
        self.stacked_widget.addWidget(self.folder_explorer)
        self.widget_current.setLayout(self.tool_layout)
        self.widget_current.setVisible(False)
        self._init_tools()

    def _init_tools(self):
        action_folder_explorer = QAction(self)
        folder_icon = QIcon()
        folder_icon.addPixmap(QPixmap(':/default/ui/icons/explorer.png'), QIcon.Normal, QIcon.Off)
        action_folder_explorer.setIcon(folder_icon)
        action_folder_explorer.triggered.connect(self.on_action_folder_explorer_triggered)
        self.addAction(action_folder_explorer)

    def on_action_folder_explorer_triggered(self):
        if not self.widget_current.isVisible():
            self.widget_current.setVisible(True)
            self.folder_explorer.setVisible(True)
        else:
            self.folder_explorer.setVisible(False)
            self.widget_current.setVisible(False)
