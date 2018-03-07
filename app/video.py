import configparser as cp
import os

import cv2
import numpy as np


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
        return int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

    def parse_config(self):
        self.downsize_factor = 1 / self.config["DEFAULT"].getfloat("downsize_factor")

    def rewind(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def close(self):
        self.cap.release()

    def match_template(self, img, template):
        # methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
        #           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        if not os.path.isfile(template):
            raise FileNotFoundError(f"{config_file} does not exist")
        temp_img = cv2.imread(template)
        w, h = temp_img.shape[0:2]
        # print(f"Template W/H = {w}/{h}")
        method = eval('cv2.TM_CCOEFF')
        res = cv2.matchTemplate(img, temp_img, method)
        res -= np.min(res)
        res /= np.max(res)
        res *= 255
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img, top_left, bottom_right, 255, 2)
        res_out = np.zeros_like(img)
        res_out[0:res.shape[0], 0:res.shape[1], :] = cv2.cvtColor(res, cv2.COLOR_GRAY2RGB)
        return np.concatenate([res_out, img], axis=1)

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
            cv2.imshow('frame', gray) if show else None
            scene_file_name = os.path.join(output_dir, "scene_{:03d}.png".format(frame_no))
            detect_file_name = os.path.join(output_dir, "detect_{:03d}.png".format(frame_no))
            cv2.imwrite(scene_file_name, gray)
            cv2.imwrite(detect_file_name,
                        self.match_template(gray, os.path.join(self.script_directory, "sprites/00_huen.png")))
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
