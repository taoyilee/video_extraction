import configparser as cp
import os

import cv2


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

    def __init__(self, filename, config_file=None):
        self.filename = filename
        if config_file is None:
            script_directory = os.path.dirname(os.path.realpath(__file__))
            config_file = os.path.join(script_directory, "default_config.ini")
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
        return int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

    def parse_config(self):
        self.downsize_factor = 1 / self.config["DEFAULT"].getfloat("downsize_factor")

    def rewind(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def close(self):
        self.cap.release()

    def extract_frames(self, show=False):
        self.rewind()
        output_dir = "captures"
        os.makedirs(output_dir, exist_ok=True)

        frame_no = 0
        while self.cap.isOpened():
            for i in range(int(self.config["DEFAULT"].getfloat("time_downsample"))):
                ret, frame = self.cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
            gray = cv2.resize(gray, (0, 0), fx=self.downsize_factor, fy=self.downsize_factor)
            font = cv2.FONT_HERSHEY_SIMPLEX
            frame_status = "{:.2f}s #{}".format(self.get_current_frame_time() / 1000, self.get_current_frame())
            gray = cv2.putText(gray, frame_status, (0, 13), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imshow('frame', gray)
            scene_file_name = os.path.join(output_dir, "scene_{:03d}.png".format(frame_no))
            cv2.imwrite(scene_file_name, gray)
            frame_no += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def __repr__(self):
        return_string = "Video {} ".format(self.filename)
        return_string += "has {} frames @ {:.3f}\n".format(self.frame_cnt, self.fps)
        return_string += f"Current position is {self.pos_msec} (ms) @ frame {self.pos_frames} "
        return_string += "(AVI ratio = {:.2e})\n".format(self.pos_avi_ratio)
        return_string += f"W/H = {self.frame_width}/{self.frame_height}\n"
        return return_string
