from .folderExplorer import FolderExplorer
from .editorsExplorer import EditorsExplorer
from PySide6.QtCore import QObject, Signal, Slot


class ExplorersManager(QObject):
    def __init__(self, window):
        # TODO: use singleton
        self.window = window
        self.folder_explorer = FolderExplorer(window)
        self.editors_explorer = EditorsExplorer(window)

    @Slot()
    def folder_filepath_response(self, filepath):
        """
        handle filepath_clicked from folder_explorer
        """
        pass
