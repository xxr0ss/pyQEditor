from PySide6.QtCore import Qt, Signal, Slot, QCoreApplication, qDebug  # for enum flags
from PySide6.QtWidgets import QMainWindow, QFileDialog, QDockWidget, QMessageBox, QTabWidget, QWidget
from .editor.codeEditorWidget import CodeEditorWidget
from .welcomePage import WelcomePage
from .editor.tabsManager import TabsManager
import os

from .ui.ui_mainwindow import Ui_mainWindow


class MainWindow(QMainWindow):
    # Signals
    externalFile = Signal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('No File')

        self.tabs_manager = TabsManager(parent=self)
        self.editor_tabs_dock = self.add_dock_tab_manager(self.tabs_manager)

        self.check_cmd_args()

    @Slot()
    def on_actionNew_triggered(self):
        self.make_sure_tabs_dock_visible()
        new_editor = CodeEditorWidget(parent=self.editor_tabs_dock, filepath=None)
        self.tabs_manager.add_editor_tab(new_editor, new_editor.get_file_base_name())

    @Slot()
    def on_actionOpen_triggered(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File')
        tabs = self.tabs_manager.tabs

        if filename[0] == '':
            return

        # check if already opened
        for i in range(tabs.count()):
            page = tabs.widget(i)
            if isinstance(page, CodeEditorWidget):
                if page.filepath == filename[0]:
                    return

        self.make_sure_tabs_dock_visible()
        self.tabs_manager.add_editor_tab(ce := CodeEditorWidget(self.editor_tabs_dock, filename[0]),
                                         ce.get_file_base_name())

    @Slot()
    def on_actionSave_triggered(self):
        tabs = self.tabs_manager.tabs
        editor = tabs.currentWidget()
        if not isinstance(editor, CodeEditorWidget):
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
        tabs.setTabText(tabs.currentIndex(), editor.get_file_base_name())
        editor.need_saving = False

    @Slot()
    def close_editor_tabs(self, dock_tabs: QDockWidget):
        dock_tabs.close()

    def make_sure_tabs_dock_visible(self):
        if self.editor_tabs_dock.isHidden():
            self.editor_tabs_dock.show()

    def add_dock_tab_manager(self, tabs_mgr: TabsManager) -> QDockWidget:
        dock = QDockWidget('', self)
        dock.setWidget(tabs_mgr.tabs)
        dock.resize(self.size())
        # dock.setFeatures(~QDockWidget.DockWidgetClosable)

        self.addDockWidget(Qt.TopDockWidgetArea, dock)

        tabs_mgr.tabs_empty.connect(lambda: self.close_editor_tabs(dock))
        self.externalFile.connect(
            lambda filepath: tabs_mgr.add_editor_tab(
                t := CodeEditorWidget(parent=dock, filepath=filepath),
                t.get_file_base_name()))

        return dock

    def add_welcome_page(self):
        page = WelcomePage(self)
        page.resize(self.size())
        self.tabs_manager.add_editor_tab(page, 'Welcome')

    def check_cmd_args(self):
        argv = QCoreApplication.arguments()
        if len(argv) > 1:
            if os.path.exists(argv[1]):
                qDebug(b'opening file from command line (could be file drop on executable)')
                self.externalFile.emit(argv[1])
            else:
                QMessageBox.information(self, 'Error', 'Invalid file', QMessageBox.Ok)
        else:
            self.add_welcome_page()
