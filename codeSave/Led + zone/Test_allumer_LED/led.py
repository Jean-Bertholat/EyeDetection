import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs

GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
GPIO.setwarnings(False) #On désactive les messages d'alerte

LED = [13,22,37,35,38,40] #Définit le numéro du port GPIO qui alimente la led
#LED = [11,7,16,12,15,13]

def test(LED):
    for i in LED:
        GPIO.setup(i, GPIO.OUT) #Active le contrôle du GPIO
    
test(LED)

state = GPIO.input(LED[0]) #Lit l'état actuel du GPIO, vrai si allumé, faux si éteint
state1 = GPIO.input(LED[1]) #Lit l'état actuel du GPIO, vrai si allumé, faux si éteint

state2 = GPIO.input(LED[2])
state3 = GPIO.input(LED[3]) 
state4 = GPIO.input(LED[4])
state5 = GPIO.input(LED[5])

if state : #Si GPIO allumé
    GPIO.output(LED[0], GPIO.LOW) #On l’éteint
else : #Sinon
    GPIO.output(LED[0], GPIO.HIGH) #On l'allume
    
if state1 : #Si GPIO allumé
    GPIO.output(LED[1], GPIO.LOW) #On l’éteint
else : #Sinon
    GPIO.output(LED[1], GPIO.HIGH) #On l'allume
"""    
if state : 
    GPIO.output(LED[2], GPIO.LOW) 
else :
    GPIO.output(LED[2], GPIO.HIGH) 
    
if state1 : 
    GPIO.output(LED[3], GPIO.LOW) 
else : 
    GPIO.output(LED[3], GPIO.HIGH)
    
if state : 
    GPIO.output(LED[4], GPIO.LOW) 
else :
    GPIO.output(LED[4], GPIO.HIGH) 
    
if state1 : 
    GPIO.output(LED[5], GPIO.LOW) 
else : 
    GPIO.output(LED[5], GPIO.HIGH)
   """ 
    
    