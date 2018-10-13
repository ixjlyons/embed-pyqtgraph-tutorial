from PyQt5 import QtGui
import application

fname = 'screenshot.png'

if __name__ == '__main__':
    app = QtGui.QApplication([])
    widget = application.CustomWidget()
    pixmap = QtGui.QPixmap(widget.size())
    widget.render(pixmap)
    pixmap.save(fname)
