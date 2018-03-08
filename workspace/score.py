import cv2

from app.frame import Frame
from app.timeseries_features.score import Score

score_95450 = cv2.imread("workspace/scene_193.png")
frame = Frame(score_95450)
Score(frames=[frame])
