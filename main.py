import os
import sys
import re
import pandas as pd
from src.scoring import compute_CSS

# Vérification des arguments de la ligne de commande
if len(sys.argv) != 3 or sys.argv[1] != "-f":
    print("Utilisation : python main.py -f <fichier.apx>")
    exit(1)

# Récupération et transformation du chemin en chemin absolu
af_file = os.path.abspath(sys.argv[2])

# Vérification si le fichier existe
if not os.path.isfile(af_file):
    print(f"Erreur : le fichier '{af_file}' n'existe pas.")
    exit(1)

# Fonction pour lire le fichier .apx et extraire les arguments et attaques
def read_file(af_file):
    liste_arg = set()
    liste_att = set()
    with open(af_file, "r") as my_file:
        for line in my_file:
            match_arg = re.match(r"arg\((.+)\)\.", line)
            if match_arg:
                liste_arg.add(match_arg.group(1))
            match_att = re.match(r"att\((.+),(.+)\)\.", line)
            if match_att:
                liste_att.add((match_att.group(1), match_att.group(2)))
    return liste_arg, liste_att

# Lecture du fichier .apx
arguments, atk = read_file(af_file)

print("Arguments:", arguments)
print("Attaques:", atk)

# Définition des arguments et des votes
all_arguments = list(arguments)  # Conversion en liste pour l'indexation
votes_example = {
    "v1": {"a":  1, "b": 0, "c":  0, "d": -1, "e":  0},
    "v2": {"a":  0, "b":  0, "c":  0, "d": 1, "e":  1},
    "v3": {"a":  1, "b": -1, "c": -1, "d": -1, "e":  1},
    "v4": {"a": -1, "b":  1, "c":  1, "d":  -1, "e":  -1},
}

# Liste des extensions préférées (à remplacer plus tard par un solver)
extensions_pref = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('a', 'e'), ('c', 'e')]

# Calcul du CSS avec différentes méthodes
aggregation_methods = ['sum', 'min', 'leximin']
metrics = ['S', 'D', 'U']

results = []
for agg in aggregation_methods:
    for metric in metrics:
        best_extension, best_distance = compute_CSS(votes_example, extensions_pref, all_arguments, agg, metric)
        results.append({
            "Méthode": agg,
            "Métrique": metric,
            "Extension CSS": best_extension,
            "Distance Maximale": best_distance
        })

# Création et affichage du DataFrame
df_results = pd.DataFrame(results)
print(df_results)