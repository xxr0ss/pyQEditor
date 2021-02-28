from PySide6.QtWidgets import QWidget, QToolBar, QStackedWidget, QVBoxLayout, QSplitter
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtCore import Signal, Slot
from .folderExplorer import FolderExplorer
from ..icons_rc import *


class SideBar(QToolBar):
    request_explorer = Signal()

    def __init__(self, parent):
        super(SideBar, self).__init__(parent)
        self.parent = parent
        self.setMovable(False)
        self.folder_explorer = FolderExplorer(self.parent)

        self.tool_view = ToolView(self)
        self.tool_view.widget_container.addWidget(self.folder_explorer)

        self._init_tools()

    def _init_tools(self):
        action_folder_explorer = QAction(self)
        folder_icon = QIcon()
        folder_icon.addPixmap(QPixmap(':/default/ui/icons/explorer.png'), QIcon.Normal, QIcon.Off)
        action_folder_explorer.setIcon(folder_icon)
        action_folder_explorer.triggered.connect(self.on_action_folder_explorer_triggered)
        self.addAction(action_folder_explorer)

    def on_action_folder_explorer_triggered(self):
        tools = self.tool_view
        if tools.widget_container.currentWidget() == self.folder_explorer:
            if tools.isVisible():
                tools.setVisible(False)
            else:
                tools.setVisible(True)
        else:
            tools.widget_container.setCurrentWidget(self.folder_explorer)
            self.folder_explorer.setVisible(True)


class ToolView(QWidget):
    def __init__(self, parent):
        super(ToolView, self).__init__(parent)
        self.parent = parent
        self.tool_layout = QVBoxLayout(self)
        self.tool_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_container = QStackedWidget(self)
        self.tool_layout.addWidget(self.widget_container)
        self.setLayout(self.tool_layout)
        print('ToolView init done')