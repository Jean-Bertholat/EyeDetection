from __future__ import print_function
import cv2 as cv
import argparse

## ARGUMENTS ##

parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='data/haarcascades/haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()

## INITIALISATION ##

camera_device = args.camera
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade

face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()

## METHODES ##

def detectObjects(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)

    """print(frame_gray.shape) #-- Renvoie les couleurs liée à chaque pixel de l'image dans une matrice."""

    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    #print(faces)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)

        face_frame = frame_gray[y:y+h,x:x+w]

        #-- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(face_frame)
        """print(eyes)"""
        
        for (x2,y2,w2,h2) in eyes:
            if y2 > h2 // 2:
                pass

            eye_center = (x + x2 + w2//2, y + y2 + h2//2)

            radius = int(round((w2 + h2)*0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
            
    return frame

def displayFrame(frame):
    cv.imshow('Capture - Face detection', frame)

def launchFlow(camera):
    cap = cv.VideoCapture(camera)
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)
    return cap
    
def closeFlow(cap):
    print("## STOPING DISPLAYING ##")
    cap.release()
    cv.destroyAllWindows()
    
def loadCascades(cascade, name): #-- 1. Load the cascades

    if not cascade.load(cv.samples.findFile(name)):
        print('--(!)Error loading : ' + name)
        exit(0)

def main():

## LOADING CASCADES ##
    
    loadCascades(face_cascade,face_cascade_name)
    loadCascades(eyes_cascade,eyes_cascade_name)
    
    cap = launchFlow(camera_device) #-- 2. Read the video stream

    while True:
        _, frame = cap.read()
        print(frame.shape)

        if frame is None:
            print('--(!) No captured frame -- Break!')
            break

        img = detectObjects(frame)
        displayFrame(img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    closeFlow(cap)
    
if __name__ == "__main__":
    main()
