import sys
import os
import pygarg.dung.apx_parser
import pygarg.dung.solver
from src.scoring import compute_CSS
from src.parse_apx import parse_func_apx

# Vérification des arguments de la ligne de commande
if len(sys.argv) != 5 or sys.argv[1] != "-f" or sys.argv[3] != "-s":
    print("Utilisation : python main.py -f <fichier.apx> -s <PR|CO>")
    exit(1)

# Récupération et transformation du chemin en absolu
af_file = os.path.abspath(sys.argv[2])
if not os.path.isfile(af_file):
    print(f"Erreur : le fichier '{af_file}' n'existe pas.")
    exit(1)

# Vérification de la sémantique
semantics = sys.argv[4].upper()
if semantics not in ["PR", "CO"]:
    print("Erreur : La sémantique doit être 'PR' (préférée) ou 'CO' (complète).")
    exit(1)

# Charger le fichier .apx avec pygarg
#arguments, attacks = pygarg.dung.apx_parser.parse(af_file)

arguments, attacks, votes_example = parse_func_apx(af_file)
print("Votes :" ,votes_example)

print("Arguments:", arguments)
print("Attaques:", attacks)

# Calculer les extensions avec pygarg
extensions = pygarg.dung.solver.extension_enumeration(arguments, attacks, semantics)  # Sémantique préférée

print("Extensions trouvées:", extensions)

# Exemple d'appel à compute_CSS avec les extensions trouvées (mettre les bons paramètres)
# votes_example = {
#     "v1": {"a":  1, "b": 0, "c":  -1, "d": 1, "e":  -1},
#     "v2": {"a":  1, "b":  -1, "c":  0, "d": 1, "e":  0},
#     "v3": {"a":  -1, "b": 1, "c": 0, "d": 0, "e":  1},
#     "v4": {"a": 0, "b":  1, "c":  -1, "d":  0, "e":  1},
# }
agregation = "leximin"  # sum : Somme , min : Minimum, leximin : Leximin
metric = "U"  # S : Satisfaction , D : Disatisfaction, U : Utility

best_extension, best_distance = compute_CSS(votes_example, extensions, arguments, agregation, metric)

print("Résultat pour l'aggrégation ",agregation," et la mesure ",metric)
print("Meilleure extension selon CSS:", best_extension)
print("Distance associée:", best_distance)