import sys
import os
import pygarg.dung.apx_parser
import pygarg.dung.solver
from src.scoring import compute_CSS
from src.parse_apx import parse_func_apx
from src.generation import vote_generation

# Vérification des arguments de la ligne de commande
if len(sys.argv) != 9 or sys.argv[1] != "-f" or sys.argv[3] != "-s" or sys.argv[5] != "-a" or sys.argv[7] != "-m":
    print("Utilisation : python main.py -f <fichier.apx> -s <PR|CO> -a <sum|min|leximin> -m <S|D|U>")
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

aggregation = sys.argv[6].lower()
if aggregation not in ["sum", "min", "leximin"]:
    print("Erreur : l'agrégation doit être 'sum', 'min' ou 'leximin'.")
    exit(1)

measure = sys.argv[8].upper()
if measure not in ["S", "D", "U"]:
    print("Erreur : la mesure doit être 'S', 'D' ou 'U'.")
    exit(1)

arguments, attacks, votes_example = parse_func_apx(af_file)
print("Votes lu par le fichier apx :" ,votes_example)

print("Arguments:", arguments)
print("Attaques:", attacks)

# Calculer les extensions avec pygarg
extensions = pygarg.dung.solver.extension_enumeration(arguments, attacks, semantics)  # Sémantique préférée

print("Extensions trouvées:", extensions)

best_extension, best_distance = compute_CSS(votes_example, extensions, arguments, aggregation, measure)

votes, verite = vote_generation(extensions, arguments)


print("Votes générés :", votes)
print("Vérité choisie (vecteur) :", verite)
print("Résultat pour l'aggrégation ",aggregation," et la mesure ",measure)
print("Meilleure extension selon CSS:", best_extension)
print("Distance associée:", best_distance)