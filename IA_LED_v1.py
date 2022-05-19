from __future__ import print_function
import cv2 as cv
import RPi.GPIO as GPIO
import argparse


## ARGUMENTS ##

parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='data/haarcascades/haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()

## INITIALISATION ##

GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
GPIO.setwarnings(False) #On désactive les messages d'alerte
#GPIO.setwarnings(False) #On désactive les messages d'alerte
GPIO_LED = [[11,7,16,12],[15,13,22,18],[37,35,38,40]] #Définit le numéro du port GPIO qui alimente la led
XY_AREAS = [4, 3]


camera_device = args.camera
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade

face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()

## METHODES ##

def setupAllGpio(LED):
    for LEDi in LED:
        for i in LEDi:
            GPIO.setup(i, GPIO.OUT) #Active le contrôle du GPIO


def detectObjects(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    listEyes = []
    
    """print(frame_gray.shape) """

    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    #print(faces)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)

        face_frame = frame_gray[y:y+h,x:x+w]

        #-- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(face_frame)
        #print(eyes)
        
        for (x2,y2,w2,h2) in eyes:
            if y2 > h2 // 2:
                pass

            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            
            radius = int(round((w2 + h2)*0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
            
            if listEyes == []:  # Pour permettre d'avoir l'oeil gauche en 0
                listEyes.append(eye_center)
            elif len(listEyes) == 1:
                if listEyes[0][0] > eye_center[0]:
                    listEyes.insert(0,eye_center)
                else:
                    listEyes.append(eye_center)
                
    return (frame, listEyes)

def displayFrame(frame):
    cv.imshow('Capture - Face detection', frame)

def launchFlow(camera,w=640,h=480):
    cap = cv.VideoCapture (camera)#("filename.avi")#(
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)
    """   
    if not (cap.set(cv.CAP_PROP_FRAME_WIDTH,w) and cap.set(cv.CAP_PROP_FRAME_HEIGHT,h)):
        print('--(!)Error reshaping video size capture')
        exit(0)"""
         
    return cap
    
def closeFlow(cap, listGPIO):
    print("## STOPING DISPLAYING ##")
    for LEDi in listGPIO:
        for i in LEDi:
            GPIO.output(i, GPIO.LOW) #On allume la bonne led

    cap.release()
    cv.destroyAllWindows()
    
def loadCascades(cascade, name): #-- 1. Load the cascades

    if not cascade.load(cv.samples.findFile(name)):
        print('--(!)Error loading : ' + name)
        exit(0)
        
def ledManag(frame, listEyes, listLed):
    xMax = frame.get(cv.CAP_PROP_FRAME_WIDTH)
    yMax = frame.get(cv.CAP_PROP_FRAME_HEIGHT)

    X, Y = getAreas(xMax, yMax, XY_AREAS[0], XY_AREAS[1])
    #eye_center = (280,100)
    #print(eye_center)
    
   
    try:
        for i in listLed :
            GPIO.output(i, GPIO.LOW) #On éteint les LEDs
        #Oeil gauche 
        for i in range (len(X)-1):
            if (listEyes[0][0] > X[i]) and (listEyes[0][0] < X[i+1]):
                
                for j in range (len(Y)-1):
                    if listEyes[0][1] > Y[j] and listEyes[0][1] < Y[j+1]:
                        GPIO.output(listLed[j][i], GPIO.HIGH) #On allume la bonne led
                        
        #Oeil droit
        for i in range (len(X)-1):
            if (listEyes[1][0] > X[i]) and (listEyes[1][0] < X[i+1]):
                
                for j in range (len(Y)-1):
                    if listEyes[1][1] > Y[j] and listEyes[1][1] < Y[j+1]:
                        GPIO.output(listLed[j][i], GPIO.HIGH) #On allume la bonne led
                        
    except IndexError:
         print("Pas d'yeux détectés")
    
    return X,Y
        
    
def getAreas(x, y, xAreas, yAreas):

    X = [0]
    Y = [0]
    
    for i in range (xAreas) :
        X.append(X[i] + x//(xAreas))
        
    for i in range (yAreas) :
        Y.append(Y[i] + y//(yAreas))
    
    return X, Y

def drawGrid(frame, X, Y):
    xMax = frame.shape[0]
    yMax = frame.shape[1]
    
    try:
        for i in range (len(X)):
            frame = cv.line(frame, (int(X[i]), 0), (int(X[i]), xMax), (255,255,255), 1)
            
        for i in range (len(Y)):
            frame = cv.line(frame, (0, int(Y[i])), (yMax, int(Y[i])), (255,255,255), 1)
                
    except TypeError:
        pass
    
    return frame
    

def main():

## LOADING CASCADES ##
    
    loadCascades(face_cascade,face_cascade_name)
    loadCascades(eyes_cascade,eyes_cascade_name)
    setupAllGpio(GPIO_LED)
    (listX,listY) = [[],[]]
    cap = launchFlow(camera_device) #-- 2. Read the video stream
    listEyes = []   

    while True:
        _, frame = cap.read()

        if frame is None:
            print('--(!) No captured frame -- Break!')
            break

        img, listEyes = detectObjects(frame)
        img = drawGrid(img,listX,listY)
        displayFrame(img)
        (listX,listY) = ledManag(cap, listEyes, GPIO_LED)
        print(listEyes)
        

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    closeFlow(cap,GPIO_LED)
    
if __name__ == "__main__":
    main()
