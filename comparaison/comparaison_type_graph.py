import pandas as pd
import matplotlib.pyplot as plt
import ast
import os

df = pd.read_csv("obaf_results.csv") 

output_dir = "figures"
os.makedirs(output_dir, exist_ok=True)

def normalize_extension(ext):
    try:
        parsed = ast.literal_eval(ext.strip())

        # Si c'est une seule extension [a, b], on la met dans une liste [[a, b]]
        if isinstance(parsed, list):
            if len(parsed) > 0 and isinstance(parsed[0], list):
                # Plusieurs extensions
                return [sorted([str(arg).strip() for arg in sub]) for sub in parsed]
            else:
                # Une seule extension
                return [sorted([str(arg).strip() for arg in parsed])]
    except:
        pass
    return []

def compare_extensions(returned_exts, true_ext):
    normalized_returned = normalize_extension(returned_exts)
    normalized_truth = normalize_extension(true_ext)

    # On compare avec la première vérité seulement (on suppose une seule vérité)
    return normalized_truth[0] in normalized_returned if normalized_truth else False


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

results = []

for method_label, col in methods.items():
    if col not in df.columns:
        continue
    df[f"match_{method_label}"] = df.apply(lambda row: compare_extensions(row[col], row["verite"]), axis=1)
    
    grouped = df.groupby("type")[f"match_{method_label}"].mean().reset_index()
    for _, row in grouped.iterrows():
        results.append({
            "Méthode": method_label,
            "Type": row["type"],
            "Taux de réussite (%)": row[f"match_{method_label}"] * 100
        })

bar_df = pd.DataFrame(results)

plt.figure(figsize=(12, 6))
colors = {"BA": "#2ca02c", "WS": "#d62728"}

for i, t in enumerate(bar_df["Type"].unique()):
    subset = bar_df[bar_df["Type"] == t]
    plt.bar([x + i * 0.35 for x in range(len(subset))],
            subset["Taux de réussite (%)"],
            width=0.35,
            label=t,
            color=colors[t])

plt.xticks([x + 0.175 for x in range(len(subset))], subset["Méthode"], rotation=45)
plt.ylabel("Taux de réussite (%)")
plt.title("Comparaison des taux de réussite par méthode selon le type de graphe (BA vs WS)")
plt.legend()
plt.tight_layout()

output_path = os.path.join(output_dir, "taux_reussite_par_type_graph.png")
plt.savefig(output_path, dpi=300)
plt.close()

print(f" Graphique enregistré dans : {output_path}")
