import pandas as pd
import matplotlib.pyplot as plt
import os
import ast

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


# df["num_arg"] = pd.to_numeric(df["num_arg"], errors="coerce")

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

# par arguments
# plt.figure(figsize=(10, 6))

# for label, col in methods.items():
#     match_col = f"match_{label}"
#     df[match_col] = df.apply(lambda row: compare_extensions(row[col], row["verite"]), axis=1)
#     grouped = df.groupby("num_arg")[match_col].mean().reset_index()
#     grouped["Taux de réussite (%)"] = grouped[match_col] * 100
#     print(f"Trace: {label} ({col}) - {grouped.shape[0]} points")

#     plt.plot(grouped["num_arg"], grouped["Taux de réussite (%)"], marker='o', linewidth=1.5, label=label)

# plt.xlabel("Nombre d'arguments")
# plt.ylabel("Taux de réussite (%)")
# plt.title("Comparaison des méthodes (AR & CSS) selon le nombre d'arguments")
# plt.grid(True)
# plt.legend()
# plt.tight_layout()

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
