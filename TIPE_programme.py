from __future__ import print_function
import cv2 as cv
import argparse # module d'analyse de ligne de commande (traitement d'argument)

# On crée la fonction qui va détecter le visages et les yeux.
def detectAndDisplay(frame): # frame = lit le flux camera (Matrice qui contient la couleur de chaque pixel) (IMAGE 1 frame et frame_gay)
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # Convertit une image d'un espace colorimétrique à un autre (Ici en gris)
    frame_gray = cv.equalizeHist(frame_gray) # L'algorithme normalise la luminosité et augmente le contraste de l'image.

    #print(frame_gray) # Renvoie les couleurs liée à chaque pixel (3 sous-pixels respectivement RGB chaque coder de 0 à 255) de l'image dans une matrice. (IMAGE 2)
    #print(frame_gray.shape) # Renvoie la taille de la matrice (IMAGE 3)

    """#-- Detect faces"""

    faces = face_cascade.detectMultiScale(frame_gray) # Renvoie la matrice [[X,Y,W,H]] (Si 2 tête détecter : [[][]]) (IMAGE 4). Le repère (Image 5)
    for (x,y,w,h) in faces: # On a une boucle pour si on a plusieurs tête
        center = (x + w//2, y + h//2) # Prend le centre de la tête 
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4) # Dessine une ellipse autour de la tête (arg : img, centre, taille, angle_départ, angle_fin, couleur, epaisseur) 
        
        faceROI = frame_gray[y:y+h,x:x+w] # On ne prend que la partie supérieur de notre image pour ne pas détecter la bouche par exemple comme un oeil. (IMAGE 6)

        """#-- In each face, detect eyes"""  # Pareil que faces

        eyes = eyes_cascade.detectMultiScale(faceROI) # Renvoie la matrice [[X,Y,W,H]] (IMAGE 7)

        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25)) # On détermine le rayon du cercle
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4) # Ici on rajoute un cercle sur notre image 

    cv.imshow('Capture - Face detection', frame) # Permet d'ouvrir la fenêtre

# Partie IA (reconnaissance d'objet)
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.') # On crée un objet analyseur (On lui donne un nom)
    # Et indique quels arguments il peut prendre
parser.add_argument('--face_cascade', help='Path to face cascade.', default='data/haarcascades/haarcascade_frontalface_alt.xml') # (nom, nom de ce qu'il fait, le chemin du fichier dans lequel il va chercher les arguments)
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0) # Ajout la camera0 a l'objet.

args = parser.parse_args() # On crée un autre objet qui prend tout les arguments

face_cascade_name = args.face_cascade # On définie variable locale qui contient les données du fichier qui nourrit l'IA
eyes_cascade_name = args.eyes_cascade

face_cascade = cv.CascadeClassifier() # On définie l'IA
eyes_cascade = cv.CascadeClassifier()


"""#-- 1. Load the cascades""" # On donne a manger à l'IA 

if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)

camera_device = args.camera


"""#-- 2. Read the video stream"""

cap = cv.VideoCapture(camera_device) # Ouvre le flux caméra
if not cap.isOpened: # Si rien ne s'ouvre retourne une erreur
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read() # On lit le flux caméra

    if frame is None: # Si on ne lit rien retourne une erreur
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame) # On lance notre algorithme pour repérer les yeux ...

    if cv.waitKey(1) & 0xFF == ord('q'): # Appuyer sur q pour arrêter l'algorithme. 
        break
cap.release() # On arrete de lire le flux
cv.destroyAllWindows() # On ferme la fênetre d'affichage de notre ordi.
