from threading import Event

import cv2

from hwdesk.camera.base import BaseCamera


class MS2109(BaseCamera):
    def __init__(
        self, index: int, fps: int = 10, exit_flag: Event | None = None
    ):
        super().__init__(index, fps, exit_flag)
        assert self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 0)
        assert self.cap.set(cv2.CAP_PROP_CONTRAST, 128)
        assert self.cap.set(cv2.CAP_PROP_SATURATION, 128)
        assert self.cap.set(cv2.CAP_PROP_HUE, 0)
