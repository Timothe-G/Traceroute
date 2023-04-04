import argparse
import csv
import sys
from scapy.all import *
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt

def generate_graph(results, output_dir):
    for ip, result in results.items():
        G = nx.DiGraph()
        G.add_node("Source")

        for ttl, udp_reply, tcp_reply, icmp_reply in result:
            for reply in [udp_reply, tcp_reply, icmp_reply]:
                if reply:
                    src = reply[IP].src
                    G.add_edge("Source" if ttl == 1 else prev_src, src)
                    prev_src = src

        # Créer le graph
        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 10))
        nx.draw(G, pos, node_size=3000, node_color='lightblue', with_labels=True, font_size=12, font_weight='bold')
        edge_labels = {(u, v): f"TTL {v[1:]}" for u, v in G.edges() if not v.startswith("Source")}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        plt.title(f"Traceroute Graph for IP: {ip}")

        # Enregistre le graph
        plt.savefig(f"{output_dir}/{ip}_graph.png")
        plt.close()

def traceroute_custom(ip, min_ttl=1, max_ttl=30, n_series=1, udp_port=33434, tcp_port=80, icmp_type=8, timeout=1, packet_size=60):
    result = []
    for ttl in range(min_ttl, max_ttl + 1):
        udp_reply = None
        tcp_reply = None
        icmp_reply = None

        for _ in range(n_series):
            # UDP
            udp_pkt = IP(dst=ip, ttl=ttl) / UDP(dport=udp_port) / (b'\x00' * packet_size)
            udp_reply = sr1(udp_pkt, timeout=timeout, verbose=0)

            # TCP
            tcp_pkt = IP(dst=ip, ttl=ttl) / TCP(dport=tcp_port, flags="S") / (b'\x00' * packet_size)
            tcp_reply = sr1(tcp_pkt, timeout=timeout, verbose=0)

            # ICMP
            icmp_pkt = IP(dst=ip, ttl=ttl) / ICMP(type=icmp_type) / (b'\x00' * packet_size)
            icmp_reply = sr1(icmp_pkt, timeout=timeout, verbose=0)

            if udp_reply is not None or tcp_reply is not None or icmp_reply is not None:
                break

        result.append((ttl, udp_reply, tcp_reply, icmp_reply))

        if udp_reply is not None and tcp_reply is not None and icmp_reply is not None:
            if udp_reply[IP].src == ip and tcp_reply[IP].src == ip and icmp_reply[IP].src == ip:
                break

    return result

def main(args):
    input_file = args.input_file
    output_file = args.output_file

    ips = []

    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            ips.extend(row)

    results = {}
    for ip in ips:
        result = traceroute_custom(ip, min_ttl=args.min_ttl, max_ttl=args.max_ttl, n_series=args.n_series,
                                   udp_port=args.udp_port, tcp_port=args.tcp_port, icmp_type=args.icmp_type,
                                   timeout=args.timeout, packet_size=args.packet_size)

        # Vérification si la destination est atteinte
        destination_reached = False
        if result[-1][1] is not None and result[-1][1][IP].src == ip:
            if result[-1][2] is not None and result[-1][2][IP].src == ip:
                if result[-1][3] is not None and result[-1][3][IP].src == ip:
                    destination_reached = True

        if not destination_reached:
            results[ip] = result
        else:
            results[ip] = result[:-1]  # Exclure la dernière étape où la destination est atteinte

    with open(output_file, 'w') as f:
        for ip, result in results.items():
            f.write(f"Traceroute results for {ip}:\n")
            for ttl, udp_reply, tcp_reply, icmp_reply in result:
                f.write(f"TTL {ttl}:\n")
                if udp_reply:
                    f.write(f"  UDP: {udp_reply[IP].src}\n")
                if tcp_reply:
                    f.write(f"  TCP: {tcp_reply[IP].src}\n")
                if icmp_reply:
                    f.write(f"  ICMP: {icmp_reply[IP].src}\n")
            f.write("\n")
            
    # Génération des graphs
    generate_graph(results, args.output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Outil de traceroute par Timothé et Nathanaël")
    parser.add_argument("input_file", help="Fichier d'entrée contenant les adresses IP (txt ou csv)")
    parser.add_argument("output_file", help="Fichier de sortie pour le résultat du traceroute")
    parser.add_argument("--output-dir", help="Dossier de sortie pour sauvegarder les graphs", default="graphs")
    parser.add_argument("--min-ttl", type=int, default=1, help="Valeur TTL minimale (défaut: 1)")
    parser.add_argument("--max-ttl", type=int, default=30, help="Valeur TTL maximale (défaut: 30)")
    parser.add_argument("--n-series", type=int, default=1, help="Nombre de série pour chaque étape d'exploration (défaut: 1)")
    parser.add_argument("--udp-port", type=int, default=33434, help="Port UDP (défaut: 33434)")
    parser.add_argument("--tcp-port", type=int, default=80, help="Port TCP (défaut: 80)")
    parser.add_argument("--icmp-type", type=int, default=8, help="Type ICMP (défaut: 8)")
    parser.add_argument("--timeout", type=int, default=1, help="Tmeps d'attente entre chaque paquets (défaut: 1)")
    parser.add_argument("--packet-size", type=int, default=60, help="Taille d'un paquet (défaut: 60)")

    args = parser.parse_args()

    # Créez le répertoire de sortie s'il n'existe pas
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    main(args)