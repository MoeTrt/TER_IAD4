import re
import networkx as nx
from collections import defaultdict

class AttackRemoval:
    def __init__(self, apx_file, votes, epsilon=0.1):
        self.arguments, self.attacks = self.parse_apx(apx_file) 
        self.votes = self.aggregate_votes(votes)  
        self.epsilon = epsilon
        self.scores = self.compute_scores() 
        self.modified_attacks = self.modify_attacks() 

    def parse_apx(self, filename):
        """Parse un fichier APX et extrait les arguments et attaques."""
        arguments = set()
        attacks = set()
        with open(filename, "r") as file:
            for line in file:
                if match := re.match(r"arg\((\w+)\)\.", line):
                    arguments.add(match.group(1))
                elif match := re.match(r"att\((\w+),(\w+)\)\.", line):
                    attacks.add((match.group(1), match.group(2)))
        return arguments, attacks

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

    def apply_preferred_semantics(self):
        """Trouve une extension préférée après modification des attaques."""
        G = nx.DiGraph()
        G.add_nodes_from(self.arguments)
        G.add_edges_from(self.modified_attacks)

        extensions = []
        for arg in self.arguments:
            if all(pred not in G.nodes for pred in G.predecessors(arg)):
                extensions.append({arg})

        return extensions

    def get_results(self):
        """Affiche les résultats de COSAR."""
        print("\n **Scores des arguments**")
        for arg, score in self.scores.items():
            print(f"{arg}: {score:.2f}")

        print("\n **Attaques après suppression**")
        for att in self.modified_attacks:
            print(att)

        print("\n **Extensions préférées**")
        print(self.apply_preferred_semantics())


apx_file = "af.txt" 

votes = {
    "v1": {"a": 1, "b": -1, "c": 0, "d": -1, "e": 1},
    "v2": {"a": 1, "b": 0, "c": 0, "d": -1, "e": 1},
    "v3": {"a": 1, "b": -1, "c": 0, "d": -1, "e": 1},
    "v4": {"a": -1, "b": 0, "c": 1, "d": 0, "e": 1},
    "v5": {"a": 1, "b": 0, "c": 0, "d": -1, "e": -1},
    "v6": {"a": 1, "b": 1, "c": 0, "d": -1, "e": -1},
}

obaf = AttackRemoval(apx_file, votes)
obaf.get_results()
