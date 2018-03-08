import matplotlib.pyplot as plt
import pandas as pd

from app.frame import Frame
from app.timeseries_features.BaseFeature import BaseFeature
from app.timeseries_features.Digit import Digit


class Score(BaseFeature):
    scores = []
    time = []
    ts = None

    def time_series(self):
        self.extract_score()
        ts = pd.Series(self.scores, index=self.time, name="Score")
        plt.figure()
        ts.plot()
        plt.xlabel("Time (ms)")
        plt.ylabel("Score")
        plt.show()

    def extract_score(self):
        for f in self.frames:  # type:Frame
            score = 0
            w = int(f.w * 20 / 1280)
            h = int(f.h * 27 / 720)
            x0 = int(f.w * 0.1565)
            y0 = int(f.h * 0.508)
            for i in range(5):
                digit_i = f.frame[y0:y0 + h, x0 - (i + 1) * w:x0 - i * w]
                d = Digit(digit_i)
                score += d.estimate_digit() * (10 ** i)
            self.scores.append(score)
            self.time.append(f.frame_time)
            print(f"Score for frame #{f.frame_no} is {score}")
