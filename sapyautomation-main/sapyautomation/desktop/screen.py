import threading
from time import sleep
from datetime import datetime

import cv2
import numpy
import pyautogui


class ScreenCapture:

    def __init__(self):
        self._recording = False
        self._actual_frame = None
        self._record_data = None

    def record_data(self) -> dict:
        if self._record_data is not None:
            duration = (self._record_data['stopped_at'] -
                        self._record_data['started_at']).total_seconds()
            framerate = int(self._record_data['total_frames'] / duration)

            return {'duration': duration,
                    'framerate': framerate,
                    'lostframes': self._record_data['lost_frames'],
                    'path': self._record_data['file_path']}

        return None

    def take_screenshoot(self, file_path: str, await_before: float = 0.1,
                         await_after: float = 0.1,
                         asynchronous: bool = False):
        """  This method takes a screenshot.

        Args:
            file_path(str): absolute path to the screenshot-file.
            await_before(float): seconds to await before taking evidence
            await_after(float): seconds to await after taking evidence
            asynchronous(bool): Flag to take screenshot asynchronously.

        """
        if asynchronous:
            threading.Thread(target=self._screenshoot, args=(
                file_path, await_before, await_after)).start()
        else:
            self._screenshoot(file_path, await_before, await_after)

        return file_path

    def start_record(self, file_path: str, frame_rate: float = 25.0):
        """ Starts the recorder

        Args:
            file_path(str): absolute path to the video-file.
            frame_rate(float): frame rate for the video.

        """
        self._recording = True
        self._record_data = {'total_frames': 0,
                             'lost_frames': 0,
                             'started_at': None,
                             'stopped_at': None,
                             'file_path': file_path}
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self._out = cv2.VideoWriter(file_path, fourcc, frame_rate,
                                    pyautogui.size())

        threading.Thread(target=self._record).start()

    def stop_record(self):
        """ Stops the recorder
        """
        self._recording = False
        sleep(1)

    @staticmethod
    def _record_frame():
        """ This method takes a screenshoot and coverts it to frame
        for the VideoWriter object.
        """
        img = pyautogui.screenshot()
        frame = numpy.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return frame

    @staticmethod
    def _screenshoot(file_path: str, await_before: float = 0.1,
                     await_after: float = 0.1):
        """ This method takes a screenshot.

        Args:
            file_path(str): absolute path to the screenshot-file.
            await_before(float): seconds to await before taking evidence
            await_after(float): seconds to await after taking evidence

        """
        sleep(await_before)
        pyautogui.screenshot(file_path)
        sleep(await_after)

    def _record(self):
        """ This method takes frames and appends them to the
        VideoWriter(_out) object.

        """
        self._record_data['started_at'] = datetime.now()
        while self._recording:
            self._record_data['total_frames'] = \
                self._record_data['total_frames'] + 1
            try:
                frame = self._record_frame()
                self._out.write(frame)
                sleep(0.005)
            except IOError:
                # pass on frame capture error
                self._record_data['lost_frames'] = \
                    self._record_data['lost_frames'] + 1

        self._record_data['stopped_at'] = datetime.now()
