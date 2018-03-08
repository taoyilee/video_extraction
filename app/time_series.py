from app.timeseries_features.score import Score


class TimeSeries:
    frame = []

    def __init__(self, frames=[]):
        if frames is not None:
            self.frame = frames

    def add_frame(self, frame):
        self.frame.append(frame)

    def score(self):
        return Score(self.frame)

    def __repr__(self):
        return f"** This time-series contains {len(self.frame)} frames."
