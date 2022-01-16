#!/bin/bash
#On demande en paramètre du script 1) l'adresse de la machine/serveur à "ping" 2) l'adresse d'un fichier à télécharger
if [ $# -gt 1 ]
then

    #On récupère le chemin du dossier dans lequel se trouve le script car on va devoir utiliser plusieurs autres fichiers qui s'y trouvent
    chemin=${0::-15}

    #On créer une variable "key" qui contient le chemin vers la clé privée qui sera utiliser pour se connecter au vps de Matthias 
    key="${chemin}iutsshkey"

    #On récupère le temps de connectivité grace à un ping
    ping=$(ping -c 1 $1 | grep "time=" | cut -d " " -f 8 | tr -d "time=")

    #On récupère le débit descendant grace a la commande curl 
    download_number=`curl -w '%{speed_download}\n' $2 |& tail -n 1`

    #On récupère le débit montant grace à l'upload de la clé privé sur le vps de Matthias. 
    upload_number=`scp -vi $key $key iut@iziram.fr:/home/iut/upload |& tail -n 2 | head -n 1 | cut -d " " -f 5`
    upload_number=${upload_number::-1}

    #Le débit montant récupéré est en Kbit/s donc on le converti en Ko/s
    upload_number=`bc <<< $upload_number*1000 `
    upload_number=`bc <<< $upload_number/8 `
    upload_number=`bc <<< $upload_number/1000 `
    #On récupère la date sous la forme d'un timestamp
    depoch=$(date +%s)

    #Afin d'avoir des observations intéressantes on utilise le Script modifConnectivity.sh. Celui-ci ajoutera ou non une valeur aléatoire au valeur observée
    #De cette façon on aura pas de valeur trop constantes
    ping=$($modifier ping $ping)
    upload_number=$($modifier upload $upload_number)
    download_number=$($modifier download $download_number)

    #On affiche dans la sortie nos valeurs
    echo "$ping,$download_number,$upload_number,$depoch"
fi

exit 0;