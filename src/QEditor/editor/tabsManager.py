from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QWidget, QTabWidget, QMessageBox
from ..welcomePage import WelcomePage
from ..editor.codeEditorWidget import CodeEditorWidget


class TabsManager(QObject):
    modified_flag = ' *'

    def __init__(self, parent):
        super(TabsManager, self).__init__()
        self.parent = parent
        self._tabs = QTabWidget()
        self._tabs.setTabPosition(QTabWidget.North)
        self._tabs.setTabsClosable(True)  # so that there will be a 'X' on tab for closing
        self._tabs.tabCloseRequested.connect(self.remove_editor_tab)
        self._tabs.setMovable(True) # make tabs movable (their order can be changed)

    @property
    def tabs(self):
        return self._tabs

    def add_editor_tab(self, widget: QWidget, title: str):
        # auto remove welcome page by default when opened new tab
        if self._tabs.count() == 1:
            if isinstance(self._tabs.widget(0), WelcomePage):
                self._tabs.removeTab(0)
        if isinstance(widget, CodeEditorWidget):
            # mark tab as modified when content of editor changed
            widget.content_status_changed.connect(lambda need_saving: self.update_tab_status(widget, need_saving))
            idx = self._tabs.addTab(widget, title)
            self._tabs.setCurrentIndex(idx)
        elif isinstance(widget, WelcomePage):
            self._tabs.addTab(widget, title)

    @Slot()
    def remove_editor_tab(self, index):
        tab = self._tabs.widget(index)
        if isinstance(tab, CodeEditorWidget):
            if tab.need_saving:
                button = QMessageBox.warning(tab, 'Close tab', 'Do you want to save changes?',
                                             QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel)
                if button == QMessageBox.Ok:
                    self.parent.on_actionSave_triggered()
                    if tab.need_saving:
                        # opened save file fileDialog but not actually saved
                        QMessageBox.information(tab, 'Information', 'File not saved', QMessageBox.Ok)
                        return
                elif button == QMessageBox.No:
                    pass
                elif button == QMessageBox.Cancel:
                    return
                else:
                    pass
                    # it's not possible to reach here right?

        self._tabs.removeTab(index)

    @Slot()
    def update_tab_status(self, w: CodeEditorWidget, need_saving: bool):
        idx = self._tabs.indexOf(w)
        text = self._tabs.tabText(idx)
        if need_saving:
            if text.endswith(self.modified_flag):
                return
            text += self.modified_flag
        else:
            # because this slot is called when code editor changes, so there's
            # no need to set its 'need_saving' status back to False
            text.removesuffix(self.modified_flag)
        self._tabs.setTabText(idx, text)
