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
        if isinstance(parsed, list):
            if len(parsed) > 0 and isinstance(parsed[0], list):
                parsed = parsed[0]
            return sorted([str(arg).strip() for arg in parsed])
    except:
        pass
    return []

def compare_extensions(ext1, ext2):
    return normalize_extension(ext1) == normalize_extension(ext2)

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
    
    grouped = df.groupby("semantique")[f"match_{method_label}"].mean().reset_index()
    for _, row in grouped.iterrows():
        results.append({
            "Méthode": method_label,
            "Sémantique": row["semantique"],
            "Taux de réussite (%)": row[f"match_{method_label}"] * 100
        })

bar_df = pd.DataFrame(results)

plt.figure(figsize=(12, 6))
colors = {"PR": "#1f77b4", "CO": "#ff7f0e"}

for i, semantic in enumerate(bar_df["Sémantique"].unique()):
    subset = bar_df[bar_df["Sémantique"] == semantic]
    plt.bar([x + i * 0.35 for x in range(len(subset))],
            subset["Taux de réussite (%)"],
            width=0.35,
            label=semantic,
            color=colors[semantic])

plt.xticks([x + 0.175 for x in range(len(subset))], subset["Méthode"], rotation=45)
plt.ylabel("Taux de réussite (%)")
plt.title("Comparaison des taux de réussite par méthode selon la sémantique (PR vs CO)")
plt.legend()
plt.tight_layout()

output_path = os.path.join(output_dir, "taux_reussite_par_semantique.png")
plt.savefig(output_path, dpi=300)
plt.close()

print(f" Graphique enregistré dans : {output_path}")
