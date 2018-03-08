import cv2
import numpy as np

from app.frame import Frame
from app.timeseries_features.score import Score

score_95450 = cv2.imread("workspace/scene_3434.png")
score_95450 = cv2.cvtColor(score_95450, cv2.COLOR_BGR2GRAY)
print(f"H/W = {np.shape(score_95450)[0]}, {np.shape(score_95450)[1]}")
frame = Frame(score_95450)
score = Score(frames=[frame])
score.time_series()
