import os
import sys
from src.AttackRemoval import AttackRemoval
from src.parse_apx import parse_func_apx
def main(): 
    
# Vérification des arguments de la ligne de commande
    if len(sys.argv) != 3 or sys.argv[1] != "-f" :
        print("Utilisation : python main.py -f <fichier.apx>")
        exit(1)

    # Récupération et transformation du chemin en absolu
    af_file = os.path.abspath(sys.argv[2])
    if not os.path.isfile(af_file):
        print(f"Erreur : le fichier '{af_file}' n'existe pas.")
        exit(1)

    # # Vérification de la sémantique (option commande)
    # semantics = sys.argv[4].upper()
    # if semantics not in ["PR", "CO"]:
    #     print("Erreur : La sémantique doit être 'PR' (préférée) ou 'CO' (complète).")
    #     exit(1)

    filename = os.path.basename(af_file)
    if filename.startswith("PR_"):
        semantics = "PR"
    elif filename.startswith("CO_"):
        semantics = "CO"
    else:
        print("Erreur : le nom du fichier ne contient pas une sémantique reconnue (PR_ ou CO_)")
        exit(1)

    # Charger le fichier .apx avec pygarg
    arguments, attacks, votes = parse_func_apx(af_file)

    # print("Arguments:", arguments)
    # print("Attaques:", attacks)
    
    attRe = AttackRemoval(arguments,attacks,votes)
    attRe.get_results(semantics)
    # attRe.save_to_apx('af1_AR')
    
main()