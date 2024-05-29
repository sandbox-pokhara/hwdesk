from random import randint


class BaseControls:
    def __init__(self):
        self.x = -1
        self.y = -1

    def base_move(self, x: int, y: int) -> None:
        raise NotImplementedError

    def click(self, button: str = "left") -> None:
        raise NotImplementedError

    def press_and_release(self, key: str, modifier: str = "") -> None:
        raise NotImplementedError

    def write(self, text: str) -> None:
        raise NotImplementedError

    def scroll(self, delta: int) -> None:
        raise NotImplementedError

    def release(self) -> None:
        raise NotImplementedError

    # derived methods
    def move(self, x: int, y: int, humanize_x: int = 5, humanize_y: int = 5):
        tx = x + randint(-humanize_x, humanize_x)
        ty = y + randint(-humanize_y, humanize_y)

        # avoid negative positions
        tx = max(0, tx)
        ty = max(0, ty)

        self.x = tx
        self.y = ty
        self.base_move(tx, ty)
