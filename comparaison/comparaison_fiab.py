import pandas as pd
import matplotlib.pyplot as plt
import os
import ast

# Chargement des données
df = pd.read_csv("obaf_results.csv")

# Dossier de sortie
output_dir = "figures"
os.makedirs(output_dir, exist_ok=True)

# Fonction pour parser et normaliser les extensions
def normalize_extension(ext):
    try:
        parsed = ast.literal_eval(ext.strip())
        if isinstance(parsed, list):
            if len(parsed) > 0 and isinstance(parsed[0], list):
                return [sorted([str(arg).strip() for arg in sub]) for sub in parsed]
            else:
                return [sorted([str(arg).strip() for arg in parsed])]
    except:
        pass
    return []

# Fonction de comparaison
def compare_extensions(returned_exts, true_ext):
    normalized_returned = normalize_extension(returned_exts)
    normalized_truth = normalize_extension(true_ext)
    return normalized_truth[0] in normalized_returned if normalized_truth else False

# Méthodes à tracer
methods = {
    "AR": "EXT_AR",
    "CSS_U_min": "CSS_U_min",
    "CSS_U_sum": "CSS_U_sum",
    "CSS_U_leximin": "CSS_U_leximin",
}

# Couleurs personnalisées
custom_colors = {
    "AR": "#3142D8",
    "CSS_U_min": "#8A1538",  
    "CSS_U_sum": "#F4E150",  
    "CSS_U_leximin": "#807B7B",  
}

# ➤ Création du graphique
plt.figure(figsize=(10, 6))

for label, col in methods.items():
    match_col = f"match_{label}"
    df[match_col] = df.apply(lambda row: compare_extensions(row[col], row["verite"]), axis=1)
    grouped = df.groupby("fiabilite")[match_col].mean().reset_index()
    grouped["Taux de réussite (%)"] = grouped[match_col] * 100

    plt.plot(grouped["fiabilite"], grouped["Taux de réussite (%)"],
             marker='o', linewidth=1.5, label=label, color=custom_colors[label])

plt.title("Comparaison des méthodes AR et CSS_U selon la fiabilité", fontsize=14)
plt.xlabel("Fiabilité")
plt.ylabel("Taux de réussite (%)")
plt.grid(True)
plt.ylim(0, 105)
plt.legend()
plt.tight_layout()

# ➤ Sauvegarde
output_path = os.path.join(output_dir, "taux_reussite_AR_CSS_U.png")
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Graphique enregistré dans : {output_path}")
