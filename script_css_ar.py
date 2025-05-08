import os
import csv
import subprocess

obaf_root_dir = "./benchmark/OBAF/WS"
output_csv = "obaf_results.csv"

measures = ["S", "D", "U"]
aggregations = ["sum", "min", "leximin"]
css_headers = [f"CSS_{m}_{a}" for m in measures for a in aggregations]

# Header complet du fichier global
global_headers = [
    "fichier_apx", "num_arg", "num_ext", "semantique", "methode",
    "fiabilite", "fiabilite_observee", "repetition", "verite",
    "EXT_AR", "NB_EXT_AR"
] + css_headers

# Liste globale des lignes finales
all_rows = []

file_count = 0

for root, dirs, files in os.walk(obaf_root_dir):
    if "info_generation.csv" not in files:
        continue

    info_path = os.path.join(root, "info_generation.csv")
    updated_rows = []

    with open(info_path, newline="") as f:
        reader = csv.DictReader(f)
        original_headers = reader.fieldnames or []
        for row in reader:
            file_count += 1
            apx_path = os.path.join(root, row["fichier_apx"]).replace("\\", "/")
            filename = row["fichier_apx"]

            # Déduction de la sémantique
            if filename.startswith("PR_"):
                semantics = "PR"
            elif filename.startswith("CO_"):
                semantics = "CO"
            else:
                print(f" [{file_count}] {filename} : Sémantique inconnue")
                continue

            print(f"\n[{file_count}] {apx_path} (sem: {semantics})")

            # -------- AR
            print("   ➤ AR en cours...")
            ext_ar = "N/A"
            try:
                result = subprocess.run(
                    ["python", "mainAR.py", "-f", apx_path],
                    capture_output=True, text=True, check=True
                )
                for line in result.stdout.splitlines():
                    if line.startswith("EXT_AR:"):
                        ext_ar = line.split(":", 1)[1].strip()
            except subprocess.CalledProcessError as e:
                print(f"     AR failed: {e}")
                print("   STDERR:\n", e.stderr)

            # -------- CSS
            css_extensions = []
            for m in measures:
                for a in aggregations:
                    print(f"   ➤ CSS {m}-{a}...")
                    try:
                        result = subprocess.run(
                            ["python", "mainCSS.py", "-f", apx_path, "-s", semantics, "-a", a, "-m", m],
                            capture_output=True, text=True, check=True
                        )
                        best_ext = "N/A"
                        for line in result.stdout.splitlines():
                            if "Meilleure extension selon CSS:" in line:
                                best_ext = line.split(":", 1)[-1].strip()
                                break
                        css_extensions.append(best_ext)
                    except subprocess.CalledProcessError as e:
                        print(f"    CSS {m}-{a} failed")
                        css_extensions.append("N/A")

            # -------- Mise à jour ligne actuelle
            row["EXT_AR"] = ext_ar
            for i, css_col in enumerate(css_headers):
                row[css_col] = css_extensions[i]

            updated_rows.append(row)

            # On ajoute à la liste globale (pour obaf_results.csv)
            all_rows.append([
                row["fichier_apx"], row["num_arg"], row["num_ext"], semantics, row["methode"],
                row["fiabilite"], row["fiabilite_observee"], row["repetition"], row["verite"],
                ext_ar
            ] + css_extensions)

    # ---------- Réécriture de info_generation.csv enrichi
    print(f" Mise à jour : {info_path}")
    updated_headers = original_headers.copy()
    for new_col in ["EXT_AR"] + css_headers:
        if new_col not in updated_headers:
            updated_headers.append(new_col)

    with open(info_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=updated_headers)
        writer.writeheader()
        writer.writerows(updated_rows)

# ---------- Écriture finale du CSV global
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(global_headers)
    writer.writerows(all_rows)

print(f"\n Fichier global généré : {output_csv}")
