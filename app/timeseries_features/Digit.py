import os

import cv2
import numpy as np


class Digit:
    script_directory = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, frame):
        self.frame = cv2.resize(frame, (20, 27))
        self.binarize()

    def binarize(self):
        self.frame = np.where(self.frame > 127, 1, 0)

    def shift(self, left_pixels):
        shifted_frame = np.concatenate([self.frame[:, left_pixels:], np.zeros((self.frame.shape[0], left_pixels))],
                                       axis=1)
        return shifted_frame

    def estimate_digit(self):
        est = np.zeros_like(range(3))
        mse = np.zeros_like(range(3))
        for i in range(3):
            est[i], mse[i] = self._estimate_digit(self.shift(i))
        return est[np.argmin(mse)]

    def _estimate_digit(self, frame):
        mse = np.zeros_like(range(10))
        for j in range(10):
            template = cv2.imread(os.path.join(self.script_directory, f"sprites/03_score{j}.png"))
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template_bin = np.where(template > 127, 1, 0)
            mse[j] = np.sum((template_bin - frame) ** 2)
        est = np.argmin(mse)
        mse = min(mse)
        return est, mse
