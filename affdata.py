import csv
import numpy as np
from typing import Dict, Protocol


def recupaffmetrique(metrique1: str, metrique2: str):
    conectDict: Dict[str, np.ndarray ] = {"upstream": np.array([]), "downstream": np.array([]), "ping": np.array([]), "temps": np.array([])}
    upstream: int
    downstream: int
    ping: int
    temps: int
    port : int
    prot : str
    Protocol : int
    tps: int
    portDict: Dict[str, np.ndarray] = {"port" : np.array([]),"prot" : np.array([]), "temps" : np.array([])}
    with open(metrique1, newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in datareader:
           # print(row)
           upstream = row[0]
           downstream = row[1]
           ping = row[2]
           temps = row[3]
           if temps not in conectDict["temps"]:
               conectDict["temps"] = np.array([[temps]])
           
           if ping not in conectDict["ping"]:
               conectDict["ping"] = np.array([[ping]])
            
           if downstream not in conectDict["downstream"]:
               conectDict["downstream"] = np.array([[downstream]])
            
           if upstream not in conectDict["upstream"]:
               conectDict["upstream"] = np.array([[upstream]])
            



    with open ( metrique2, newline='') as csvfile:
        Portreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in Portreader:
            # print(row)
            port = row[0]
            prot = row[1]
            tps = row[3]
            if prot == "UDP":
                protocle = 1
            elif prot == "TCP":
                protocle = 2
            elif prot == "HTTP":
                protocle = 3
            elif prot == "HTTPS":
                protocle = 4
            elif prot == "NTP":
                protocle = 5
            if port not in portDict["port"]:
                portDict["port"] = np.array([[port]])
            
            if protocle not in portDict["prot"]:
                portDict["prot"] = np.array([["prot"]])
            
            if tps not in portDict["temps"]:
                portDict["temps"] = np.array([[tps]])



    
    

if __name__ == "__main__":
    recupaffmetrique('connectivityData.csv','portData.csv')