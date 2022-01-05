import csv
import numpy as np
from typing import Dict, Protocol, Tuple, List
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
from protocolConverter import converter
def affmetrique31(portDict: Dict[str,np.ndarray], interface="toutes", temps_debut:int=-1, temps_fin:int = -1):
    times = {}
    fig, axs = plt.subplots()
    if interface not in portDict:
        fig.suptitle("Nombre de port ouverts par rapport au temps (toutes interfaces)", fontsize=24)
        if temps_debut == -1 or temps_fin == -1:
            for inter in portDict:
                for temps in portDict[inter]:
                    if temps in times :
                        times[temps] += len(portDict[inter][temps])
                    else:
                        times[temps] = len(portDict[inter][temps])
    else:
        fig.suptitle(f"Nombre de port ouverts par rapport au temps (Interface : {interface})", fontsize=24)
        for temps in portDict[interface]:
                    if temps in times :
                        times[temps] += len(portDict[interface][temps])
                    else:
                        times[temps] = len(portDict[interface][temps])
    
    axs.bar(times.keys(),times.values(), width=4)
    axs.xaxis.set_major_formatter(dateFormatter)
    fig.autofmt_xdate()
    


def affmetrique32(portDict, port, interface="toutes"):
    fig, axs = plt.subplots()
    inters : list = list(portDict.keys())
    if interface not in portDict:
        fig.suptitle(f"Affichage de l'état du port {port} pour chaque interface", fontsize=24)
        tmps = []
        interfaces = []
        for inter in portDict:
            for temps in portDict[inter]:
                if port in portDict[inter][temps]:
                    tmps.append(temps)
                    interfaces.append(inters.index(inter))
        axs.scatter(tmps, interfaces)
    else:
        fig.suptitle(f"Affichage de l'état du port {port} sur l'interface {interface}", fontsize=24)
        inters = [interface]
        times = {}
        for temps in portDict[interface]:
            if port in portDict[interface][temps]:
                times[temps] = 0
        axs.scatter(times.keys(), times.values())
    
    def interFormatter(id,_)->str:
        if id in [float(i) for i in range(len(inters))]:
            return inters[int(id)]
        else:
            return ""
    
    axs.xaxis.set_major_formatter(dateFormatter)
    axs.yaxis.set_major_formatter(interFormatter)
    fig.autofmt_xdate()


def dateFormatter(epoch:int, _) -> str :
    import datetime
    datetime = datetime.datetime.fromtimestamp(epoch)
    return datetime

def transformationCsvDicoMetrique2(path:str):
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


if __name__ == "__main__":
    # a = recupaffmetrique1('./python/connectivityData.csv')
    b = transformationCsvDicoMetrique2('./python/portData.csv')
    affmetrique32(b, "36847")
    affmetrique31(b)
    # affmetrique1(a)
    # affmetrique12(a)
    # affmetrique13(a)
    plt.show()
    