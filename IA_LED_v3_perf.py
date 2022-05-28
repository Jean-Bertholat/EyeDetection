from __future__ import print_function
from tkinter.tix import TCL_DONT_WAIT
import cv2 as cv
import RPi.GPIO as GPIO
import argparse
import time


## ARGUMENTS ##
# Arguments that are mandatory for the program to work
# These arguments can be modified according to the environment in use

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
XY_AREAS = [4, 3]   # define the number of raws and the number of columns


camera_device = args.camera
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade

face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()

global isEyeDetected
global tDown
global tUp

isEyeDetected = 0
tDown = 0
tUp = 0

## METHODES ##

def setupAllGpio(LED):
# Initialize the GPIO of the rasp as output GPIO
    for LEDi in LED:
        for i in LEDi:
            GPIO.setup(i, GPIO.OUT) #Active le contrôle du GPIO

def launchFlow(camera,w=640,h=480):
    # Start the camera recording
    cap = cv.VideoCapture (camera)
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)
         
    return cap

def closeFlow(cap, listGPIO):
    # Stop the camera recording
    print("## STOPING DISPLAYING ##")
    for LEDi in listGPIO:
        for i in LEDi:
            GPIO.output(i, GPIO.LOW) #On allume la bonne led

    cap.release()
    cv.destroyAllWindows()

def loadCascades(cascade, name): #-- 1. Load the cascades
    #Load the cascade file for the program
    if not cascade.load(cv.samples.findFile(name)):
        print('--(!)Error loading : ' + name)
        exit(0)

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

def displayFrame(frame):
    # display the frame to the screen
    cv.imshow('Capture - Face detection', frame)


def detectObjects(frame):
# Detect faces and eyes in a frame, and return the modified frame and the coordonates of the eyes in the frame
    
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    listEyes = []
    listError = []
    firstFrame = frame_gray.shape
    
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)

    for (x,y,w,h) in faces:
        #(x, y) are the coordonates of the up left corner of the rectangle face in the frame
        #(w, h) are the width and hight of the face
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)

        face_frame = frame_gray[y:y+h,x:x+w] #Select only the face rectangle
        
        secondFrame = face_frame.shape
        augmFactor = (firstFrame[0]//secondFrame[0],firstFrame[1]//secondFrame[1])
        
        #-- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(face_frame)
        
        for (x2,y2,w2,h2) in eyes:
            #print(eyes)
            #print("y + h//2 =", (y + h//2)//augmFactor[1])
            #(x2, y2) are the coordonates of the up left corner of the rectangle eye int the rectangle face
            #(w2, h2) are the width and hight of the eye

            if y + y2 + h2//2 > (y + h//2):
                #if mouth or nose are detected as eye
                error_center = (x + x2 + w2//2, y + y2 + h2//2)
                listError.append(error_center)
                pass
            
            else:
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
                
    return (frame, listEyes, listError)
        
def ledManag(frame, listEyes, listLed):
    xMax = frame.get(cv.CAP_PROP_FRAME_WIDTH)
    yMax = frame.get(cv.CAP_PROP_FRAME_HEIGHT)
    global isEyeDetected
    
    X, Y = getAreas(xMax, yMax, XY_AREAS[0], XY_AREAS[1])    
    # X, Y are lists of the coordonates of the lines and columns on the frame
   
    try:
        for i in listLed :
            GPIO.output(i, GPIO.LOW) #On éteint les LEDs
            ##############################################################éteint time
            tDown = time.time()
        #Oeil gauche 
        for i in range (len(X)-1):
            # We try to find in which area the eye is (only one i will work)
            if (listEyes[0][0] > X[i]) and (listEyes[0][0] < X[i+1]):
                # When we have find the x
                for j in range (len(Y)-1):
                    #We look for the y
                    if listEyes[0][1] > Y[j] and listEyes[0][1] < Y[j+1]:
                        # now that we have the coordonates of the area in which the eye is we can turn on the coresponding led (The led are in areas order)
                        #################################################################alumée time
                        tUp = time.time()
                        GPIO.output(listLed[j][i], GPIO.HIGH) #On allume la bonne led
                        
        #Oeil droit
        for i in range (len(X)-1):
            if (listEyes[1][0] > X[i]) and (listEyes[1][0] < X[i+1]):
                
                for j in range (len(Y)-1):
                    if listEyes[1][1] > Y[j] and listEyes[1][1] < Y[j+1]:
                        GPIO.output(listLed[j][i], GPIO.HIGH) #On allume la bonne led
            
        isEyeDetected = 1 #Trigger eyes detected

    except IndexError:
        print("Pas d'yeux détectés")
    
    return X,Y
        
def getAreas(x, y, xAreas, yAreas):
    # Return the coordonates (x,y) of the differents limits of areas (of the grid lines)

    X = [0]
    Y = [0]
    
    for i in range (xAreas) :
        X.append(X[i] + x//(xAreas))
        
    for i in range (yAreas) :
        Y.append(Y[i] + y//(yAreas))
    
    return X, Y


def precision(countEye, countError):
    
    res = countError/(countEye + countError)

    return res

def main(nb):

    ## LOADING CASCADES ##
    
    loadCascades(face_cascade,face_cascade_name)
    loadCascades(eyes_cascade,eyes_cascade_name)
    setupAllGpio(GPIO_LED)
    (listX,listY) = [[],[]]
    cap = launchFlow(camera_device) #-- 2. Read the video stream
    
    listEyes = []
    listError = []
    global isEyeDetected

    frname = "./Logs/RespondTime" + str(nb) + ".csv"
    ffname = "./Logs/LogFormes" + str(nb) + ".txt"

    fr = open(frname, "a")
    fr.write("Num_Frame,Respond_Time,Eyes detected\n")
    
    ff = open(ffname, "a")
    i = 0
    timer = 0
    countEye = 0
    countError = 0

    while timer < 20:   #1 minute recording

        start = 0 #To compute the respond time of a frame detection
        end = 0

    ## COMPUTATION ##

        _, frame = cap.read()
        
        if frame is None:
            print('--(!) No captured frame -- Break!')
            break
        
        start = time.time() #start the timer before face detection

        img, listEyes, listError = detectObjects(frame)
        img = drawGrid(img,listX,listY)
        displayFrame(img)
        (listX,listY) = ledManag(cap, listEyes, GPIO_LED)
        tStable = tUp - tDown
        print(f"Stability time evolution : {tStable}") 

        end = time.time() #The LED have been turned on

    ## LOGS ##

        print(f"Eye: {listEyes}, Error(s): {listError}\n")
        
        ff.write(f"{i}- Eye: {listEyes}, error: {listError}\n")
        countEye += len(listEyes) 
        countError += len(listError) 
        #fr.write(f"{i}- {end-start:.10f} Eyes detected: {isEyeDetected}\n")
        fr.write(f"{i},{end-start:.10f},{isEyeDetected}\n")
        
        i += 1
        isEyeDetected = 0 #restart the trigger 


        timer += (end - start)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    ratio = precision(countEye, countError)
    print(f"Precision {ratio}")
    
    closeFlow(cap,GPIO_LED)
    
if __name__ == "__main__":
    #main(0)
    main("poubelle")


## précision bonnes Led allumée + stats sur la nombre de détection de bouches // aux yeux

#nberror // (nbbouch +nboeil) -> pourcentage de détection de bouche // nb de détection
# Précision : ratio bouche détection, ratio 1 seul oeil détecté
#find what is x,x2 y,y2 (top, bottum left, right corner) ?