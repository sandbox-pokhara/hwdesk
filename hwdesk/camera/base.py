from cv2.typing import MatLike


class BaseCamera:
    fps: int = 10

    def __init__(self, is_software: bool):
        self.is_software = is_software

    def screenshot(self) -> MatLike | None:
        raise NotImplementedError

    def release(self) -> None:
        raise NotImplementedError
