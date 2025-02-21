import pandas as pd
from src.scoring import compute_CSS

# Définition des arguments et des votes
all_arguments = ['a', 'b', 'c', 'd', 'e']
votes_example = {
    "v1": {"a":  1, "b": -1, "c":  0, "d": -1, "e":  1},
    "v2": {"a":  1, "b":  0, "c":  0, "d": -1, "e":  1},
    "v3": {"a":  1, "b": -1, "c":  0, "d": -1, "e":  1},
    "v4": {"a": -1, "b":  0, "c":  1, "d":  0, "e":  1},
    "v5": {"a":  1, "b":  0, "c":  0, "d": -1, "e": -1},
    "v6": {"a":  1, "b":  1, "c":  0, "d": -1, "e": -1},
}

# Liste des extensions préférées
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
