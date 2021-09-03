import threading
import time
import subprocess
import os
import wave

import cv2
import pyaudio
import numpy as np
from PyQt5.QtCore import *

class VideoRecorder(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, fourcc="MJPG", name="temp_video.avi", camindex=0, frameSize=(640, 480), fps=30):
        super(VideoRecorder, self).__init__()
        self.open = True
        self.fps = fps
        self.video_cap = cv2.VideoCapture(camindex)
        self.fourcc = cv2.VideoWriter_fourcc(*fourcc)
        self.video_out = cv2.VideoWriter(name, self.fourcc, self.fps, frameSize)
        self.frame_count = 1
        self.start_time = time.time()
        
    def record(self):
        timer_start = time.time()
        timer_current = 0
        while self.open:
            ret, video_frame = self.video_cap.read()
            if ret:
                self.video_out.write(video_frame)
                self.frame_count += 1
                time.sleep(1/self.fps) 
                self.change_pixmap_signal.emit(video_frame)
            else:
                break

    def stop_video_rec(self):
        if self.open:
            self.open = False
            self.video_out.release()
            self.video_cap.release()
            cv2.destroyAllWindows()

    def start_video_rec(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()
        return video_thread
        

class AudioRecorder():
    def __init__(self, name="temp_audio.wav", fpb=1024, rate=44100, channels=2):
        self.open = True
        self.rate = rate
        self.frames_per_buffer = fpb
        self.channels = channels
        self.audio_filename = name
        self.format = pyaudio.paInt16
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(rate=self.rate, format=self.format,
                                      frames_per_buffer=self.frames_per_buffer,
                                      channels=self.channels, input=True)
        self.audio_frames = []

    def record(self):
        self.stream.start_stream()
        while self.open:
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)
            if not self.open:
                break
            

    def stop_audio_rec(self):
        if self.open:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            wave_file = wave.open(self.audio_filename, 'wb')
            wave_file.setnchannels(self.channels)
            wave_file.setsampwidth(self.audio.get_sample_size(self.format))
            wave_file.setframerate(self.rate)
            wave_file.writeframes(b''.join(self.audio_frames))
            wave_file.close()

    def start_audio_rec(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()
        return audio_thread

def stop_av_recording(filename, frame_count, elapsed_time, recorded_fps):
    
    print("Total Frame Count = "+str(frame_count))
    print("Elapsed Time = "+str(elapsed_time))
    print("Frames per Second = "+str(recorded_fps))

    while threading.active_count() > 2:
        time.sleep(1)

    # If FPS is higher or lower than expected then re encode.
    if abs(recorded_fps - 6) >= 0.01:
        print("Re-encoding...")
        cmd = "ffmpeg -r " + str(recorded_fps) + " -i temp_video.avi -pix_fmt yuv420p -r 6 temp_video_correct_fps.avi"
        subprocess.call(cmd, shell=True)

        print("Muxing(After Re-encoding)...")
        cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video_correct_fps.avi -pix_fmt yuv420p \"" + filename + "\""
        subprocess.call(cmd, shell=True)
    else:
        print("Muxing(Directly)...")
        cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video.avi -pix_fmt yuv420p \"" + filename + "\""
        subprocess.call(cmd, shell=True)


def file_manager():
    local_path = os.getcwd()
    if os.path.exists(str(local_path) + "/temp_audio.wav"):
        os.remove(str(local_path) + "/temp_audio.wav")
    if os.path.exists(str(local_path) + "/temp_video.avi"):
        os.remove(str(local_path) + "/temp_video.avi")
    if os.path.exists(str(local_path) + "/temp_video_correct_fps.avi"):
        os.remove(str(local_path) + "/temp_video_correct_fps.avi")

