import cv2
import io
import numpy as np
import os
import time
from time import sleep
from picamera import PiCamera
import sys
import math
sys.path.append("libs/classification/")
sys.path.append("libs/")
from classification_sample import processImg
from dictionary import dict

#PARAMETRAGE DE LA CAMÉRA ------------------------
camera = PiCamera() #utilisation de la librairie PiCamera()
camera.resolution = (480, 480) #Vidéo de 1024*1024 pixels
camera.framerate = 30 #Nb d'images/s
camera.iso = 100
#camera.start_preview(alpha=100)
camera.image_effect = 'saturation' #Effet d'image #non = default value
camera.brightness = 40
camera.awb_mode  = "shade" #Mise au point de la luminosité
# ------------------------------------------------
i = 0
lock = 0 #Permet de forcer une attente entre 2 symboles pour que l'utilisateur puisse préparer son geste
texte_screen = ""
indx_code = 0
code = ['*','*','*','*']
camera.start_preview() #Affiche le flux vidéo en direct
while(1):    
    start_time = time.time()
    stream = io.BytesIO()
    camera.capture(stream, format="jpeg", resize=(224, 224)) #Prend une "photo"
    stream.seek(0)
    verif_symbol_img = cv2.imdecode(np.fromstring(stream.read(), np.uint8), 1)
    stream.flush()
    t_prise = time.time() - start_time
    start_time = time.time()
    resultat = processImg('libs/network/1miohands-v2.xml', verif_symbol_img) #Appel fonction
    t_traite = time.time() - start_time #Pour mesurer les performances
    print("----- %s s pour prendre l'image -----"%(t_prise))
    print("----- %s s pour traiter l'image -----"%(t_traite))
    if lock == 0 :
        if(resultat[1][resultat[0][0]]>0.5 and resultat[0][0] != 0): #On vérifie qu'un signe a été reconnu
            lock = 1
            texte_screen = str(dict[resultat[0][0]])
            code[indx_code] = texte_screen
            indx_code += 1
        else:
            texte_screen = str(dict[resultat[0][0]]) + ' - ' + "{:.2f}".format(resultat[1][resultat[0][0]]*100) + '%'
    else :
        texte_screen = 'Signe suivant ...'
    #Display result
    texte_screen += "\n"
    for codeI in code :
        texte_screen += str(codeI) #Montre le code enregistré pour le moment
    camera.annotate_text = texte_screen #Affiche le code sur la caméra
    if lock == 1 :
        i += 1
		if i == 3 :
			lock = 0
			i = 0
    
    cv2.waitKey(1)
    print("i = ", i, " | lock = ", lock)
    print('\n')
    if indx_code == 4 : #Le code est enregistré
        texte_fin = ""
        for codeI in code :
            texte_fin += str(codeI)
        print(texte_fin)
        input("Appuyer sur une entrée")
        break; #On arrête le programme

camera.stop_preview() 