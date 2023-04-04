# Traceroute

## - Pré-requis -

  - Pour utiliser ce script de traceroute sous python, il est recommande d'utiliser la version de Python 3.7.3 (script testé sur cette version).
  - Ensuite, vous devez posséder les modules NetworkX, Matplotlib et Scapy. Pour les installer pour Python 3, voici la commande:
  ```
  pip3 install networkx matplotlib scapy
  ```
  
## - Utilisation de la commande -

Pour lancer le script il suffit de faire cette commande en se situant dans le même répertoire que le script:
 ```
 python3 traceroute.py [fichier source] [fichier de sortie] (options)
 ```
 
Plusieurs options sont à disposition, les voici:
 ```
 --output-dir : Spécifie un nom pour le dossier de sortie. S'il n'existe pas, le dossier est créé. Valeur par défaut : "graphs"
 --min-ttl : Spécifie une valeur de TTL minimale. Valeur par défaut : 1
 --max-ttl : Spécifie ue valeur de TTL maximale. Valeur par défaut : 30
 --n-series : Spécifie le nombre de série (une série est constitué d'un paquet UDP, TCP, et ICMP) pour chaque étape d'exploration. Valeur par défaut : 1
 --udp-port : Spécifie un port UDP. Valeur par défaut: 33434
 --tcp-port : Spécifie un port TCP. Valeur par défaut: 80
 --icmp-type : Spécifie un type ICMP. Valeur par défaut: 8
 --timeout : Spécifie le temps d'attente entre chaque paquets en secondes. Valeur par défaut: 1
 --packet-size : Spécifie la taille d'un paquet en bytes. Valeur par défaut : 60
  ```
