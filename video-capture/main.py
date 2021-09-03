import sys
import time
import calendar
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from suppress_qtw import suppress_qt_warnings
from video_player import VideoPlayer
from capture_av import *

class VC_Homescreen(QWidget):
    def __init__(self, parent=None):
        super(VC_Homescreen, self).__init__(parent)

        self.is_recording = False
        self.disply_width = 640
        self.display_height = 480
        self.im = QPixmap("./video.png")
        self.image_label = QLabel()
        self.image_label.setPixmap(self.im)

        self.startButton = QPushButton()
        self.startButton.setIcon(self.style().standardIcon(QStyle.SP_DriveDVDIcon))
        self.startButton.setStyleSheet('color:white; background-color:green; height:25px')
        self.startButton.clicked.connect(self.capture_video)

        self.stopButton = QPushButton()
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopButton.setStyleSheet('color:white; background-color:red; height:25px')
        self.stopButton.clicked.connect(self.save_video)
        self.stopButton.setEnabled(self.is_recording)

        self.playButton = QPushButton()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.setStyleSheet('color:white; background-color:blue; height:25px')
        self.playButton.clicked.connect(self.open_video_player)

        self.im_grid = QGridLayout()
        self.im_grid.addWidget(self.image_label,1,1)

        self.b_grid = QGridLayout()
        self.b_grid.addWidget(self.startButton, 1,1)
        self.b_grid.addWidget(self.stopButton, 1,2)
        self.b_grid.addWidget(self.playButton,1,3)

        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.addLayout(self.im_grid)
        self.outer_layout.addLayout(self.b_grid)

        self.setLayout(self.outer_layout)

        self.setWindowTitle("Video Capture")
        self.show()

    def open_video_player(self):
        self.player = VideoPlayer()
        self.player.setWindowTitle("Video Player")
        self.player.resize(665, 540)
        self.player.show()

    def save_video(self):
        self.audio_thread.stop_audio_rec()
        frame_count = self.video_thread.frame_count
        elapsed_time = time.time() - self.video_thread.start_time
        recorded_fps = frame_count / elapsed_time  
        self.video_thread.stop_video_rec()

        name, _ = QFileDialog.getSaveFileName(
            self, 'Save File', str(calendar.timegm(time.gmtime()))+'.avi', 'Video Files (*.avi)')
        if name:
            stop_av_recording(name, frame_count, elapsed_time, recorded_fps)
            file_manager()
        self.image_label.setPixmap(self.im)
        self.is_recording = False
        self.stopButton.setEnabled(self.is_recording) 

        msg = QMessageBox()
        msg.setWindowTitle('Save Video')
        msg.setText('Video saved Successfully!')
        msg.setIcon(QMessageBox.Information)
        msg.exec_()


    def capture_video(self):
        if self.is_recording == False:
            self.video_thread = VideoRecorder()
            self.video_thread.change_pixmap_signal.connect(self.update_image)
            self.video_thread_obj = self.video_thread.start_video_rec()

            self.audio_thread = AudioRecorder()
            self.audio_thread_obj = self.audio_thread.start_audio_rec() 

            self.is_recording = True   
            self.stopButton.setEnabled(self.is_recording) 
        
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

if __name__ == '__main__':
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    ex = VC_Homescreen()
    sys.exit(app.exec_())

