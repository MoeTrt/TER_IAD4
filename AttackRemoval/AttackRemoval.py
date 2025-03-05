import re
import networkx as nx
from collections import defaultdict

import pygarg.dung.solver

class AttackRemoval:
    def __init__(self, arguments, attacks, votes, epsilon=0.1):
        self.arguments = arguments
        self.attacks = attacks
        self.votes = self.aggregate_votes(votes)  
        self.epsilon = epsilon
        self.scores = self.compute_scores() 
        self.modified_attacks = self.modify_attacks() 

    def aggregate_votes(self, votes):
        """Agrège les votes des différents votants pour obtenir v+, v0, v-."""
        aggregated = {arg: [0, 0, 0] for arg in self.arguments}  
        for voter, arg_votes in votes.items():
            for arg, value in arg_votes.items():
                if arg in aggregated:  
                    if value == 1:
                        aggregated[arg][0] += 1  
                    elif value == 0:
                        aggregated[arg][1] += 1 
                    elif value == -1:
                        aggregated[arg][2] += 1  
        return aggregated

    def compute_scores(self):
        """Calcule le score de chaque argument en fonction des votes."""
        scores = {}
        for arg, (pos, abst, neg) in self.votes.items():
            if pos == 0 and neg == 0:
                scores[arg] = 0  
            else:
                scores[arg] = pos / (pos + neg + self.epsilon)
        return scores

    def modify_attacks(self):
        """Supprime les attaques où l'attaquant est plus faible que l'attaqué."""
        new_attacks = set()
        for (x, y) in self.attacks:
            if self.scores[x] >= self.scores[y]:  
                new_attacks.add((x, y))
        return new_attacks

    def get_results(self, semantic):
        """Affiche les résultats de COSAR."""
        if semantic == 'CO':
            sem = 'complètes'
        else :
            sem = 'préférées'
        print("\n **Scores des arguments**")
        for arg, score in self.scores.items():
            print(f"{arg}: {score:.2f}")

        print("\n **Attaques après suppression**")
        for att in self.modified_attacks:
            print(att)

        print(f"\n **Extensions {sem}**")
        print(pygarg.dung.solver.extension_enumeration(self.arguments, self.modified_attacks, semantic))

    def save_to_apx(self, filename):
        """Sauvegarde le nouveau système d'argumentation dans un fichier .apx."""
        with open(filename, 'w') as f:
            for arg in self.arguments:
                f.write(f"arg({arg}).\n")
            for att in self.modified_attacks:
                f.write(f"att({att[0]},{att[1]}).\n")
        print(f"Système d'argumentation sauvegardé dans {filename}")