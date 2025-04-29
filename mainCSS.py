import sys
import os
# import pygarg.dung.apx_parser
import pygarg.dung.solver
from src.scoring import compute_CSS
from src.parse_apx import parse_func_apx
from src.generation import vote_generation

# Vérification des arguments de la ligne de commande
if len(sys.argv) != 9 or sys.argv[1] != "-f" or sys.argv[3] != "-s" or sys.argv[5] != "-a" or sys.argv[7] != "-m":
    print("Utilisation : python main.py -f <fichier.apx> -a <sum|min|leximin> -m <S|D|U>")
    exit(1)

# Récupération et transformation du chemin en absolu
af_file = os.path.abspath(sys.argv[2])
if not os.path.isfile(af_file):
    print(f"Erreur : le fichier '{af_file}' n'existe pas.")
    exit(1)

filename = os.path.basename(af_file)
if filename.startswith("PR_"):
    semantics = "PR"
elif filename.startswith("CO_"):
    semantics = "CO"
else:
    print("Erreur : le nom du fichier ne contient pas une sémantique reconnue (PR_ ou CO_)")
    exit(1)

# # Vérification de la sémantique (option commande)
# semantics = sys.argv[4].upper()
# if semantics not in ["PR", "CO"]:
#     print("Erreur : La sémantique doit être 'PR' (préférée) ou 'CO' (complète).")
#     exit(1)

aggregation = sys.argv[4].lower()
if aggregation not in ["sum", "min", "leximin"]:
    print("Erreur : l'agrégation doit être 'sum', 'min' ou 'leximin'.")
    exit(1)

measure = sys.argv[6].upper()
if measure not in ["S", "D", "U"]:
    print("Erreur : la mesure doit être 'S', 'D' ou 'U'.")
    exit(1)

arguments, attacks, votes = parse_func_apx(af_file)

# print("Votes lu par le fichier apx :" ,votes)
# print("Arguments:", arguments)
# print("Attaques:", attacks)

extensions = pygarg.dung.solver.extension_enumeration(arguments, attacks, semantics) 

# print("Extensions trouvées:", extensions)
# votes, verite = vote_generation(extensions, arguments)

best_extension, best_distance = compute_CSS(votes, extensions, arguments, aggregation, measure)

# print("Votes générés :", votes)
# print("Vérité choisie (vecteur) :", verite)
print("Résultat pour l'aggrégation",aggregation," et la mesure",measure)
print("Meilleure extension selon CSS:", best_extension)
print("Distance associée:", best_distance)

