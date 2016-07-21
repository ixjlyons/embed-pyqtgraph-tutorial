import argparse
from PyQt4 import QtGui, QtCore

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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Show a pyqtgraph plot embedded in a PyQt UI.")
    parser.add_argument('-s', '--screenshot', action='store_true',
        help="Take a screenshot of the UI instead of running it.")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    app = QtGui.QApplication([])
    widget = CustomWidget()

    if args.screenshot:
        pixmap = QtGui.QPixmap(widget.size())
        widget.render(pixmap)
        pixmap.save('screenshot.png')
    else:
        widget.show()
        app.exec_()
