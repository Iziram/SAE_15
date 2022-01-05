"""! @brief Simple script qui génère des fausses données pour permettre à Victor d'avancer dans attendre les scripts bash
 @file LoremDataGenerator.py
 @section libs Librairies/Modules
  - os
  - random

 @section authors Author(s)
  - Créé par [Prénom] [Nom] le [Date] .
"""
from os import remove, path
from random import randint
def generatePortData(path:str ="./portData.csv"):
    """!
    @brief Cette fonction génère les données csv concernant les ports d'une machine fictive

    Paramètre(s) : 
        @param path : str = "./portData.csv" => le chemin du fichier qui sera créé de la forme (n°port:int, protocole:str, temps:int)

    """
    removeFileIfExists(path)
    time : int = 1638188438
    protocol : list = [22,23,443,80,8080,68]
    ip : list = ["1.2.3.4","10.1.1.1","0.0.0.0"]
    lines : list = []
    for i in range(5):
            port : list = [ randint(1, 65000) for x in range(randint(1, 100))]
            for p in port :
                lines.append(f'{ip[randint(0, 2)]},{p},{protocol[randint(0,len(protocol)-1)]},{time}\n')
            time += 60
    with open(path,'w') as file :
        file.writelines(lines)

def removeFileIfExists(paths:str):
    """!
    @brief Cette fonction supprime le fichier s'il existe

    Paramètre(s) : 
        @param paths : str => Le chemin du fichier

    """
    if path.exists(paths):
        remove(paths)

def generateConnectivityData(path : str = "./connectivityData.csv"):
    """!
    @brief Cette fonction génère les données csv concernant la connectivité d'une machine fictive

    Paramètre(s) : 
        @param path : str = "./connectivityData.csv" => le chemin du fichier qui sera créé dans la forme (upstream:int, downstream:int, ping:int,temps:int)

    """
    removeFileIfExists(path)
    time : int = 1638188438
    lines : list = []
    
    for i in range(100):
        lines.append(f'{randint(1, 2000)},{randint(1, 2000)},{randint(1, 2000)},{time}\n')
        time += 60
    with open(path,'w') as file :
        file.writelines(lines)

if __name__ == "__main__":
    generatePortData()
    generateConnectivityData()