import os
import re
import csv
import networkx as nx
import pygarg.dung.apx_parser
from pygarg.dung.solver import extension_enumeration
from collections import defaultdict

#  Dossier contenant les fichiers .apx
folder_path = "./graph/BA"

#  Paramètres
semantics = "PR"
categories = ["10", "20", "30"]
pbCycle_list = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

# Stockage par (numArg, pbCycle)
files_by_category_pb = defaultdict(list)

for filename in os.listdir(folder_path):
    if not filename.endswith(".apx"):
        continue

    #  Extraire numArg et pbCycle
    cat_match = re.search(r'numArg(\d+)', filename)
    pb_match = re.search(r'pbCycle([0-9.]+)', filename)
    if not cat_match or not pb_match:
        continue

    category = cat_match.group(1)
    pb_cycle = float(pb_match.group(1))

    if category not in categories or pb_cycle not in pbCycle_list:
        continue

    full_path = os.path.join(folder_path, filename)

    try:
        arguments, attacks = pygarg.dung.apx_parser.parse(full_path)
    except Exception as e:
        print(f" Erreur fichier {filename} : {e}")
        continue

    # Vérifie la présence d’un cycle
    G = nx.DiGraph()
    G.add_nodes_from(arguments)
    G.add_edges_from(attacks)

    if not any(nx.simple_cycles(G)):
        continue

    #  Calcule les extensions préférées
    extensions = extension_enumeration(arguments, attacks, semantics)

    if len(extensions) < 2:
        continue

    key = (category, pb_cycle)
    files_by_category_pb[key].append((filename, len(extensions)))

#  Sélection finale : max 2 fichiers par (numArg, pbCycle)
final_selection = []

for key, file_list in files_by_category_pb.items():
    file_list.sort(key=lambda x: -x[1])  # Trie par nb d'extensions décroissant
    selected = file_list[:2]
    for filename, ext_count in selected:
        final_selection.append((filename, key[0], key[1], ext_count))

#  Sauvegarde .csv
with open("fichiers_selectionnes.csv", "w", newline="") as f_csv:
    writer = csv.writer(f_csv)
    writer.writerow(["filename", "numArgs", "pbCycle", "num_extensions"])
    for row in final_selection:
        writer.writerow(row)

print(f" {len(final_selection)} fichiers sélectionnés")
print("   - fichiers_selectionnes.txt")
print("   - fichiers_selectionnes.csv")
