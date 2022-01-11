import csv
import numpy as np
from typing import Dict, List
import matplotlib.pyplot as plt
from dateutil import parser
from datetime import datetime
import sys
import ipywidgets as widgets
from IPython.display import display, clear_output, Markdown

def dateFormatter(epoch:int, _ = None) -> str :
    """!
    @brief Cette fonction permet de convertir un timestamp epoch en une date compréhensible.

    Paramètres : 
        @param epoch : int => timestamp dans le format epoch
        @param _ = None => Un paramètre qui est requis par matplotlib mais non utilisé par la fonction
    Retour de la fonction : 
        @return str => La date compréhensible

    """
    if epoch > 0:
        return str(datetime.fromtimestamp(epoch))
    return ""

def inverseDateFormatter(date: str) -> str:
    return int(parser.parse(date).timestamp())

def secondsToTime(s):
    hour = s // 3600
    s = s % 3600
    minute = s // 60
    s = s % 60
    return f'{hour}:{minute}:{s}'

def xlabels(tmps):
        l = []
        for i in list(tmps):
            if i not in l:
                l.append(dateFormatter(i))
            else:
                l.append("")
        return l


def ticks(tickList : list, axe="x"):
    if axe == "x":
        if len(tickList)> 4:

            x : list = [
                tickList[0],
                tickList[int(len(tickList) * 1/4)], 
                tickList[int(len(tickList) * 2/4)], 
                tickList[int(len(tickList) * 3/4)], 
                tickList[-1]
            ]
            plt.xticks(x, xlabels(x))
        else:
            plt.xticks(tickList, xlabels(tickList))


