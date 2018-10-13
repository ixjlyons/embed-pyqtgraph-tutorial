from PyQt5 import QtGui, QtCore

# import the "form class" from your compiled UI
from template import Ui_CustomWidget


class CustomWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent=parent)

        # set up the form class as a `ui` attribute
        self.ui = Ui_CustomWidget()
        self.ui.setupUi(self)

        # access your UI elements through the `ui` attribute
        self.ui.plotWidget.plot(x=[0.0, 1.0, 2.0, 3.0],
                                y=[4.4, 2.5, 2.1, 2.2])

        # simple demonstration of pure Qt widgets interacting with pyqtgraph
        self.ui.checkBox.stateChanged.connect(self.toggleMouse)

    def toggleMouse(self, state):
        if state == QtCore.Qt.Checked:
            enabled = True
        else:
            enabled = False

        self.ui.plotWidget.setMouseEnabled(x=enabled, y=enabled)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    widget = CustomWidget()
    widget.show()
    app.exec_()
