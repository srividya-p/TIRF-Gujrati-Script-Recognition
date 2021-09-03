import sys
import calendar
import time
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2
import numpy as np

from suppress_qtw import suppress_qt_warnings

class Image(QWidget):
    def __init__(self, path, parent=None):
        super(Image, self).__init__(parent)
        self.image = QPixmap(path).scaled(600, 600, QtCore.Qt.KeepAspectRatio)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.path='./images/placeholder.jpg'

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QtCore.QPoint(), self.image)
        painter.setPen(QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine))
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
        name, ok = QInputDialog.getText(self,"Annotation Name","Enter Annotation Name:")
        if name and ok:
            self.save_image_coords(self.begin.x(), self.begin.y(), self.end.x(), self.end.y(), name)

    def sizeHint(self):
        return self.image.size()

    def save_image_coords(self, x1, y1, x2, y2, annotation):
        filename = os.path.basename(self.path)
        filename = filename[:filename.index('.')]
        img_arr = self.convertQImageToMat(self.image)
        
        annotated_img = cv2.rectangle(img_arr, (x1, y1), (x2, y2), (255, 0, 0), 2)
        annotated_img = cv2.putText(annotated_img, annotation, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        cv2.imwrite('./crops/'+filename+'.png', annotated_img)
        self.updateImage('./crops/'+filename+'.png')

        coords_file = open('./crops/'+filename+'.txt', 'a')
        coords_file.write('annotation:'+annotation+'\n')
        for coord in [x1, y1, x2, y2]:
            coords_file.write(str(coord)+'\n')
        coords_file.write('\n')
        coords_file.close()

        msg = QMessageBox()
        msg.setWindowTitle('Save Coordinates')
        msg.setText('Coordinates saved Successfully!')
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def updateImage(self, path):
        self.image = QPixmap(path).scaled(600, 600, QtCore.Qt.KeepAspectRatio)
        self.path = path
        self.update()

    def convertQImageToMat(self, incomingImage):
        incomingImage = incomingImage.toImage().convertToFormat(4)

        width = incomingImage.width()
        height = incomingImage.height()

        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  
        return arr


class BC_Homepage(QWidget):
    def __init__(self, parent=None):
        super(BC_Homepage, self).__init__(parent)

        self.currFile = './images/placeholder.jpg'

        # Buttons
        self.openButton = QPushButton('Open')
        self.openButton.clicked.connect(self.show_image)
        self.openButton.setStyleSheet(
            'background-color : blue; color: white; height:25px')
        self.openButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Image
        self.image_frame = Image("/home/pika/Desktop/TIFR/box-crop/images/placeholder.jpg")
        self.image_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Layouts
        self.im_grid = QVBoxLayout()
        self.im_grid.addWidget(self.image_frame, alignment=QtCore.Qt.AlignCenter)
        self.im_grid.addWidget(self.openButton,alignment=QtCore.Qt.AlignCenter)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.im_grid)
        
        self.setLayout(self.main_layout)

        self.setWindowTitle("Box Crop")
        self.show()

    def show_image(self):
        filename, _ = QFileDialog().getOpenFileName(self, 'Select an Image',
                                                    '.', 'Image Files (*.jpg *.jpeg *.png *.svg)')

        if filename == '':
            print('Error reading File!')
            return

        self.image_frame.updateImage(filename)
        self.currFile = filename


if __name__ == '__main__':
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    display_image_widget = BC_Homepage()
    display_image_widget.show()
    sys.exit(app.exec_())
