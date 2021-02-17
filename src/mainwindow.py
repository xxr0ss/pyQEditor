from PySide6.QtCore import Qt, Signal, Slot, QCoreApplication, qDebug, QObject  # for enum flags
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

        self.externalFile.connect(self.add_new_dock_editor)
        # TODO remove dock widget at its closeEvent or something
        self.current_dock_editor: QDockWidget = None

        # set dock tabs position north
        self.setTabPosition(Qt.TopDockWidgetArea, QTabWidget.North)

        self.check_cmd_args()

    @Slot()
    def on_actionNew_triggered(self):
        self.add_new_dock_editor(None)

    @Slot()
    def on_actionOpen_triggered(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File')
        if filename[0] != '':
            # check if already opened
            for dock in self.dock_pages:
                widget = dock.widget()
                if not isinstance(widget, CodeEditor):
                    continue
                if widget.filepath == filename[0]:
                    # same file opened
                    return

            self.add_new_dock_editor(filename[0])
    
    @Slot()
    def on_actionSave_triggered(self):
        if self.current_dock_editor is None:
            print('[x] current editor is none')
            return

        editor: CodeEditor = self.current_dock_editor.widget()

        if editor.__title__ == CodeEditor.untitled:
            # new file to save
            name = QFileDialog.getSaveFileName(self, 'Save File')
            if name[0] == '':
                return
            filepath = name[0]
        else:
            filepath = editor.filepath

        with open(filepath, 'wb') as f:
            f.write(editor.get_content())
        editor.filepath = filepath
        # TODO update editor title

    # @Slot(bool)
    def update_dock_status(self, visible: bool):
        sender: QDockWidget = self.sender()
        if visible:
            self.current_dock_editor: CodeEditor = sender.widget()
            print(self.current_dock_editor.__title__)

    def add_new_dock_editor(self, filepath):
        editor = CodeEditor(self, filepath)
        new_dock_editor = QDockWidget(editor.__title__, self)
        new_dock_editor.setWidget(editor)
        self.addDockWidget(Qt.TopDockWidgetArea, new_dock_editor)
        if len(self.dock_pages) != 0:
            self.tabifyDockWidget(self.dock_pages[-1], new_dock_editor)
        self.dock_pages.append(new_dock_editor)

        new_dock_editor.visibilityChanged[bool].connect(self.update_dock_status)

        new_dock_editor.show()
        new_dock_editor.raise_()
        self.current_dock_editor = new_dock_editor

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
