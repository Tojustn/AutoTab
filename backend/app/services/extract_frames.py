import cv2 as cv
import os
import json 
from app.services.user_session import get_user_paths


def extract_frames(videopath: str, mode: str, interval: int = None, frames_array: list = None) -> dict:
    user_paths = get_user_paths()
    frames_path = user_paths["file_path"]
    videoObj = cv.VideoCapture(videopath)
    fps = videoObj.get(cv.CAP_PROP_FPS)
    frame_count = 0
    success = True
    saved_frames = []

    if not videoObj.isOpened():
        print(f"Failed to open video: {videopath}")
        return {"success": False, "error": "Failed to open video"}

    if mode == "interval":
        if interval is None or interval < 1:
            interval = 1
        frame_interval = int(fps * interval)
    elif mode == "select":
        if not frames_array:
            videoObj.release()
            return {"success": False, "error": "frames_array required for select mode"}
        frames_set = set(int(frame * fps) for frame in frames_array)
    else:
        videoObj.release()
        return {"success": False, "error": "Invalid mode"}

    while success:
        success, image = videoObj.read()
        if not success:
            break

        save = False
        if mode == "interval":
            if frame_count % frame_interval == 0:
                save = True
        elif mode == "select":
            if frame_count in frames_set:
                save = True

        if save:
            uploadFile = os.path.join(frames_path, f"frame_{frame_count}.jpg")
            cv.imwrite(uploadFile, image)
            saved_frames.append(frame_count)
        frame_count += 1

    videoObj.release()
    return {"success": True, "total_frames": frame_count, "saved_frames": saved_frames}
