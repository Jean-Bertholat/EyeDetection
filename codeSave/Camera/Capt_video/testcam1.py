from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 180

camera.start_preview()
camera.start_recording('/home/pi/Desktop/Camera/video.h264')
sleep(15)
camera.stop_recording()
camera.stop_preview()