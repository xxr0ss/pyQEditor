# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'codeeditor.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from editingArea import EditingArea
from editorStatusBar import EditorStatusBar


class Ui_CodeEditor(object):
    def setupUi(self, CodeEditor):
        if not CodeEditor.objectName():
            CodeEditor.setObjectName(u"CodeEditor")
        CodeEditor.resize(400, 300)
        self.verticalLayoutWidget = QWidget(CodeEditor)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(79, 39, 271, 151))
        self.editorVLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.editorVLayout.setSpacing(0)
        self.editorVLayout.setObjectName(u"editorVLayout")
        self.editorVLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.editorVLayout.setContentsMargins(0, 0, 0, 0)
        self.codeEditingArea = EditingArea(self.verticalLayoutWidget)
        self.codeEditingArea.setObjectName(u"codeEditingArea")

        self.editorVLayout.addWidget(self.codeEditingArea)

        self.statusBar = EditorStatusBar(self.verticalLayoutWidget)
        self.statusBar.setObjectName(u"statusBar")

        self.editorVLayout.addWidget(self.statusBar)


        self.retranslateUi(CodeEditor)

        QMetaObject.connectSlotsByName(CodeEditor)
    # setupUi

    def retranslateUi(self, CodeEditor):
        CodeEditor.setWindowTitle(QCoreApplication.translate("CodeEditor", u"Form", None))
    # retranslateUi

