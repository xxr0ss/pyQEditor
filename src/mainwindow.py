from PySide6.QtCore import Qt, Signal, Slot, QCoreApplication, qDebug  # for enum flags
from PySide6.QtWidgets import QMainWindow, QFileDialog, QDockWidget, QMessageBox, QTabWidget
from codeEditor import CodeEditor
from welcomePage import WelcomePage
import os

from ui.ui_mainwindow import Ui_mainWindow


class MainWindow(QMainWindow):
    # Signals
    externalFile = Signal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        # store editor dock widget instances
        self.dock_pages: list[QDockWidget] = []

        self.externalFile.connect(self.addNewEditor)
        # set dock tabs position north
        self.setTabPosition(Qt.TopDockWidgetArea, QTabWidget.North)

        self.check_cmd_args()

    @Slot()
    def on_actionOpen_triggered(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File')
        self.addNewEditor(filename[0])
    
    @Slot()
    def on_actionSave_triggered(self):
        pass

    def addNewEditor(self, filename):
        editor = CodeEditor(self, filename)
        new_dock_editor = QDockWidget(editor.__title__, self)
        new_dock_editor.setWidget(editor)
        self.addDockWidget(Qt.TopDockWidgetArea, new_dock_editor)
        if len(self.dock_pages) != 0:
            self.tabifyDockWidget(self.dock_pages[-1], new_dock_editor)
        self.dock_pages.append(new_dock_editor)
        new_dock_editor.show()
        new_dock_editor.raise_()

    def add_welcome_page(self):
        # TODO: add welcome page (like vscode)
        page = WelcomePage(self)
        new_dock = QDockWidget('Welcome', self)
        new_dock.setWidget(page)
        self.addDockWidget(Qt.TopDockWidgetArea, new_dock)
        self.dock_pages.append(new_dock)

    def check_cmd_args(self):
        argv = QCoreApplication.arguments()
        if len(argv) > 1:
            if os.path.exists(argv[1]):
                qDebug(b'opening file from command line (could be file drop on executable)')
                self.externalFile.emit(argv[1])
            else:
                QMessageBox.information(self, 'Error', 'Invalid file', QMessageBox.Ok)
        else:
            # create untitled new file
            # self.addNewEditor(None)
            self.add_welcome_page()
