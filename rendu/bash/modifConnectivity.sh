#!/bin/bash
#le script demande 2 paramètre, 1) le type de mesure que l'on modifie 2) la mesure.
if [ $# -gt 1 ]
then
    #On récupère le chemin pour pouvoir accéder au fichier de configuration.
    chemin=${0::-20}
    
    #On lit le fichier et on prend le premier chiffre qui s'y trouve, il correspond à un booléen disant si on doit ou non modifier les observations des mesures.
    conf=$(cat ${chemin}modif.conf | cut -d " " -f 1)
    if [ "$conf" == "1" ]
    then
        if [ "$1" == "ping" ]
        then
            #Si on modifie un ping on doit ajouter une valeur positive inférieur à 500
            rdm=$((1 + $RANDOM % 500))
            val=$(bc <<< $rdm+"$2");
            echo $val;
        else
            #Sinon on modifie les autres valeurs en ajoutant un nombre aléatoire entre -200 et 599
            rdm=$((-200 + $RANDOM % 600))
            val=$(bc <<< $rdm+$2);
            echo ${val#-}
        fi
    else
        #Si on ne modifie pas les mesures on renvoit juste la mesure non modifiée
        echo $2
    fi
fi
exit 0;