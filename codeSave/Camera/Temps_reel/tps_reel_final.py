import cv2
import numpy as np
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24
    camera.start_preview()
    
def main():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('image')
    
    while True:
        _, frame = cap.read()
        print(frame.shape)
        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()