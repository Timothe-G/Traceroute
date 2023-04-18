Le programme commence par importer plusieurs bibliothèques, notamment argparse, csv, sys, Scapy, pathlib, NetworkX et Matplotlib.

La fonction principale du programme est "main(args)", qui prend des arguments en entrée à l'aide du module argparse. Ces arguments comprennent le nom du fichier d'entrée contenant les adresses IP à tracer, le nom du fichier de sortie pour le résultat du traceroute, le dossier de sortie pour sauvegarder les graphiques et plusieurs options de configuration pour le traceroute personnalisé.

La fonction "main(args)" lit le fichier d'entrée et exécute la fonction "traceroute_custom" pour chaque adresse IP fournie. La fonction "traceroute_custom" envoie des paquets avec des valeurs de TTL croissantes jusqu'à ce qu'il atteigne sa destination ou atteigne une valeur maximale de TTL. Les réponses ICMP, UDP et TCP sont stockées dans une liste appelée "result" pour chaque TTL, et cette liste est ajoutée au dictionnaire "results", qui est associé à l'adresse IP correspondante.

Le résultat du traceroute pour chaque adresse IP est enregistré dans le fichier de sortie sous forme de texte. Les adresses IP qui ont atteint leur destination sont exclues du dictionnaire "results". Enfin, la fonction "generate_graph" est appelée pour chaque adresse IP dans le dictionnaire "results", et elle génère un graphique à partir des résultats du traceroute et l'enregistre dans le dossier de sortie.

La fonction "generate_graph" crée un graphique en utilisant la bibliothèque NetworkX et Matplotlib. Le graphique montre les adresses IP atteintes lors du traceroute pour chaque valeur de TTL. Les nœuds du graphique représentent les adresses IP, et les arêtes du graphique représentent les sauts de TTL. La couleur des nœuds est définie en fonction du nombre de sauts de TTL pour atteindre l'adresse IP, et les étiquettes d'arêtes affichent la valeur de TTL correspondante.

En somme, ce code réalise un traceroute personnalisé pour chaque adresse IP fournie, affiche les résultats dans un fichier de sortie sous forme de texte et génère un graphique à partir des résultats du traceroute pour chaque adresse IP, qui est enregistré dans un dossier de sortie spécifié.
