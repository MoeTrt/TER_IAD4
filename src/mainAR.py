import os
import sys
import pygarg.dung.apx_parser
import AttackRemoval

def main(): 
    
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
    arguments, attacks = pygarg.dung.apx_parser.parse(af_file)

    # print("Arguments:", arguments)
    # print("Attaques:", attacks)

    votes1 = {
    "v1": {"a": 1, "b": 0, "c": 0, "d": -1, "e": 0},
    "v2": {"a": 0, "b": 0, "c": 0, "d": 1, "e": 1},
    "v3": {"a": 1, "b": -1, "c": -1, "d": -1, "e": -1},
    "v4": {"a": -1, "b": 1, "c": 1, "d": -1, "e": -1}
    }

    votes2 = {
    "v1": {"a": 1, "b": 0, "c": -1, "d": 1, "e": -1},
    "v2": {"a": 1, "b": -1, "c": 0, "d": 1, "e": 0},
    "v3": {"a": -1, "b": 1, "c": 0, "d": 0, "e": 1},
    "v4": {"a": 0, "b": 1, "c": -1, "d": 0, "e": 1}
    }
    
    attRe = AttackRemoval.AttackRemoval(arguments,attacks,votes1)
    attRe.get_results(semantics)
    # attRe.save_to_apx('af1_AR')
    
main()