import csv
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from typing import Dict, Optional, Protocol, Tuple, List
import matplotlib.pyplot as plt
from protocolConverter import converter

def recupaffmetrique1(metrique1: str)-> Dict[str,np.ndarray]:
    """
    la fonction permet de récupérer 2 fichier csv puis de les mettre sous forme d'un Dict[str, np.ndarray]
    Paramètre:
        metrique1 : str ==> chemin du fichier csv de la metrique 1
        metrique2 ; str ==> chemin du fichier csv de la mérique 3
    retour de la fonction:
        la foction retourne 2 Dict[str, np.ndarray]
    """
    #variable utilisé pour la métrique 1
    conectDict: Dict[int,List[int]] = {}
    down : int
    tps : int
    pg : int
    
    #parti du programme qui récupère le fichier csv de la métrique 1 pour ensuite le metre sous forme d'un dictionnaire
    with open(metrique1, newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in datareader:
           up = int(row[0])
           down = int(row[1])
           pg = int(row[2])
           tps = int(row[3])
           conectDict[tps] = [up, down, pg]
        
    return conectDict

def recupaffmetrique2(path:str):
    dico = {}
    
    with open(path, newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in datareader:
            interface : str = row[0]
            temps : int = int(row[3])
            
            port_proto : dict = {
                    row[1] : converter(row[2])
                }
            
            if interface in dico:
                if temps in dico[interface]:
                    dico[interface][temps][row[1]] = converter(row[2])
                else:
                    dico[interface][temps] = port_proto
            else:
                dico[interface] = {
                    temps:port_proto}
                
    return dico
    


def affmetrique1(connectdict: Dict[str,int]):
    #upstream en fonction du temps
   
    y : List[int] = []
    for i in connectdict:
        y.append(connectdict[i][0])
    
    fig, axs = plt.subplots()
    axs.scatter(connectdict.keys(),y)
    axs.plot(connectdict.keys(),y,'r:')
    axs.set_title('upstream en fonction du temps')
    
    
    

def affmetrique12(connectdict: Dict[str,int]):
    #downstream en fonction du temps
    y : List[int] = []
    for i in connectdict:
        y.append(connectdict[i][1])
    
    fig, axs = plt.subplots()
    axs.scatter(connectdict.keys(),y)
    axs.plot(connectdict.keys(),y,'r:')
    axs.set_title('downstream en fonction du temps')
    

def affmetrique13(connectdict: Dict[str,int]):
    #ping en fonction du temps
    y : List[int] = []
    for i in connectdict:
        y.append(connectdict[i][2])
  
    fig, axs = plt.subplots()
    axs.scatter(connectdict.keys(),y)
    axs.plot(connectdict.keys(),y,'r:')
    axs.set_title('ping en fonction du temps')
    
    
    

    
    
    

if __name__ == "__main__":
    a = recupaffmetrique1('./python/connectivityData.csv')
    #b = recupaffmetrique2('./python/portData.csv')
    
    affmetrique1(a)
    affmetrique12(a)
    affmetrique13(a)
    plt.show()
    
    
    