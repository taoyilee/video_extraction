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

    def __init__(self, filename):
        self.filename = filename
        if not os.path.isfile(self.filename):
            raise FileNotFoundError(f"{self.filename} does not exist")
        self.extract_properties()

    def extract_properties(self):
        cap = cv2.VideoCapture(self.filename)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.pos_msec = cap.get(cv2.CAP_PROP_POS_MSEC)
        self.pos_frames = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        self.pos_avi_ratio = cap.get(cv2.CAP_PROP_POS_AVI_RATIO)
        self.frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fourcc = cap.get(cv2.CAP_PROP_FOURCC)
        self.frame_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.format = cap.get(cv2.CAP_PROP_FORMAT)

        cap.release()

    def show_frames(self):
        cap = cv2.VideoCapture(self.filename)
        output_dir = "captures"
        os.makedirs(output_dir, exist_ok=True)

        frame_no = 0
        downsample = 10
        while (cap.isOpened()):
            for i in range(downsample):
                ret, frame = cap.read()
            if frame is None:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            cv2.imshow('frame', gray)
            scene_file_name = os.path.join(output_dir, f"scene_{frame_no}.png")
            cv2.imwrite(scene_file_name, gray)
            frame_no += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def __repr__(self):
        return_string = "Video {} ".format(self.filename)
        return_string += "has {} frames @ {:.3f}\n".format(self.frame_cnt, self.fps)
        return_string += f"Current position is {self.pos_msec} (ms) @ frame {self.pos_frames} "
        return_string += "(AVI ratio = {:.2e})\n".format(self.pos_avi_ratio)
        return_string += f"W/H = {self.frame_width}/{self.frame_height}\n"
        return return_string
