# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './template.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CustomWidget(object):
    def setupUi(self, CustomWidget):
        CustomWidget.setObjectName(_fromUtf8("CustomWidget"))
        CustomWidget.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(CustomWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plotWidget = PlotWidget(CustomWidget)
        self.plotWidget.setObjectName(_fromUtf8("plotWidget"))
        self.gridLayout.addWidget(self.plotWidget, 0, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(CustomWidget)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)

        self.retranslateUi(CustomWidget)
        QtCore.QMetaObject.connectSlotsByName(CustomWidget)

    def retranslateUi(self, CustomWidget):
        CustomWidget.setWindowTitle(_translate("CustomWidget", "Form", None))
        self.checkBox.setText(_translate("CustomWidget", "Mouse Enabled", None))

from pyqtgraph import PlotWidget
