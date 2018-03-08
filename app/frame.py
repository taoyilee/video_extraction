import os

import cv2
import numpy as np


class Frame:
    def __init__(self, frame, frame_no=0, frame_time=0):
        self.frame = frame
        self.frame_no = frame_no
        self.frame_time = frame_time

    def match_template(self, template):
        # methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
        #           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        if not os.path.isfile(template):
            raise FileNotFoundError(f"{config_file} does not exist")
        temp_img = cv2.imread(template)
        w, h = temp_img.shape[0:2]
        # print(f"Template W/H = {w}/{h}")
        method = eval('cv2.TM_CCOEFF')
        res = cv2.matchTemplate(self.frame, temp_img, method)
        res -= np.min(res)
        res /= np.max(res)
        res *= 255
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        highlighted_frame = self.frame.copy()
        cv2.rectangle(highlighted_frame, top_left, bottom_right, 255, 2)
        res_out = np.zeros_like(highlighted_frame)
        res_out[0:res.shape[0], 0:res.shape[1], :] = cv2.cvtColor(res, cv2.COLOR_GRAY2RGB)
        return np.concatenate([res_out, highlighted_frame], axis=1)
