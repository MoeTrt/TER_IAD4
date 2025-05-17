import pandas as pd
import matplotlib.pyplot as plt
import os
import ast

df = pd.read_csv("obaf_results_WS.csv")

output_dir = "figures/WS"
os.makedirs(output_dir, exist_ok=True)

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

# ➤ On ne garde que AR et CSS_U
method_groups = {
    "AR": ["AR"],
    "CSS_U": ["CSS_U_min", "CSS_U_sum", "CSS_U_leximin"]
}

methods = {
    "AR": "EXT_AR",
    "CSS_U_min": "CSS_U_min",
    "CSS_U_sum": "CSS_U_sum",
    "CSS_U_leximin": "CSS_U_leximin",
}

custom_colors = {
    "AR": "#3142D8",
    "CSS_U_min": "#8A1538",  
    "CSS_U_sum": "#F4E150",  
    "CSS_U_leximin": "#807B7B",  
}

# ➤ Création de la figure avec seulement 2 sous-graphiques
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes = axes.flatten()

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

plt.suptitle("Comparaison des méthodes AR et CSS_U selon la fiabilité (WS)", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.95])

output_path = os.path.join(output_dir, "taux_reussite_AR_CSS_U_ws.png")
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Graphique enregistré dans : {output_path}")
