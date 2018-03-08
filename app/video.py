import configparser as cp
import os

import cv2
import numpy as np

from app.frame import Frame
from app.time_series import TimeSeries


class Video:
    fps = None
    pos_msec = None
    pos_frames = None
    pos_avi_ratio = None
    frame_width: int = None
    frame_height: int = None
    fourcc = None
    frame_cnt: int = None
    format = None
    config: cp.ConfigParser = cp.ConfigParser()
    cap = None
    downsize_factor = 1
    script_directory = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, filename, config_file=None):
        self.filename = filename
        if config_file is None:
            config_file = os.path.join(self.script_directory, "default_config.ini")
        print(f"Using config file {config_file}")
        if not os.path.isfile(config_file):
            raise FileNotFoundError(f"{config_file} does not exist")
        self.config.read(config_file)

        if not os.path.isfile(self.filename):
            raise FileNotFoundError(f"{self.filename} does not exist")
        self.parse_config()
        self.cap = cv2.VideoCapture(self.filename)
        self.extract_properties()

    def extract_properties(self):

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.pos_msec = self.get_current_frame_time()
        self.pos_frames = self.get_current_frame()
        self.pos_avi_ratio = self.cap.get(cv2.CAP_PROP_POS_AVI_RATIO)
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fourcc = self.cap.get(cv2.CAP_PROP_FOURCC)
        self.frame_cnt = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.format = self.cap.get(cv2.CAP_PROP_FORMAT)

    def get_current_frame_time(self):
        return self.cap.get(cv2.CAP_PROP_POS_MSEC)

    def get_current_frame(self):
        return int(self.cap.get(cv2.CAP_PROP_POS_FRAMES) - 1)

    def parse_config(self):
        self.downsize_factor = 1 / self.config["DEFAULT"].getfloat("downsize_factor")

    def rewind(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def close(self):
        self.cap.release()

    def skip_frames(self, frames_to_skip):
        for i in range(frames_to_skip):
            self.cap.read()

    def frame_generator(self):
        self.rewind()
        time_step = int(self.config["DEFAULT"].getfloat("time_downsample"))
        for frame_no in range(0, self.frame_cnt, time_step):
            ret, frame = self.cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.resize(frame, (0, 0), fx=self.downsize_factor, fy=self.downsize_factor)
            yield Frame(frame, self.get_current_frame(), self.get_current_frame_time())
            self.skip_frames(time_step)

    def extract_time_series(self):
        self.rewind()
        time_series = TimeSeries()
        for f in self.frame_generator():
            time_series.add_frame(f)
        return time_series

    def extract_frames(self, show=False):
        self.rewind()
        output_dir = "captures"
        os.makedirs(output_dir, exist_ok=True)

        generator = self.frame_generator()
        for f in generator:
            gray = cv2.cvtColor(f.frame, cv2.COLOR_GRAY2RGB)
            gray = cv2.resize(gray, (0, 0), fx=self.downsize_factor, fy=self.downsize_factor)
            font = cv2.FONT_HERSHEY_SIMPLEX
            frame_status = "{:.2f}s #{}".format(f.frame_time / 1000, f.frame_no)
            gray = cv2.putText(gray, frame_status, (0, 13), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imshow('frame', gray) if show else None
            scene_file_name = os.path.join(output_dir, "scene_{:03d}.png".format(f.frame_no))
            print(f"Writing {scene_file_name}, {frame_status}")
            cv2.imwrite(scene_file_name, gray)

    def __repr__(self):
        return_string = "Video {} ".format(self.filename)
        return_string += "has {} frames @ {:.3f}\n".format(self.frame_cnt, self.fps)
        return_string += f"Current position is {self.pos_msec} (ms) @ frame {self.pos_frames} "
        return_string += "(AVI ratio = {:.2e})\n".format(self.pos_avi_ratio)
        return_string += f"W/H = {self.frame_width}/{self.frame_height}\n"
        return return_string
