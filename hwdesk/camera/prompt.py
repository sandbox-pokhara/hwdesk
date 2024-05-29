from tkinter.messagebox import showerror  # type:ignore
from tkinter.simpledialog import askinteger

from opencv_cam_idx.finder import find_cameras


def ask_camera_idx() -> tuple[int, str]:
    prompt: list[str] = []
    prompt.append("Please enter the index of camera you want to access:")
    valid_idx: dict[int, tuple[int, str]] = {}
    for c in find_cameras():
        if "pid_2130" in c.device_path:
            valid_idx[c.idx] = c.idx, c.friendly_name
            prompt.append(f"Index={c.idx}, Name={c.friendly_name}")
    if valid_idx == {}:
        showerror("HwDesk Error", "No MS2130 devices found.")
        return -1, ""
    idx = askinteger(
        "Camera Selection", "\n".join(prompt), initialvalue=0, minvalue=0
    )
    if idx not in valid_idx:
        showerror("HwDesk Error", "Please select a valid camera index.")
        return -1, ""
    return valid_idx[idx]
