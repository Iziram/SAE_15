#!/bin/bash

#Récuppération de la date en timestamp
date=$(date '+%s')

#Récuppération de la liste des ports ouverts avec netstat -nautA dont on retire l'entête avec tail -n +3 puis on normalise les espaces avec tr -s ' '
infos=$(netstat -nautA inet | tail -n +3 | tr -s ' ')

#Par défaut la boucle 'for' parcourt un texte et utilise ' ' comme délimiteur. Nous le changeons car nous devons délimiter par ligne.
#On retient le précédent délimiteur car nous modifons une variable environnementale et donc nous devrons la remettre à la fin
before=$IFS
#On assigne le nouveau délimiteur, ici un saut de ligne
IFS=$'\n'

#On parcourt notre liste de ports
for ligne in $infos
do
   #On récuppère le socket local et distant dont on obtient le port distant et le port local
   socket_local=`echo $ligne | cut -d " " -f 4`
   socket_distant=`echo $ligne | cut -d " " -f 5`
   port_local=`echo $socket_local | cut -d ':' -f 2`
   port_distant=`echo $socket_distant | cut -d ':' -f 2`

   #On établie une variable "protocol" qui aura comme valeur un numéro de port représentant le protocol.
   protocol="d"
   #On regarde si notre port local est un port connu ou réservé (10000 est une valeur arbitraire)
   if (( port_local > 10000 ));
   then
      #Si le port local est supérieur à 10000 on considère le port distant comme le port représentant 
      protocol=$port_distant
   else
      #Sinon on considère le port local.
      protocol=$port_local
   fi

   #Afin d'avoir des observations intéressantes on utilise le Script modifPorts.sh. S'il renvoit "0" enregistre bien le port, sinon on ne l'enregistre pas.
   chemin=${0::-8}
   if [ "$(${chemin}modifPorts.sh)" == "0" ]
   then
      echo "$(echo $socket_local | cut -d ':' -f 1 ),$port_local,$protocol,$date" >> $1
   fi


done;

#On remet la configuration par défaut du 'For' 
IFS=$before
exit 0;