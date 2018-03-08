import matplotlib.pyplot as plt

from app.video import Video

v0 = Video("videos/video0.mp4", "workspace/config.ini")
# v0.extract_frames(show=False)
# frame_gen = v0.frame_generator()
# for f in frame_gen:
#    print(f"#{f.frame_no} {f.frame_time} {np.shape(f.frame)}")
time_series = v0.extract_time_series()
# print(time_series)

score0 = time_series.score()
score0.time_series()

