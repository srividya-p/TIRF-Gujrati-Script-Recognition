import sys
import calendar
import time
import os
import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2
import numpy as np

from suppress_qtw import suppress_qt_warnings


class Image(QWidget):
    def __init__(self, path, parent=None):
        super(Image, self).__init__(parent)
        self.image = QPixmap(path)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.path = './images/placeholder.jpg'

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QtCore.QPoint(), self.image)
        painter.setPen(QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine))
        painter.drawRect(QtCore.QRect(self.begin, self.end))

    def sizeHint(self):
        return self.image.size()

    def plotBoxes(self, anPath, charIndex, char, all):
        filename = os.path.basename(anPath)
        filename = filename[:filename.index('.')]
        
        img_arr = self.convertQImageToMat(self.image)
        annotated_img = img_arr
        h = img_arr.shape[0]
        w = img_arr.shape[1]

        xcen, ycen, wa, ha = 0, 0, 0, 0

        a_file = open(anPath)
        heights = []
        for line in a_file.readlines():
            l_array = line.split(' ')
            if l_array[0] != str(charIndex) and not all and l_array[0] != char:
                continue
            
            if(len(l_array) == 5):
                x1, y1, x2, y2 = l_array
            else:
                # xcen, ycen, wa, ha = l_array[2:]
                x1, y1, x2, y2 = l_array

            # x1 = max(float(xcen) - float(wa) / 2, 0)
            # x2 = min(float(xcen) + float(wa) / 2, 1)
            # y1 = max(float(ycen) - float(ha) / 2, 0)
            # y2 = min(float(ycen) + float(ha) / 2, 1)


            # x1 = int(w * x1)
            # x2 = int(w * x2)
            # y1 = int(h * y1)
            # y2 = int(h * y2)

            # heights.append(float(ha))

            annotated_img = cv2.rectangle(
                img_arr, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 1)

        
        cv2.imwrite('./annotations/'+filename+'.jpg', annotated_img)
        self.updateImage('./annotations/'+filename+'.jpg')

        # avg_font_ratio = sum(heights) / len(heights)
        print(filename)
        # print("Average Font Ratio = "+str(avg_font_ratio))
        # print("Average Font = "+str(avg_font_ratio * h))
        print()

    def updateImage(self, path):
        self.image = QPixmap(path)
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
        self.targetPath = 'Null'
        self.charMapping = dict()
        self.setCharMapping()

        # Side Input
        self.charInput = QLineEdit()

        # Buttons
        self.openButton = QPushButton('Open')
        self.openButton.clicked.connect(self.show_image)
        self.openButton.setStyleSheet(
            'background-color : blue; color: white; height:25px;font-size: 16px;')
        self.openButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.pathButton = QPushButton('Path')
        self.pathButton.clicked.connect(self.set_path)
        self.pathButton.setStyleSheet(
            'background-color : green; color: white; height:25px;font-size: 16px;')
        self.pathButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.plotButton = QPushButton('Plot')
        self.plotButton.clicked.connect(self.plot_char_instances)
        self.plotButton.setStyleSheet(
            'background-color : purple; color: white; height:25px;font-size: 16px;')
        self.plotButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.plotAllButton = QPushButton('Plot All')
        self.plotAllButton.clicked.connect(self.plot_char_instances)
        self.plotAllButton.setStyleSheet(
            'background-color : orange; color: black; height:25px;font-size: 16px;')
        self.plotAllButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.clearButton = QPushButton('Clear')
        self.clearButton.clicked.connect(self.clear_annotations)
        self.clearButton.setStyleSheet(
            'background-color : red; color: white; height:25px;font-size: 16px;')
        self.clearButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Image
        self.image_frame = Image(
            "/home/pika/Desktop/TIFR/Assignments/box-crop/images/placeholder.jpg")
        self.image_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Text
        self.pathLabel = QLabel("Current Target Path: " + self.targetPath)
        self.pathLabel.setStyleSheet("font-size: 16px; margin-top:20px")

        # Layouts
        self.bt_grid = QHBoxLayout()
        self.bt_grid.addWidget(
            self.openButton, alignment=QtCore.Qt.AlignCenter)
        self.bt_grid.addWidget(
            self.pathButton, alignment=QtCore.Qt.AlignCenter)
        self.bt_grid.addWidget(
            self.plotButton, alignment=QtCore.Qt.AlignCenter)
        self.bt_grid.addWidget(
            self.plotAllButton, alignment=QtCore.Qt.AlignCenter)
        self.bt_grid.addWidget(
            self.clearButton, alignment=QtCore.Qt.AlignCenter)

        self.im_grid = QVBoxLayout()
        self.im_grid.addWidget(
            self.image_frame, alignment=QtCore.Qt.AlignCenter)
        self.im_grid.addLayout(self.bt_grid)
        self.im_grid.addWidget(self.pathLabel)

        # Main Layout
        self.main_grid = QGridLayout()
        self.main_grid.addLayout(self.im_grid, 0, 0)

        self.setLayout(self.main_grid)
        self.setWindowTitle("Plot Annotations")
        self.show()

    def setCharMapping(self):
        space_names_path = './space.names'
        space_names_file = open(space_names_path, 'r')
        chars = space_names_file.readlines()
        char_index_map = dict()

        i = 0
        for char in chars:
            char_index_map[char.replace('\n', '')] = i
            i += 1
        self.charMapping = char_index_map

    def show_image(self):
        default = '/home/pika/Downloads/GSR-Downloads/Tests' if self.targetPath == 'Null' else self.targetPath

        filename, _ = QFileDialog().getOpenFileName(self, 'Select an Image',
                                                    default, 'Image Files (*.jpg *.jpeg *.png *.svg)')

        if filename == '':
            print('Error reading File!')
            return

        self.image_frame.updateImage(filename)
        self.currFile = filename

    def set_path(self):
        filename = QFileDialog().getExistingDirectory(
            self, 'Select a Folder', '/home/pika/Downloads/GSR-Downloads')

        if(filename == ''):
            return

        self.targetPath = filename
        self.pathLabel.setText('Current Path: '+self.targetPath)

    def plot_char_instances(self):
        if 'placeholder' in self.currFile:
            return

        if self.targetPath == 'Null':
            return

        filename = os.path.basename(self.currFile)
        filename = filename.replace(filename[filename.index('.'):], '')

        dataset_files = os.listdir(self.targetPath)
        annotation_file = list(
            filter(lambda file: filename+'.txt' == file, dataset_files))[0]

        if self.sender().text() == 'Plot All':
            self.image_frame.plotBoxes(self.targetPath+'/'+annotation_file, -1, -1, True)
        else:
            char, ok = QInputDialog.getText(self, "Character", "Enter Character:")
            if not char or not ok:
                return

            char = char.replace(char[1:], '')
            if(char not in self.charMapping.keys()):
                msg = QMessageBox()
                msg.setWindowTitle('Warning')
                msg.setText('The models are not trained for this Character!')
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
            
            self.image_frame.plotBoxes(self.targetPath+'/'+annotation_file, self.charMapping[char],char, False)
    
    def clear_annotations(self):
        self.image_frame.updateImage(self.currFile)

if __name__ == '__main__':
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    display_image_widget = BC_Homepage()
    display_image_widget.show()
    sys.exit(app.exec_())
