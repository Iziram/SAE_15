#!/bin/bash

#On récupère le chemin pour pouvoir accéder au fichier de configuration.
chemin="${0::-11}modif.conf"

#On met le contenu du fichier dans une variable puis on vide le fichier.
confs=$(<${chemin})
> ${chemin} 

#Pour chaque booléen du fichier de configuration on inverse sa valeur
for i in $confs
do
    if [ "$i" == "1" ]
    then
        #On utilise un echo -n pour ajouter la valeur dans le fichier sans passer de nouvelle lignes
        echo -n "0 " >> $chemin
    else
        echo -n "1 " >> $chemin
    fi
done 

exit 0;
