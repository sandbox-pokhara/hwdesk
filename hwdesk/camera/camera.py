from opencv_cam_idx.finder import find_cameras

from hwdesk.camera.base import BaseCamera
from hwdesk.camera.ms2109 import MS2109
from hwdesk.camera.ms2130 import MS2130


def get_camera_idx_by_name(server_name: str):
    for c in find_cameras():
        if c.friendly_name == server_name:
            return c.idx
    raise RuntimeError(
        f"Camera index for server {server_name} not found. "
        "Please make sure the camera name is set at firmware level."
    )


def get_camera_idx(
    method: str, name: str = "", index: int = -1, server_name: str = ""
):
    if method == "server_name":
        return get_camera_idx_by_name(server_name)
    elif method == "name":
        return get_camera_idx_by_name(name)
    elif method == "index":
        return index
    else:
        raise NotImplementedError(
            f"MS21XX identify method {method} not supported."
        )


def get_camera_module(
    server_name: str, camera_type: str, fps: int = 30, index: int = -1
) -> BaseCamera:
    """
    Returns ms2109, ms2130 or mss module
    """
    method = (
        "server_name"
        if server_name
        else "index" if index > 0 else "server_name"
    )
    if camera_type == "ms2109":
        idx = get_camera_idx(method, "", index, server_name)
        return MS2109(idx, fps)
    elif camera_type == "ms2130":
        idx = get_camera_idx(method, "", index, server_name)
        return MS2130(idx, fps)
    raise NotImplementedError(f"Camera {camera_type} is not supported.")
