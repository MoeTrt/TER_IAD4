import pandas as pd
import matplotlib.pyplot as plt
import ast
import os

# Chargement des données
df = pd.read_csv("obaf_results.csv")

# Dossier de sortie
output_dir = "figures"
os.makedirs(output_dir, exist_ok=True)

# Fonction pour normaliser les extensions
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

# Fonction pour comparer les extensions retournées avec la vérité
def compare_extensions(returned_exts, true_ext):
    normalized_returned = normalize_extension(returned_exts)
    normalized_truth = normalize_extension(true_ext)
    return normalized_truth[0] in normalized_returned if normalized_truth else False

# On garde uniquement AR et CSS_U
methods = {
    "AR": "EXT_AR",
    "CSS_U_min": "CSS_U_min",
    "CSS_U_sum": "CSS_U_sum",
    "CSS_U_leximin": "CSS_U_leximin",
}

colors = {
    "AR": "#3142D8",
    "CSS_U_min": "#8A1538",  
    "CSS_U_sum": "#F4E150",  
    "CSS_U_leximin": "#807B7B",
}

# Création de la figure avec deux sous-graphiques : BA et WS
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
types = ["BA", "WS"]

for i, t in enumerate(types):
    ax = axes[i]
    df_type = df[df["type"] == t]
    
    for label, col in methods.items():
        match_col = f"match_{label}"
        df_type[match_col] = df_type.apply(lambda row: compare_extensions(row[col], row["verite"]), axis=1)
        grouped = df_type.groupby("fiabilite")[match_col].mean().reset_index()
        grouped["Taux de réussite (%)"] = grouped[match_col] * 100
        
        ax.plot(grouped["fiabilite"], grouped["Taux de réussite (%)"], 
                marker='o', linewidth=1.5, label=label, color=colors[label])
    
    ax.set_title(f"Graphe {t}")
    ax.set_xlabel("Fiabilité")
    ax.set_ylabel("Taux de réussite (%)")
    ax.grid(True)
    ax.set_ylim(0, 105)
    ax.legend()

plt.suptitle("Comparaison des méthodes AR et CSS_U selon la fiabilité (BA vs WS)", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.94])

# Sauvegarde
output_path = os.path.join(output_dir, "courbes_fiabilite_AR_CSS_U_par_type_graph.png")
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Graphique enregistré dans : {output_path}")
