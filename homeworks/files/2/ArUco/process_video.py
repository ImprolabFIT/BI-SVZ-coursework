import os
import cv2
from tqdm import tqdm
import numpy as np
import logging
from typing import Callable


logging.basicConfig(level=logging.INFO, format='%(message)s')


class VideoIterator:
    """
    cv2.VideoCapture iterator for reading video frames.
    Releases capture before StopIteration or after deletion. 
    Example usage:
        ```python
        reader = VideoIterator('input.mp4')
        for frame in reader:
            ...
        ```
    """

    def __init__(self, *cap_args, **cap_kwargs):
        """Initialize the video iterator.
        All args and kwargs are passed to cv2.VideoCapture.

        Raises
        ------
        RuntimeError
            When video capture fails to initialize.
        """
        self.cap = cv2.VideoCapture(*cap_args, **cap_kwargs)

        if not self.cap.isOpened():
            raise RuntimeError("Failed to initialize video capture.")

        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame = 0

    def _release(self) -> None:
        """Release the video capture."""
        if self.cap.isOpened():
            self.cap.release()

    def __iter__(self):
        return self

    def __next__(self) -> np.ndarray:
        ret, frame = self.cap.read()

        if not ret:
            self._release()
            raise StopIteration

        self.current_frame += 1

        return frame

    def __len__(self):
        return self.total_frames

    def __del__(self):
        self._release()


def process_video(in_name: str, out_name: str, update_fn: Callable[[np.ndarray, ...], np.ndarray], *fn_args, **fn_kwargs) -> None:
    """Open video "in_name", apply "update_fn" to each frame, and save the output to "out_name".

    Parameters
    ----------
    in_name : str
        name of the input video file
    out_name : str
        name of the output video file
    update_fn : Callable[[np.ndarray, ...], np.ndarray]
        function that takes a frame and returns a processed frame

    Raises
    ------
    RuntimeError
        if video writer fails to initialize
    """
    reader = VideoIterator(in_name)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For .mp4
    out_cap = cv2.VideoWriter(out_name, fourcc, reader.fps,
                              (reader.frame_width, reader.frame_height))

    if not out_cap.isOpened():
        raise RuntimeError("Failed to initialize video writer.")

    for frame in tqdm(reader, total=len(reader), unit='frame', desc=f'Processing video with function {update_fn.__name__}'):
        processed_frame = update_fn(frame, *fn_args, **fn_kwargs)
        out_cap.write(processed_frame)

    out_cap.release()

    cv2.destroyAllWindows()
    logging.info(f"Video processing complete. Output saved at: {out_name}.")
