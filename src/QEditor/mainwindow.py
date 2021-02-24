from PySide6.QtCore import Qt, Signal, Slot, QCoreApplication, qDebug  # for enum flags
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QLabel, QSplitter
from PySide6.QtGui import QCloseEvent
from .editor.codeEditorWidget import CodeEditorWidget
from .welcomePage import WelcomePage
from .editor.tabsManager import TabsManager
from .sideBar import SideBar, FolderExplorer
import os

from .ui.ui_mainwindow import Ui_mainWindow


class MainWindow(QMainWindow):
    # Signals
    external_file = Signal(str)     # arg from commandline
    external_dir = Signal(str)      # arg from commandline

    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('No File')

        self.tabs_manager = TabsManager(self)

        self.side_bar: SideBar = None
        self.init_side_bar()
        self.folder_explorer = self.side_bar.folder_explorer
        self.folder_explorer.file_clicked.connect(self.open_file_in_tabs)

        self.init_tabs_widget()
        self.init_status_bar()

        self.main_splitter = self.init_main_splitter()
        self.setCentralWidget(self.main_splitter)
        self.check_cmd_args()

    @Slot()
    def on_actionNew_File_triggered(self):
        # TODO 这样访问会不会太直接？要不要把创建CodeEditorWidget封装在tabs_manager?
        new_editor = CodeEditorWidget(parent=self, filepath=None)
        self.tabs_manager.add_editor_tab(new_editor, new_editor.windowTitle())

    @Slot()
    def on_actionOpen_File_triggered(self):
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

        ce = CodeEditorWidget(self, filename[0])
        self.tabs_manager.add_editor_tab(ce, ce.windowTitle())

    @Slot()
    def on_actionOpen_Folder_triggered(self):
        opened_dir = QFileDialog.getExistingDirectory(self, 'Open Folder')
        if opened_dir == '':
            return

        folder = self.folder_explorer
        folder.open_folder(opened_dir)
        folder.show()

    @Slot()
    def on_actionSave_triggered(self):
        tabs = self.tabs_manager.tabs
        tab = tabs.currentWidget()
        self.save_editor_tab(tab)
        tabs.setTabText(tabs.currentIndex(), tab.get_file_base_name())

    def save_editor_tab(self, tab):
        """
        Save tab's content if the tab holds contents, for now: the CodeEditorWidget
        :param tab: widget from tabWidgets
        """
        if not isinstance(tab, CodeEditorWidget):
            return

        if tab.is_new_file():
            # new file to save
            name = QFileDialog.getSaveFileName(self, 'Save File', tab.windowTitle())
            if name[0] == '':
                return
            filepath = name[0]
        else:
            filepath = tab.filepath

        with open(filepath, 'wb') as f:
            f.write(tab.get_content())

        tab.filepath = filepath
        tab.need_saving = False

    @Slot()
    def update_window_title(self, index=-1):
        if index == -1:
            self.setWindowTitle('QEditor')
        else:
            current_tab = self.tabs_manager.tabs.widget(index)
            if current_tab is not None:
                self.setWindowTitle(self.tabs_manager.tabs.tabText(index))

    @Slot()
    def open_file_in_tabs(self, filename):
        self.tabs_manager.add_editor_tab(
            ce := CodeEditorWidget(self, filename),
            ce.windowTitle())

    def init_side_bar(self):
        self.side_bar = SideBar(self)
        self.addToolBar(Qt.LeftToolBarArea, self.side_bar)

    def init_tabs_widget(self):
        self.setCentralWidget(self.tabs_manager.tabs)
        self.external_file.connect(self.add_editor_with_check)
        self.tabs_manager.tabs.currentChanged.connect(self.update_window_title)

    def init_status_bar(self):
        status_bar = self.statusBar()
        cur_pos_label = QLabel()
        cur_pos_label.setText('0, 0')
        status_bar.addPermanentWidget(cur_pos_label)
        self.tabs_manager.cursor_pos_change.connect(
            lambda pos: cur_pos_label.setText(f'{pos[0]}:{pos[1]}')
        )

    def init_main_splitter(self):
        assert self.side_bar is not None

        splitter = QSplitter(self)
        splitter.addWidget(self.side_bar.widget_current)
        splitter.addWidget(self.tabs_manager.tabs)
        splitter.setCollapsible(0, True)
        splitter.setCollapsible(1, False)
        self.folder_explorer.setVisible(False)

        return splitter

    def brand_new_startup(self):
        # opened this application with out specifying target dir or something
        page = WelcomePage(self)
        self.tabs_manager.add_editor_tab(page, 'Welcome')

    def check_cmd_args(self):
        argv = QCoreApplication.arguments()
        if len(argv) > 1:
            if os.path.exists(path := argv[1]):
                if os.path.isfile(path):
                    self.external_file.emit(path)
                elif os.path.isdir(path):
                    self.external_dir.emit(path)
                else:
                    # TODO: what could here be?
                    pass
            else:
                QMessageBox.information(self, 'Error', 'Invalid commandline arguments', QMessageBox.Ok)
        else:
            self.brand_new_startup()

    @Slot()
    def add_editor_with_check(self, filepath) -> bool:
        """
        add editor tab if the file is not on tabs list
        :param filepath: filepath to open
        :return: if new editor added
        """
        for tab in self.tabs_manager.all_widgets:
            if not isinstance(tab, CodeEditorWidget):
                continue
            if tab.filepath == filepath:
                return False
        self.tabs_manager.add_editor_tab(
            t := CodeEditorWidget(parent=self, filepath=filepath),
            t.windowTitle())
        return True

    def closeEvent(self, event: QCloseEvent) -> None:
        # when close application with tabs at 'need_saving' status, will prompt
        tabs_mgr = self.tabs_manager
        if tabs_mgr.any_tab_needs_saving():
            unhandled_widgets = tabs_mgr.all_widgets
            for w in unhandled_widgets:
                if not tabs_mgr.remove_editor_tab(tabs_mgr.tabs.indexOf(w)):
                    # canceled
                    event.ignore()
                    return
        event.accept()
