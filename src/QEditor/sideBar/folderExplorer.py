from PySide6.QtWidgets import QTreeView, QFileSystemModel, QVBoxLayout, QWidget
from PySide6.QtCore import QObject, Signal, Slot, Qt, QModelIndex
from PySide6.QtGui import QMouseEvent
import os


class FolderExplorer(QWidget):
    """
    A explorer for file folder, use Qt's model/view
    """
    file_clicked = Signal(str)

    def __init__(self, parent):
        super(FolderExplorer, self).__init__()
        self.parent = parent
        self._folder_dir_path = ''
        self._tree_view: QTreeView = None
        self.folder_model = None
        self.layout = QVBoxLayout(self)
        # self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    @property
    def folder_dir_path(self):
        return self._folder_dir_path

    def open_folder(self, dir_name: str) -> bool:
        if self._folder_dir_path != '':
            # already have folder opened
            return False
        self._init_folder_tree_view(dir_name)
        return True

    def _init_folder_tree_view(self, dir_name):
        print('opened directory: ', dir_name)
        self._folder_dir_path = dir_name    # set associated dir path

        self.folder_model = QFileSystemModel()
        self._tree_view = FolderTreeView(self)
        self._tree_view.setModel(self.folder_model)
        self._tree_view.setRootIndex(self.folder_model.setRootPath(dir_name))

        # Hide columns we don't need
        self._tree_view.hideColumn(1)
        self._tree_view.hideColumn(2)
        self._tree_view.hideColumn(3)

        self._tree_view.setHeaderHidden(True)

        self.layout.addWidget(self._tree_view)

    @property
    def folder_tree_view(self):
        return self._tree_view

    def enterEvent(self, event: QMouseEvent) -> None:
        event.accept()
        print('Entered folder explorer')


class FolderTreeView(QTreeView):
    def __init__(self, parent):
        super(FolderTreeView, self).__init__()
        self.parent = parent

    def mousePressEvent(self, event: QMouseEvent) -> None:
        index: QModelIndex = self.indexAt(event.pos())
        if not index.isValid():
            print('invalid mousePressEvent')
            super().mousePressEvent(event)
            return

        model: QFileSystemModel = self.model()
        filepath = model.filePath(index)
        print(f"'{filepath}' clicked")

        if os.path.isfile(filepath):
            self.parent.file_clicked.emit(filepath)
        elif os.path.isdir(filepath):
            # check isExpanded twice because clicking the '>' left to item
            # will affect whether collapse or expand.
            # if we write:
            # self.collapse(index) if self.isExpanded(index) else self.expand(index)
            # super().mousePressEvent(event)
            # will mess up this process because it will expand and collapse (and vise versa)
            was_expanded = self.isExpanded(index)
            super().mousePressEvent(event)
            if event.button() == Qt.LeftButton:
                expanded = self.isExpanded(index)
                if was_expanded == expanded:
                    self.collapse(index) if expanded else self.expand(index)
        else:
            print('unknown type')
            super().mousePressEvent(event)
