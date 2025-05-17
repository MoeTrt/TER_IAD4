import pandas as pd
import matplotlib.pyplot as plt
import os
import ast

df = pd.read_csv("obaf_results.csv")
output_dir = "figures"
os.makedirs(output_dir, exist_ok=True)

# df = df[df["methode"] == "uniforme"]
df = df[df["methode"] == "non_uniforme"]

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

def compare_extensions(returned_exts, true_ext):
    normalized_returned = normalize_extension(returned_exts)
    normalized_truth = normalize_extension(true_ext)
    return normalized_truth[0] in normalized_returned if normalized_truth else False

# Groupes de méthodes pour chaque sous-graphique
method_groups = {
    "AR": ["AR"],
    "CSS_S": ["CSS_S_min", "CSS_S_sum", "CSS_S_leximin"],
    "CSS_D": ["CSS_D_min", "CSS_D_sum", "CSS_D_leximin"],
    "CSS_U": ["CSS_U_min", "CSS_U_sum", "CSS_U_leximin"]
}

# Création de la figure avec 4 sous-graphes
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

# Dictionnaire des noms de colonnes
methods = {
    "AR": "EXT_AR",
    "CSS_S_min": "CSS_S_min",
    "CSS_S_sum": "CSS_S_sum",
    "CSS_S_leximin": "CSS_S_leximin",
    "CSS_D_min": "CSS_D_min",
    "CSS_D_sum": "CSS_D_sum",
    "CSS_D_leximin": "CSS_D_leximin",
    "CSS_U_min": "CSS_U_min",
    "CSS_U_sum": "CSS_U_sum",
    "CSS_U_leximin": "CSS_U_leximin",
}

custom_colors = {
    "AR": "#3142D8",         
    "CSS_S_min": "#8A1538", 
    "CSS_S_sum": "#F4E150",  
    "CSS_S_leximin": "#807B7B",  
    "CSS_D_min": "#8A1538",  
    "CSS_D_sum": "#F4E150",  
    "CSS_D_leximin": "#807B7B",  
    "CSS_U_min": "#8A1538",  
    "CSS_U_sum": "#F4E150",  
    "CSS_U_leximin": "#807B7B",  
}

for i, (group_label, method_list) in enumerate(method_groups.items()):
    ax = axes[i]
    
    for label in method_list:
        col = methods[label]
        match_col = f"match_{label}"
        df[match_col] = df.apply(lambda row: compare_extensions(row[col], row["verite"]), axis=1)
        grouped = df.groupby("fiabilite")[match_col].mean().reset_index()
        grouped["Taux de réussite (%)"] = grouped[match_col] * 100

        ax.plot(grouped["fiabilite"], grouped["Taux de réussite (%)"], 
        marker='o', linewidth=1.5, label=label, color=custom_colors[label])

    ax.set_title(f"Comparaison - {group_label}")
    ax.set_xlabel("Fiabilité")
    ax.set_ylabel("Taux de réussite (%)")
    ax.grid(True)
    ax.legend()

plt.suptitle("Comparaison des groupes de méthodes selon la fiabilité - Votes Non-Uniforme ", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.96])

output_path = os.path.join(output_dir, "taux_reussite_non_uniforme.png")
plt.savefig(output_path, dpi=300)
plt.close()

print(f" Graphique enregistré dans : {output_path}")
