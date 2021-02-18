from PySide6.QtCore import Qt, Signal, Slot, QCoreApplication, qDebug, QObject  # for enum flags
from PySide6.QtWidgets import QMainWindow, QFileDialog, QDockWidget, QMessageBox, QTabWidget, QWidget
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

        self.editor_tabs_dock = QDockWidget('', self)
        self.editor_tabs = QTabWidget(self)
        self.editor_tabs_dock.setWidget(self.editor_tabs)
        self.editor_tabs_dock.resize(self.size())
        self.editor_tabs.setTabPosition(QTabWidget.North)
        self.addDockWidget(Qt.TopDockWidgetArea, self.editor_tabs_dock)

        self.externalFile.connect(
            lambda filepath: self.add_editor_tab(t := CodeEditor(self.editor_tabs_dock, filepath=filepath), t.get_file_base_name()))
        self.check_cmd_args()

    @Slot()
    def on_actionNew_triggered(self):
        new_editor = CodeEditor(self.editor_tabs_dock, filepath=None)
        self.add_editor_tab(new_editor, new_editor.get_file_base_name())

    @Slot()
    def on_actionOpen_triggered(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File')
        if filename[0] != '':
            # check if already opened
            for i in range(self.editor_tabs.count()):
                page = self.editor_tabs.widget(i)
                if isinstance(page, CodeEditor):
                    if page.filepath == filename[0]:
                        return

            self.add_editor_tab(ce := CodeEditor(self.editor_tabs_dock, filename[0]), ce.get_file_base_name())

    @Slot()
    def on_actionSave_triggered(self):
        editor = self.editor_tabs.currentWidget()
        if not isinstance(editor, CodeEditor):
            return

        if editor.is_new_file():
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
        self.editor_tabs.setTabText(self.editor_tabs.currentIndex(), editor.get_file_base_name())

    def add_editor_tab(self, widget: QWidget, title: str):
        self.editor_tabs.addTab(widget, title)

    def add_welcome_page(self):
        # TODO: add welcome page (like vscode)
        page = WelcomePage(self)
        self.add_editor_tab(page, 'Welcome')

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
