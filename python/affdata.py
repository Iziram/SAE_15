import csv
import numpy as np
from typing import Dict, Protocol, Tuple, List
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
    conectDict: Dict[str,np.ndarray] = {"upstream":np.ndarray([]), "downstream":np.ndarray([]), "ping":np.ndarray([]), "temps":np.ndarray([])}
    up : int 
    down : int
    tps : int
    pg : int
    
    #parti du programme qui récupère le fichier csv de la métrique 1 pour ensuite le metre sous forme d'un dictionnaire
    with open(metrique1, newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in datareader:
           up = row[0]
           down = row[1]
           pg = row[2]
           tps = row[3]
           conectDict["upstream"] = np.append(conectDict["upstream"],up)
           conectDict["downstream"] = np.append(conectDict["downstream"],down)
           conectDict["ping"] = np.append(conectDict["ping"],pg)
           conectDict["temps"] = np.append(conectDict["temps"],tps)
        
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
    plt.scatter(connectdict["temps"], connectdict["upstream"], linewidth=2.0)
    plt.suptitle('upstream en fonction du temps')
    plt.show()
def affmetrique12(connectdict: Dict[str,int]):
    #downstream en fonction du temps
    plt.scatter(connectdict["temps"], connectdict["downstream"], linewidth=2.0)
    plt.suptitle('downstream en fonction du temps')
    plt.show()
def affmetrique13(connectdict: Dict[str,int]):
    #ping en fonction du temps
    plt.scatter(connectdict["temps"], connectdict["ping"], linewidth=2.0)
    plt.suptitle('ping en fonction du temps')
    plt.show()

    
    

    
    
    

if __name__ == "__main__":
    a = recupaffmetrique1('./python/connectivityData.csv')
    b = recupaffmetrique2('./python/portData.csv')
    #affmetrique31(b)
    affmetrique1(a)
    affmetrique12(a)
    affmetrique13(a)
    
    