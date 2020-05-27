# -*- coding: utf-8 -*-
# This file is part of the Horus Project

__author__ = 'Jesús Arroyo Torrens <jesus.arroyo@bq.com>'
__copyright__ = 'Copyright (C) 2014-2016 Mundo Reader S.L.'
__license__ = 'GNU General Public License v2 http://www.gnu.org/licenses/gpl2.html'

import cv2
import math
import time
import glob
import platform
from cyuye import cyueye as cu

import logging
logger = logging.getLogger(__name__)

system = platform.system()

if system == 'Darwin':
    import uvc
    from uvc.mac import *


class WrongCamera(Exception):

    def __init__(self):
        Exception.__init__(self, "Wrong Camera")


class CameraNotConnected(Exception):

    def __init__(self):
        Exception.__init__(self, "Camera Not Connected")


class InvalidVideo(Exception):

    def __init__(self):
        Exception.__init__(self, "Invalid Video")


class WrongDriver(Exception):

    def __init__(self):
        Exception.__init__(self, "Wrong Driver")


class InputOutputError(Exception):

    def __init__(self):
        Exception.__init__(self, "V4L2 Input/Output Error")


class Camera(object):

    """Camera class. For accessing to the scanner camera"""

    def __init__(self, parent=None, camera_id=0):
        self.parent = parent
        self.camera_id = camera_id
        self.unplug_callback = None

        self._capture = None
        self._is_connected = False
        self._reading = False
        self._updating = False
        self._last_image = None
        self._video_list = None
        self._tries = 0  # Check if command fails
        self._luminosity = 1.0

        self.initialize()

        if system == 'Windows':
            self._number_frames_fail = 3
            self._max_brightness = 1.
            self._max_contrast = 1.
            self._max_saturation = 1.
        elif system == 'Darwin':
            self._number_frames_fail = 3
            self._max_brightness = 255.
            self._max_contrast = 255.
            self._max_saturation = 255.
            self._rel_exposure = 10.
        else:
            self._number_frames_fail = 3
            self._max_brightness = 255.
            self._max_contrast = 255.
            self._max_saturation = 255.
            self._max_exposure = 1000.

    def initialize(self):
        self._brightness = 0
        self._contrast = 0
        self._saturation = 0
        self._exposure = 0
        self._frame_rate = 0
        self._width = 720
        self._height = 1280
        self._rotate = False
        self._hflip = False
        self._vflip = False

    def connect(self):
        #TODO: Check if Camrea open
        logger.info("Connecting camera {0}".format(self.camera_id))
        self._is_connected = False
        self.initialize()
        time.sleep(1)
        self._capture = cu.Cam(format_id=9)
        self._capture.alloc_image_mem()
        #self._capture.capture_video()
        self._is_connected = True
        #logger.info("Check Video")
        #self._check_video()
        #logger.info("Check Camera")
        #self._check_camera()
        #logger.info("Check Driver")
        #self._check_driver()
        logger.info(" Done")

    def disconnect(self):
        self._capture=None

    def set_unplug_callback(self, value):
        self.unplug_callback = value

    def _check_video(self):
        """Check correct video"""
        frame = self.capture_image(flush=1)
        if frame is None or (frame == 0).all():
            raise InvalidVideo()

    def _check_camera(self):
        """Check correct camera"""
        c_exp = False
        c_bri = False

        try:
            # Check exposure
            if system == 'Darwin':
                self.controls['UVCC_REQ_EXPOSURE_AUTOMODE'].set_val(1)
            self.set_exposure(2)
            exposure = self.get_exposure()
            if exposure is not None:
                c_exp = exposure >= 1.9

            # Check brightness
            self.set_brightness(2)
            brightness = self.get_brightness()
            if brightness is not None:
                c_bri = brightness >= 2
        except:
            raise WrongCamera()

        if not c_exp or not c_bri:
            raise WrongCamera()

    def _check_driver(self):
        """Check correct driver: only for Windows"""
        if system == 'Windows':
            self.set_exposure(10)
            frame = self.capture_image(flush=1)
            mean = sum(cv2.mean(frame)) / 3.0
            if mean > 200:
                raise WrongDriver()

    def capture_image(self, flush=0, auto=False):
        """Capture image from camera"""
        if self._is_connected:
            if self._updating:
                return self._last_image
            else:
                self._reading = True
                if auto:
                    print("auto")
                if flush > 0:
                    for i in xrange(flush):
                        self._capture.read()
                        # Note: Windows needs read() to perform
                        #       the flush instead of grab()
                ret, image = self._capture.read()
                self._reading = False
                if ret:
                    self._success()
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    self._last_image = image
                    return image
                else:
                    self._fail()
                    return None
        else:
            return None

    def save_image(self, filename, image):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(filename, image)

    def set_rotate(self, value):
        self._rotate = value

    def set_hflip(self, value):
        pass

    def set_vflip(self, value):
        pass

    def set_brightness(self, value):
        if self._is_connected:
            if self._brightness != value:
                self._updating = True
                self._brightness = value
                if system == 'Darwin':
                    ctl = self.controls['UVCC_REQ_BRIGHTNESS_ABS']
                    ctl.set_val(self._line(value, 0, self._max_brightness, ctl.min, ctl.max))
                else:
                    pass
                self._updating = False

    def set_contrast(self, value):
        if self._is_connected:
            if self._contrast != value:
                self._updating = True
                self._contrast = value
                if system == 'Darwin':
                    ctl = self.controls['UVCC_REQ_CONTRAST_ABS']
                    ctl.set_val(self._line(value, 0, self._max_contrast, ctl.min, ctl.max))
                else:
                    pass
                self._updating = False

    def set_saturation(self, value):
        if self._is_connected:
            if self._saturation != value:
                self._updating = True
                self._saturation = value
                if system == 'Darwin':
                    ctl = self.controls['UVCC_REQ_SATURATION_ABS']
                    ctl.set_val(self._line(value, 0, self._max_saturation, ctl.min, ctl.max))
                else:
                    pass
                self._updating = False

    def set_exposure(self, value, force=False):
        if self._is_connected:
            if self._exposure != value or force:
                self._updating = True
                self._exposure = value
                value *= self._luminosity
                if value < 1:
                    value = 1
                if system == 'Darwin':
                    ctl = self.controls['UVCC_REQ_EXPOSURE_ABS']
                    value = int(value * self._rel_exposure)
                    ctl.set_val(value)
                elif system == 'Windows':
                    value = int(round(-math.log(value) / math.log(2)))
                    self._capture.set(cv2.cv.CV_CAP_PROP_EXPOSURE, value)
                else:
                    pass
                    #value = int(value) / self._max_exposure
                    #ret = self._capture.set_exposure(value)
                    #if system == 'Linux' and ret:
                    #    raise InputOutputError()
                self._updating = False

    def set_luminosity(self, value):
        possible_values = {
            "High": 0.5,
            "Medium": 1.0,
            "Low": 2.0
        }
        self._luminosity = possible_values[value]
        self.set_exposure(self._exposure, force=True)

    def set_frame_rate(self, value):
        if self._is_connected:
            if self._frame_rate != value:
                self._frame_rate = value
                self._updating = True
                print(self._capture.set_framerate(30))
                print('set framerate')
                self._updating = False

    def set_resolution(self, width, height):
        if self._is_connected:
            if self._width != width or self._height != height:
                self._updating = True
                self._set_width(width)
                self._set_height(height)
                self._update_resolution()
                self._updating = False

    def _set_width(self, value):
        pass

    def _set_height(self, value):
        pass

    def _update_resolution(self):
        self._width = 720
        self._height = 1280

    def get_brightness(self):
        if self._is_connected:
            if system == 'Darwin':
                ctl = self.controls['UVCC_REQ_BRIGHTNESS_ABS']
                value = ctl.get_val()
            else:
                return 50

    def get_exposure(self):
        if self._is_connected:
            if system == 'Darwin':
                ctl = self.controls['UVCC_REQ_EXPOSURE_ABS']
                value = ctl.get_val()
                value /= self._rel_exposure
            elif system == 'Windows':
                value = self._capture.get(cv2.cv.CV_CAP_PROP_EXPOSURE)
                value = 2 ** -value
            else:
                value = self._capture.get_exposure()
                value *= self._max_exposure
            return value

    def get_resolution(self):
        if self._rotate:
            return int(self._height), int(self._width)
        else:
            return int(self._width), int(self._height)

    def _success(self):
        self._tries = 0

    def _fail(self):
        logger.debug("Camera fail")
        self._tries += 1
        if self._tries >= self._number_frames_fail:
            self._tries = 0
            if self.unplug_callback is not None and \
               self.parent is not None and \
               not self.parent.unplugged:
                self.parent.unplugged = True
                self.unplug_callback()

    def _line(self, value, imin, imax, omin, omax):
        ret = 0
        if omin is not None and omax is not None:
            if (imax - imin) != 0:
                ret = int((value - imin) * (omax - omin) / (imax - imin) + omin)
        return ret

    def _count_cameras(self):
        for i in xrange(5):
            cap = cv2.VideoCapture(i)
            res = not cap.isOpened()
            cap.release()
            if res:
                return i
        return 5

    def get_video_list(self):
        baselist = []
        if system == 'Windows':
            if not self._is_connected:
                count = self._count_cameras()
                for i in xrange(count):
                    baselist.append(str(i))
                self._video_list = baselist
        elif system == 'Darwin':
            for device in uvc.mac.Camera_List():
                baselist.append(str(device.src_id))
            self._video_list = baselist
        else:
            for device in ['/dev/video*']:
                baselist = baselist + glob.glob(device)
            self._video_list = baselist
        return self._video_list
