from threading import Event

import cv2

from hwdesk.camera.base import BaseCamera


class MS2130(BaseCamera):
    def __init__(
        self,
        camera: cv2.VideoCapture,
        fps: int = 10,
        exit_flag: Event | None = None,
    ):
        super().__init__(camera, fps, exit_flag)
        assert self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 50)
        assert self.cap.set(cv2.CAP_PROP_CONTRAST, 50)
        assert self.cap.set(cv2.CAP_PROP_SATURATION, 50)
        assert self.cap.set(cv2.CAP_PROP_HUE, 50)
