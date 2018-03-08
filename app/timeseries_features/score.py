from app.frame import Frame
from app.timeseries_features.BaseFeature import BaseFeature


class Score(BaseFeature):

    def time_series(self):
        self.extract_score()

    def extract_score(self):
        for f in self.frames:  # type:Frame
            print(f"Frame is #{f.frame_no}")
