#!/bin/bash

date=$(date '+%s')

# On n'utilise pas l'option -n puisque cette information est inutile ici
# les options sont nécessaires pour avoir le même nombre de lignes que ce que l'on va traiter en dessous
nb_ports=$(netstat -autA inet | tail -n +3 | wc -l)

for i in $(seq 1 $nb_ports)
do
    # on utilise netstat pour avoir les numéros de ports avec les options aut pour tous les ports utp tcp ouverts/utilisés
    # on utilise l'option -n pour obtenir le numéro de port au lieu du nom du service associé
    # on utilise l'option A inet pour filtrer les ipv4 parmis les ipv6 (problème puisque les ipv6 utilisent des séparateurs : alors que le socket utilise déjà ça)
    # on utilise tail pour enlever l'en-tete de l'affichage
    # on supprime les espaces en trop et on remplace ceux restants par des virgules pour avoir un format csv
    # on récupère la donnée qui nous intéresse, en l'occurence l'interface et le port que l'on va séparer avec une virgule

    # on répète la même opération sans l'option -n pour obtenir le nom du service associé
    # on ajoute le timestamp à la fin
    echo "$(netstat -nautA inet | tail -n +3 | sed -n "$i p" | tr -s ' ' | tr ' ' ',' | cut -d ',' -f 4 | tr ':' ','),$(netstat -autA inet | tail -n +3 | sed -n "$i p" | tr -s ' ' | tr ' ' ',' | cut -d ',' -f 4 | cut -d ':' -f 2),$date"
done;

exit 0;