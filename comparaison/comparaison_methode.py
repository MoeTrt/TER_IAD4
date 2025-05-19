import pandas as pd
import matplotlib.pyplot as plt
import os
import ast

df = pd.read_csv("obaf_results_BA.csv")
output_dir = "figures/BA"
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

# Groupes de méthodes à afficher
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

# Configuration des deux sous-graphiques : uniforme vs non uniforme
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
methode_list = ["uniforme", "non_uniforme"]
titles = ["Votes Uniformes", "Votes Non-Uniformes"]

for idx, methode in enumerate(methode_list):
    ax = axes[idx]
    sub_df = df[df["methode"] == methode]

    for group_label, method_list in method_groups.items():
        for label in method_list:
            col = methods[label]
            match_col = f"match_{label}"
            sub_df[match_col] = sub_df.apply(lambda row: compare_extensions(row[col], row["verite"]), axis=1)
            grouped = sub_df.groupby("fiabilite")[match_col].mean().reset_index()
            grouped["Taux de réussite (%)"] = grouped[match_col] * 100

            ax.plot(grouped["fiabilite"], grouped["Taux de réussite (%)"],
                    marker='o', linewidth=1.5, label=label, color=custom_colors[label])

    ax.set_title(titles[idx])
    ax.set_xlabel("Fiabilité")
    if idx == 0:
        ax.set_ylabel("Taux de réussite (%)")
    ax.grid(True)
    ax.legend()

plt.suptitle("Comparaison des groupes de méthodes selon la fiabilité - Méthodes de vote (BA)", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])

output_path = os.path.join(output_dir, "taux_reussite_uniforme_vs_non_uniforme_ba.png")
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Graphique enregistré dans : {output_path}")
