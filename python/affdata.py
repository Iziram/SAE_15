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
   
    y : List[float] = [connectdict["upstream"][0],connectdict["upstream"][25],connectdict["upstream"][50],connectdict["upstream"][75],connectdict["upstream"][100]]
    x : List[float] = [connectdict["temps"][0],connectdict["temps"][25],connectdict["temps"][50],connectdict["temps"][75],connectdict["temps"][100]]

    for i in range(len(connectdict["upstream"])):
        
        if connectdict["upstream"][i] < connectdict["upstream"][i-5]:
            x.append(connectdict["temps"][i])
            y.append(connectdict["upstream"][i])

    fig, axs = plt.subplots()
    axs.scatter(connectdict["temps"], connectdict["upstream"])
    axs.set_title('upstream en fonction du temps')
    axs.axes.set_xticks(x)
    axs.axes.set_yticks(y)
    
    
    

def affmetrique12(connectdict: Dict[str,int]):
    #downstream en fonction du temps
    y : List[float] = [connectdict["downstream"][0],connectdict["downstream"][25],connectdict["downstream"][50],connectdict["downstream"][75],connectdict["downstream"][100]]
    x : List[float] = [connectdict["temps"][0],connectdict["temps"][25],connectdict["temps"][50],connectdict["temps"][75],connectdict["temps"][100]]

    for i in range(len(connectdict["downstream"])):
        
        if connectdict["downstream"][i] < connectdict["downstream"][i-5]:
            x.append(connectdict["temps"][i])
            y.append(connectdict["downstream"][i])

    fig, axs = plt.subplots()
    axs.scatter(connectdict["temps"], connectdict["downstream"])
    axs.set_title('downstream en fonction du temps')
    axs.axes.set_xticks(x)
    axs.axes.set_yticks(y)
    

def affmetrique13(connectdict: Dict[str,int]):
    #ping en fonction du temps
    y : List[float] = [connectdict["ping"][0],connectdict["ping"][25],connectdict["ping"][50],connectdict["ping"][75],connectdict["ping"][100]]
    x : List[float] = [connectdict["temps"][0],connectdict["temps"][25],connectdict["temps"][50],connectdict["temps"][75],connectdict["temps"][100]]

    for i in range(len(connectdict["ping"])):
        
        if connectdict["ping"][i] == 0:
            x.append(connectdict["temps"][i])
        if connectdict["ping"][i-1] == 0 and connectdict["ping"][i+1] == 0:
            x.remove(connectdict["temps"][i])

            

    fig, axs = plt.subplots()
    axs.scatter(connectdict["temps"], connectdict["ping"])
    axs.set_title('ping en fonction du temps')
    axs.axes.set_xticks(x)
    axs.axes.set_yticks(y)

    
    

    
    
    

if __name__ == "__main__":
    a = recupaffmetrique1('./python/connectivityData.csv')
    b = recupaffmetrique2('./python/portData.csv')
    
    #affmetrique1(a)
    #affmetrique12(a)
    affmetrique13(a)
    plt.show()
    
    
    