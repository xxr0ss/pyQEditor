# inspired by Qt's example codeeditor
#
# Copyright (C) 2019 The Qt Company Ltd.
# Contact: http://www.qt.io/licensing/
#


from PySide6.QtCore import Slot, Qt, QRect, QSize
from PySide6.QtGui import QColor, QPainter, QTextFormat, QPaintEvent, QResizeEvent
from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit


class LineNumberArea(QWidget):
    def __init__(self, editor):
        QWidget.__init__(self, editor)
        self.codeEditor = editor

    # override
    # get line number area width by calculating max(line number)
    def sizeHint(self) -> QSize:
        return QSize(self.codeEditor.line_number_area_width(), 0)

    # override
    # deal with paintEvent in CodeEditor
    def paintEvent(self, event: QPaintEvent) -> None:
        self.codeEditor.lineNumberAreaPaintEvent(event)


# TODO add Editor Info Area, for example: cursor position, encoding, tab length, LF/CRLF


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        QPlainTextEdit.__init__(self)
        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged[int].connect(self.update_line_number_area_width)
        self.updateRequest[QRect, int].connect(self.udpate_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

    def line_number_area_width(self):
        max_num = max(1, self.blockCount())
        digits = len(str(max_num))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def resizeEvent(self, event: QResizeEvent) -> None:
        pass

    def lineNumberAreaPaintEvent(self, event: QPaintEvent):
        pass

    @Slot
    def update_line_number_area_width(self, newBlockCount):
        pass

    @Slot
    def update_line_number_area(self, rect: QRect, dy: int):
        pass

    @Slot
    def highlight_current_line(self):
        pass
