from PySide6.QtCore import QEvent, QObject, QSize, Qt, Signal, Slot
from PySide6.QtGui import QEnterEvent, QIcon, QPaintEvent, QPainter, QPixmap
from PySide6.QtWidgets import QAbstractButton, QPushButton, QStyle, QStyleOption, QStyleOptionButton, QTabBar, QWidget, \
    QTabWidget, QMessageBox
from ..welcomePage import WelcomePage
from ..editor.codeEditorWidget import CodeEditorWidget
from ..rc_icons import *


class TabsManager(QObject):
    modified_flag = ' *'
    side_enum = [QTabBar.ButtonPosition.LeftSide, QTabBar.ButtonPosition.RightSide]

    tabs_empty = Signal()

    def __init__(self, parent):
        super(TabsManager, self).__init__()
        self.parent = parent
        self._tabs = QTabWidget()
        self._tabs.setTabPosition(QTabWidget.North)
        # so that there will be a 'X' on tab for closing
        self._tabs.setTabsClosable(True)
        self._tabs.tabCloseRequested.connect(self.remove_editor_tab)
        # make tabs movable (their order can be changed)
        self._tabs.setMovable(True)

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
            widget.content_status_changed.connect(
                lambda need_saving: self.update_tab_status(widget, need_saving))

        idx = self._tabs.addTab(widget, title)
        self._tabs.setCurrentIndex(idx)

        # use customized Close Button
        close_side = self.side_enum[widget.style().styleHint(
            QStyle.SH_TabBar_CloseButtonPosition, None, widget)]
        self._tabs.tabBar().setTabButton(idx, close_side, btn := CloseButton(self._tabs.tabBar()))
        btn.clicked.connect(lambda: self._tabs.tabCloseRequested.emit(idx))

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
                        QMessageBox.information(
                            tab, 'Information', 'File not saved', QMessageBox.Ok)
                        return
                elif button == QMessageBox.No:
                    pass
                elif button == QMessageBox.Cancel:
                    return
                else:
                    pass
                    # it's not possible to reach here right?

        self._tabs.removeTab(index)
        if self._tabs.count() == 0:
            self.tabs_empty.emit()

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


class CloseButton(QAbstractButton):
    def __init__(self, parent: QWidget):
        super(CloseButton, self).__init__(parent)
        self.parent = parent
        self.setFocusPolicy(Qt.NoFocus)
        self.resize(self.sizeHint())
        self.setEnabled(True)
        self.clicked.connect(self.log_clicked)

    @Slot()
    def log_clicked(self):
        print('Close Button clicked')

    def sizeHint(self) -> QSize:
        self.ensurePolished()
        width = self.style().pixelMetric(QStyle.PM_TabCloseIndicatorWidth, None, self)
        height = self.style().pixelMetric(QStyle.PM_TabCloseIndicatorHeight, None, self)
        return QSize(width, height)

    def minimumSizeHint(self) -> QSize:
        return self.sizeHint()

    def enterEvent(self, event: QEnterEvent) -> None:
        if self.isEnabled():
            self.update()
        QAbstractButton.enterEvent(self, event)

    def leaveEvent(self, event: QEvent) -> None:
        if self.isEnabled():
            self.update()
        QAbstractButton.leaveEvent(self, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        option = QStyleOption()
        option.initFrom(self)
        if self.isEnabled() and self.underMouse() and not self.isCheckable() and not self.isDown():
            option.state |= QStyle.State_Raised
        if self.isChecked():
            option.state |= QStyle.State_On
        if self.isDown():
            option.state |= QStyle.State_Sunken

        tb: QTabBar = self.parent
        if isinstance(tb, QTabBar):
            index = tb.currentIndex()
            position = TabsManager.side_enum[tb.style().styleHint(QStyle.SH_TabBar_CloseButtonPosition, None, tb)]
            if tb.tabButton(index, position):
                option.state |= QStyle.State_Selected

        p = QPainter(self)
        self.style_draw(option, p)

    def style_draw(self, option: QStyleOption, p: QPainter):
        # 移植PE_IndicatorTabClose
        size = self.style().proxy().pixelMetric(QStyle.PM_SmallIconSize, option)
        mode: QIcon.Mode = (QIcon.Active if option.state & QStyle.State_Raised else QIcon.Normal) \
            if option.state & QStyle.State_Enabled else QIcon.Disabled
        if not option.state & QStyle.State_Raised \
                and not option.state & QStyle.State_Sunken \
                and not option.state & QStyle.State_Selected:
            mode = QIcon.Disabled

        state: QIcon.State = QIcon.On if option.state & QStyle.State_Sunken else QIcon.Off
        pixmap = CloseButton.tabBar_close_button_icon().pixmap(QSize(size, size), self.devicePixelRatio(), mode, state)
        self.style().proxy().drawItemPixmap(p, option.rect, Qt.AlignCenter, pixmap)

    @staticmethod
    def tabBar_close_button_icon() -> QIcon:
        icon = QIcon()
        # add
        icon.addPixmap(QPixmap(':/default/icons/ui/closeButton.png'), QIcon.Normal, QIcon.Off)
        icon.addPixmap(QPixmap(':/default/icons/ui/closeButton_down.png'), QIcon.Normal, QIcon.On)
        icon.addPixmap(QPixmap(':/default/icons/ui/closeButton_hover.png'), QIcon.Active, QIcon.Off)
        return icon
