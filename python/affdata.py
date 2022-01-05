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

def recupaffmetrique2(metrique2: str)-> Dict[str,np.ndarray]:
    #variable utilisé pour la métrique 3
    portDict: Dict[str,np.ndarray] = {"port": np.ndarray([]), "protocol":str(), "temps": np.ndarray([])}
    port : int
    proto : int = -1
    protoc: str
    tps2: int
    #parti du programme qui récupère le fichier csv de la métrique 3 pour ensuite le metre sous forme d'un dictionnaire
    with open(metrique2, newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in datareader:
            port = row[0]
            protoc = row[1]
            tps2 = row[2]
            converter(protoc)
            portDict["port"] = np.append(portDict["port"],port)
            portDict["protocol"] = np.append(portDict["protocol"],proto)
            portDict["temps"] = np.append(portDict["temps"],tps2)
    return portDict


def affmetrique1(connectdict: Dict[str,int]):
    
    #upstream en fonction du temps
    plt.plot(connectdict["temps"], connectdict["upstream"], linewidth=2.0)
    plt.set_title('upstream en fonction du temps')
    
def affmetrique12(connectdict: Dict[str,int]):
    #downstream en fonction du temps
    plt.plot(connectdict["temps"], connectdict["downstream"], linewidth=2.0)
    plt.set_title('downstream en fonction du temps')
def affmetrique13(connectdict: Dict[str,int]):
    #ping en fonction du temps
    plt.plot(connectdict["temps"], connectdict["ping"], linewidth=2.0)
    plt.set_title('ping en fonction du temps')

def affmetrique31(portDict: Dict[str,np.ndarray]):
    #nombre de port ouvert en fonction du temps
    a : List[int] = portDict["port"]
    b : List[int] = portDict["temps"]
    c : List[int] = [] 
    d : List[int] = []
    e : List[int] = []
    f : List[int] = []
    for i in a:
        t : int = b[0]
        t1 : int
        t2 : int
        for y in b:
            if y == t:
                c.append(i)
            else:
                d.append(len(c))
                c.clear()
                t = y
    for i in d:
        if i not in e:
            e.append(i)
    for i in b:
        if i not in f:
            f.append(i)
    
    plt.bar(f, e, width=1, edgecolor="white", linewidth=0.7)
    plt.set_title('le nombre de port ouvert en fonction du temps')

    
    

if __name__ == "__main__":
    a = recupaffmetrique1('./python/connectivityData.csv')
    b = recupaffmetrique2('./python/portData.csv')
    affmetrique31(b)
    affmetrique1(a)
    affmetrique12(a)
    affmetrique13(a)
    plt.show()
    