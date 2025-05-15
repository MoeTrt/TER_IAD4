import pandas as pd
import matplotlib.pyplot as plt
import os
import ast

df = pd.read_csv("test_results_WS.csv")

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

# Dictionnaire des méthodes à tracer
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

plt.figure(figsize=(10, 6))

for label, col in methods.items():
    match_col = f"match_{label}"
    df[match_col] = df.apply(lambda row: compare_extensions(row[col], row["verite"]), axis=1)
    grouped = df.groupby("fiabilite")[match_col].mean().reset_index()
    grouped["Taux de réussite (%)"] = grouped[match_col] * 100
    print(f"Trace: {label} ({col}) - {grouped.shape[0]} points")

    plt.plot(grouped["fiabilite"], grouped["Taux de réussite (%)"], marker='o', linewidth=1.5, label=label)

plt.xlabel("Fiabilité")
plt.ylabel("Taux de réussite (%)")
plt.title("Comparaison des méthodes (AR & CSS) selon la fiabilité")
plt.grid(True)
plt.legend()
plt.tight_layout()

output_path = os.path.join(output_dir, "taux_reussite_par_fiabilite.png")
plt.savefig(output_path, dpi=300)
plt.close()

print(f" Graphique enregistré dans : {output_path}")
