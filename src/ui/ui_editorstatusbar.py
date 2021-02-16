# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editorstatusbar.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_editorStatusBar(object):
    def setupUi(self, editorStatusBar):
        if not editorStatusBar.objectName():
            editorStatusBar.setObjectName(u"editorStatusBar")
        editorStatusBar.resize(429, 31)
        self.horizontalLayoutWidget = QWidget(editorStatusBar)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 431, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(60, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.cursorPos = QLabel(self.horizontalLayoutWidget)
        self.cursorPos.setObjectName(u"cursorPos")
        self.cursorPos.setMinimumSize(QSize(10, 10))

        self.horizontalLayout.addWidget(self.cursorPos)


        self.retranslateUi(editorStatusBar)

        QMetaObject.connectSlotsByName(editorStatusBar)
    # setupUi

    def retranslateUi(self, editorStatusBar):
        editorStatusBar.setWindowTitle(QCoreApplication.translate("editorStatusBar", u"Form", None))
        self.cursorPos.setText(QCoreApplication.translate("editorStatusBar", u"1:1", None))
    # retranslateUi

