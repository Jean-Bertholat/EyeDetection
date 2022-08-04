# test de la caméra picamera.py
# importer les paquets requis pour la Picaméra
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import numpy as np
import time


# initialisation des paramètres pour la capture
"""camera = PiCamera()
camera.resolution = (800, 600)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(800, 600))"""


# initialiser la caméra du pi, attendre 2s pour la mise au point ,
# initialiser le compteur FPS
print("...démarrage de la Picamera...")
vs = VideoStream(usePiCamera=True, resolution=(1600, 1200)).start()
time.sleep(2.0)
fps = FPS().start()

print("Init Done\n")

# récupération du flux vidéo, redimension 
# afin d'afficher au maximum 800 pixels 
frame = vs.read()
frame = imutils.resize(frame, width=800)

# capture du flux vidéo
"""for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    print("Capturing\n")
# recupère à l'aide de Numpy le cadre de l'image, pour l'afficher ensuite à l'écran
    image = frame.array"""

while (True):
    # affichage du flux vidéo
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # initialisation du flux 
    #rawCapture.truncate(0)

    # si la touche q du clavier est appuyée, on sort de la boucle
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()
vs.stop()