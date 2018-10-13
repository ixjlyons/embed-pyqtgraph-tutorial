# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'template.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CustomWidget(object):
    def setupUi(self, CustomWidget):
        CustomWidget.setObjectName("CustomWidget")
        CustomWidget.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(CustomWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.plotWidget = PlotWidget(CustomWidget)
        self.plotWidget.setObjectName("plotWidget")
        self.gridLayout.addWidget(self.plotWidget, 0, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(CustomWidget)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)

        self.retranslateUi(CustomWidget)
        QtCore.QMetaObject.connectSlotsByName(CustomWidget)

    def retranslateUi(self, CustomWidget):
        _translate = QtCore.QCoreApplication.translate
        CustomWidget.setWindowTitle(_translate("CustomWidget", "Form"))
        self.checkBox.setText(_translate("CustomWidget", "Mouse Enabled"))

from pyqtgraph import PlotWidget
