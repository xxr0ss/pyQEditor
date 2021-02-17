from PySide6.QtCore import Qt, Signal, Slot  # for enum flags
from PySide6.QtWidgets import QMainWindow, QFileDialog, QDockWidget, QTabWidget
from codeEditor import CodeEditor

from ui.ui_mainwindow import Ui_mainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        # set dock tabs position north
        self.setTabPosition(Qt.TopDockWidgetArea, QTabWidget.North)

        self.codeEditor = CodeEditor(self)
        self.dock_editor = QDockWidget(self.codeEditor.__title__, self)
        self.dock_editor.setWidget(self.codeEditor)

        self.addDockWidget(Qt.TopDockWidgetArea, self.dock_editor)


    def addNewEditor(self, content):
        editor = CodeEditor(self, content)
        new_dock_editor = QDockWidget('opened file')
        new_dock_editor.setWidget(editor)
        self.addDockWidget(Qt.TopDockWidgetArea, new_dock_editor)
        self.tabifyDockWidget(new_dock_editor, self.dock_editor)

        # use both show and raise_ to display newly added dock widget in the front
        new_dock_editor.show()
        new_dock_editor.raise_()


    @Slot()
    def on_actionOpen_triggered(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File')
        file = filename[0]
        with open(file, 'r') as f:
            content = f.read()
        self.addNewEditor(content)
    
    @Slot()
    def on_actionSave_triggered(self):
        pass