from tkinter.messagebox import showerror  # type:ignore
from tkinter.simpledialog import askinteger

from opencv_cam_idx.finder import find_cameras


def ask_camera_idx():
    prompt = ""
    prompt += "Please enter the index of server you want access: \n"
    valid_idx: list[int] = []
    for c in find_cameras():
        if "pid_2130" in c.device_path:
            valid_idx.append(c.idx)
            prompt += f"Index={c.idx}, Name={c.friendly_name}"
    idx = askinteger("Server Selection", prompt, initialvalue=0, minvalue=0)
    if idx not in valid_idx:
        showerror("HwDesk Error", "Please select a valid server index.")
        return -1
    return idx
