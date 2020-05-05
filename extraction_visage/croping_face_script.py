import os
from os import path as os_path
import shutil
import argparse


var_path = os_path.abspath(os_path.split(__file__)[0]) #Récupère le répertoire courant
#print(var_path)

path_ia = var_path + '/van/face_detection_retail_intel'

shutil.rmtree(var_path + '/result_croped_faces') #Supprime le contenu du répertoir et celui-ci
os.makedirs(var_path + '/result_croped_faces') #Recréer le répertoire

ACroper_path = '/ACroper'


def parse_args():
    parser = argparse.ArgumentParser(description = 'Image face croper using Intel® Neural Compute Stick 2.' + ' || Script developed by Thomas LEPINE')
    parser.add_argument( '-p', '--prnt', metavar = 'PRINT_SOMETHING',
                        type=str, default = 'Hello World ! Special thanks to Thonny our IDE <3',
                        help = 'RAJOUTE UNE LIGNE A AFFICHER (C FAIT POUR UN EASTER-EGG)')
    
    parser.add_argument( '--INPUT_DIR', metavar = 'Directory use for the INPUT',
                        type=str, default = var_path + ACroper_path,
                        help = 'Choose your INPUT path (By default is : ' + var_path + ACroper_path + ')')
    
    return parser

#Dossier entrée    DOssier sortie    Arbre utilisé   Arbre de fichier OU Al'arache sur la racine


ARGS = parse_args().parse_args()
prnt = ARGS.prnt
Input_path = ARGS.INPUT_DIR

for Personn in os.listdir(Input_path):
    final_path = var_path + '/result_croped_faces/' + Personn
    variable_de_nommage = 1
    print(prnt)
    if not os.path.exists(final_path):
        os.makedirs(final_path) #Créer le dossier pour stocker les faces cropées s'il n'existe pas déjà
        
    for image in os.listdir(var_path + ACroper_path + '/' + Personn): 
        result_temp_path = var_path + '/van/temp'
        
        os.system('python ' + path_ia + '/face_detection_retail_0004.py' +
                  ' --face_ir ' + path_ia + '/face-detection-adas-0001-fp16.xml  -i '
                      + var_path + ACroper_path + '/'  + Personn + '/' + image + ' --crop ' + result_temp_path + ' --show no') 
        
        
        
        for faceI in os.listdir(result_temp_path): #Toutes les faces extraites
            os.system('mv ' + result_temp_path + '/' + faceI + ' ' + final_path + '/' + Personn + '_' + str(variable_de_nommage) + '.png')
            variable_de_nommage += 1
            
