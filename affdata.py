import csv
import numpy as np
from typing import Dict, Protocol, Tuple
import matplotlib.pyplot as plt


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
    portDict: Dict[str,np.ndarray] = {"port": np.ndarray([]), "protocol":np.ndarray([]), "temps": np.ndarray([])}
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
            if protoc == "UDP":
                proto = 0
            if protoc == "TCP":
                proto = 1
            if protoc == "HTTP":
                proto = 2
            if protoc == "HTTPS":
                proto = 3
            if protoc == "NTP":
                proto = 4
            portDict["port"] = np.append(portDict["port"],port)
            portDict["protocol"] = np.append(portDict["protocol"],proto)
            portDict["temps"] = np.append(portDict["temps"],tps2)
    return portDict





def afftabmetrique3(portDict: Dict[str,np.ndarray]):
    i : int =0
    while i != len(portDict["temps"]):
        plt.plot([portDict[i]["temps"]],[portDict[i]["port"]])
        i+=1
    plt.ylabel("numéro de port")
    plt.xlabel("Temps")
    plt.show()
    
    

if __name__ == "__main__":
    #recupaffmetrique1('connectivityData.csv')
    print(recupaffmetrique2('portData.csv'))
    afftabmetrique3(recupaffmetrique2('portData.csv'))
    