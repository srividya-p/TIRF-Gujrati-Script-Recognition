from PyQt5 import QtCore, QtGui, QtWidgets


class Image(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Image, self).__init__(parent)
        self.image = QtGui.QPixmap("./images/kitten1.jpg")
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(QtCore.QPoint(), self.image)
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine))
        painter.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() and QtCore.Qt.LeftButton:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == QtCore.Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()

    def sizeHint(self):
        return self.image.size()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = Image()
        self.textedit = QtWidgets.QTextEdit()

        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        lay = QtWidgets.QHBoxLayout(widget)
        lay.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        lay.addWidget(self.textedit)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