def _getDico():
    """!
    @brief Cette fonction permet de créer un dictionnaire à partir d'un tableau csv. Le tableau représente les numéros de ports correspondant à des protocols connus
    """
    with open('./python/portsList.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        dico:Dict[int, str] = {} # création du dictionnaire
        for row in csv_reader:
            try:
                dico[int(row[1])] = row[0] #Si la ligne du csv possède un port correct alors on le met dans le dictionnaire en tant que clé et son protocol en tant que valeur
            except:
                pass
    return dico  

_listport = _getDico() #On sauvegarde le dictionnaire pour ne pas le regénérer à chaque appel de fonction.
def converter(port:str) -> str:
    """!
    @brief Cette fonction permet de récuppérer un protocol à partir d'un numéro de port.

    Paramètres : 
        @param port : str => Le numéro de port dont on souhaite connaitre le protocol
    Retour de la fonction : 
        @return str or None => Le protocol associé au numéro de port ou None si aucun n'a été trouvé

    """
    try:
        protocol : str = _listport.get(int(port), "Inconnu")
        return  protocol if protocol != "" else "Inconnu"
    except:
        return "Inconnu"

def recupperationDonnesPorts(chemin:str) -> Dict[str, Dict[int, Dict[str, str or None]]]:
    """!
    @brief Cette fonction permet de récupperer les données relatives à l'activité des ports et de les convertir en un Dictionnaire utilisable par les fonctions suivantes.

    Paramètres : 
        @param chemin : str => Le chemin menant au fichier csv où se trouve les données d'activité des ports.
    Retour de la fonction : 
        @return Dict[str, Dict[int, Dict[str, str]]] => Le dictionnaire représentant les données des ports. 

    """

    dico = {}
    with open(chemin, newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in datareader: # pour chaque ligne du fichier csv
            """
            Les données du csv sont organisées comme suit :
            @ip,port,protocol,timestamp
            """

            interface : str = row[0] #On recuppère l'adresse ip liée à l'interface
            temps : int = int(row[3]) #On récuppère le timestamp
            port : str = row[1] # On récuppère le port
            protocol : str or None = converter(row[2]) # Et on récuppère le protocol, celui-ci étant un numéro de port nous devons le convertir grace à la fonction converter(vue plus haut)
            
            """
            Nous suivons ensuite l'algorithme suivant:

            Si l'adresse ip se trouve déjà dans les clés du dictionnaire principal
                Si le timestamp se trouve déjà dans les clés du dictionnaire associé à l'interface
                    On ajoute un nouveau couple clé valeur (port, protocol) dans le dictionnaire associé au timestamp
                Sinon
                    On crée un nouveau dictionnaire ayant déjà un couple clé valeur (port, protocol) que l'on assigne comme étant le dictionnaire associé au timestamp
            Sinon
                On crée un nouveau dictionnaire ayant pour clé le timestamp et pour valeur un autre dictionnaire avec le couple (port, protocol) que l'on assigne à l'interface 
                courante dans le dictionnaire principal.
            """

            if interface in dico:
                if temps in dico[interface]:
                    dico[interface][temps][port] = protocol
                else:
                    dico[interface][temps] = {port:protocol}
            else:
                dico[interface] = {
                    temps:{port:protocol}
                }
                
    return dico # On renvoie le dictionnaire principal.


def affichageProportionProtocols(portDict: Dict[str, Dict[int, Dict[str, str or None]]], interface:str ="toutes", temps_debut:int=-1, temps_fin:int = float('inf')):
    """!
    @brief Cette fonction permet de générer un diagramme circulaire représentant la proportion des protocols utilisés sur le serveur

    Paramètres : 
        @param portDict : Dict[str,Dict[int,Dict[str,strorNone]]] => Le dictionnaire représentant les données d'activité des ports
        @param interface : str = "toutes" => l'adresse ip de l'interface sur laquelle observer le port, par défaut toutes les interfaces seront affichées.
        @param temps_debut : int = -1 => Le timestamp de début de période, par défaut tous les timestamps seront compris
        @param temps_fin : int = float('inf') => Le timestamp de fin de période, par défaut tous les timestamps seront compris

    """
    
    proto : Dict[str, int] = {}

    if temps_debut == temps_fin:
        temps_fin += 24*3600


    #On récuppère le nombre d'occurences de chaque protocol en fonction de l'interface sélectionnée et de la période sélectionnée
    if interface not in portDict:
        plt.suptitle("Proportion des protocols utilisés sur toutes les interfaces")
        for inter in portDict:
            for temps in portDict[inter]:
                if temps_debut <= temps and temps <= temps_fin:
                    for port in portDict[inter][temps]:
                        protocol: str = portDict[inter][temps][port]
                        if protocol in proto:
                            proto[protocol] += 1
                        else:
                            proto[protocol] = 1
    else:
        plt.suptitle(f"Proportion des protocols utilisés sur l'interface {interface}")
        for temps in portDict[interface]:
                if temps_debut <= temps and temps <= temps_fin:
                    for port in portDict[interface][temps]:
                        protocol: str = portDict[interface][temps][port]
                        if protocol in proto:
                            proto[protocol] += 1
                        else:
                            proto[protocol] = 1
    
    #On transfome notre dictionnaire en deux listes qui seront plus facile à utiliser
    values = list(proto.values())
    labels = list(proto.keys())

    #On trie les listes de façons à avoir les proportions de protocols dans l'ordre décroissant
    labels = sorted(labels, key=lambda x: values[labels.index(x)], reverse=True)
    values.sort(reverse=True)

    #Petite lamda qui servira à formatter l'affichage des pourcentages
    autopct = lambda x: f'{x:.2f}%'


    #Afin d'éviter une surcharge du graphique, nous limitons l'affichage à 5 valeurs pertinantes ou moins.
    if len(values) > 5 :
        #On récuppère les 4 protocols les plus utilisés et on ajoute un nouveau label "Autres"
        x = labels[:5]
        x.append("Autres")
        #On récuppère les 4 valeurs les plus grandes et on ajoute une nouvelle valeur qui est la somme de toutes les autres valeurs
        y = values[:5]
        y.append(sum(values[5:]))
        #On construit le diagramme
        plt.pie(
            y,
            labels=x,
            startangle=0,
            labeldistance=1.25,
            autopct=autopct
        )
    else:
        #On construit le diagramme directement grâce aux valeurs des listes.
        plt.pie(
            values,
            labels=labels,
            startangle=0,
            labeldistance=1.25,
            autopct=autopct
        )

def affichageHistogrameMoyennes(connectdict: Dict[str,List[int]], temps_debut:int=-1, temps_fin:int = float('inf')):
    """!
    @brief Cette fonction permet de générer deux histogrammes. Le premier représentant l'upload et le download et le deuxième le ping

    Paramètres : 
        @param connectdict : Dict[str,List[int]] => dictionnaire représentant les données de connectivité
        @param temps_debut : int = -1 => Le timestamp de début de période, par défaut tous les timestamps seront compris
        @param temps_fin : int = float('inf') => Le timestamp de fin de période, par défaut tous les timestamps seront compris

    """
    
    if temps_debut == temps_fin:
        temps_fin += 24*3600

    #On prépare l'affichage matplotlib
    fig, axes = plt.subplots(nrows= 1, ncols=2, gridspec_kw={'width_ratios': [4, 1]})
    
    #On déclare les variables qui nous seront utiles
    titres : List[str] = ["Upload","Download","Ping"]
    y : Dict[int, int] = {0:0, 1:0, 2:0}
    compteur : Dict[int, int] = {0:0, 1:0, 2:0}
    
    #On récuppère toutes les mesures sur la période concernée
    for tmp in connectdict:
        if temps_debut <= tmp and tmp <= temps_fin:
            for i in range(3):
                y[i] += connectdict[tmp][i]
                compteur[i] += 1

    #Premier graphique : Upload et Download

    #On isole les mesures d'upload et de download et on fait leurs moyennes.
    ry : List[float] = [y[i]/compteur[i] for i in range(2) if compteur[i] != 0]

    #On vérifie qu'on a bien des valeurs à afficher sinon on affiche un histogramme vide
    if len(ry) > 0:
        axes[0].bar(
            range(len(ry)), 
            ry
        )
    else:
        axes[0].bar(
            [0,1],
            [0,0]
        )
    #On configure l'affichage
    axes[0].yaxis.grid(True)
    plt.sca(axes[0])

    #On remplace les valeurs arbitraire des index par les noms de nos mesures
    plt.xticks(range(len(titres)-1), titres[:2])

    plt.ylabel("kilo octet/s")
    axes[0].set_title("Upload / Download")
    
    #On génère l'affichage des valeurs sur les barres de l'histogramme
    for index, value in enumerate(ry):
        axes[0].text(
            index, 
            value//2,
            f'{value:.5}', 
            ha="center", 
            color="black",
            weight="bold",
            size="medium"
        )
    
    # Second Graphique : Ping

    #On effectue la moyenne des pings, si il n'y en a pas on met le plus grand entier possible pour signifier la perte de connectivité
    if compteur[2] != 0:
        ry = y[2]/compteur[2]
    else:
        ry = sys.maxsize

    #On génère l'histogramme
    axes[1].bar(0, ry)

    #On configure l'affichage
    axes[1].yaxis.grid(True)
    plt.sca(axes[1])

    plt.xticks([0], ["Ping"])
    plt.ylabel("millisecondes")
    axes[1].set_title("Moyenne des pings")
    plt.subplots_adjust(wspace=0.4, top=.7)
    
    #On génère l'affichage des valeurs sur les barres de l'histogramme
    axes[1].text(
            0, 
            ry//2,
            f'{float(ry):.5}', 
            ha="center", 
            color="black",
            weight="bold",
            size="medium"
        )
        
    #On récuppère le premier et dernier timestamp qui seront utilisé pour montrer la période choisie
    p_deb = dateFormatter(list(connectDict.keys())[0])
    p_fin = dateFormatter(list(connectDict.keys())[-1])

    #Si l'utilisateur à spécifier une autre période alors utilise les paramètres temps_debut et temps_fin
    if temps_debut != -1 :
        p_deb = dateFormatter(temps_debut)
    if temps_fin != float('inf'):
        p_fin = dateFormatter(temps_fin)
    
    #On affiche le titre avec la période choisie.
    plt.suptitle(f"Moyennes des différentes mesures\n Sur la période {p_deb} -> {p_fin}", fontsize=18)

portDict = recupperationDonnesPorts("./python/portData.csv")

affichageProportionProtocols(portDict)
plt.show()
