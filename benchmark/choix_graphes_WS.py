import os
import re
import csv
from collections import defaultdict
import pygarg.dung.apx_parser
from pygarg.dung.solver import extension_enumeration

# 📁 Dossier contenant les fichiers .apx
folder_path = "./graph/WS"

# ⚙️ Paramètres
semantics = "PR"
target_total = 42
target_per_category = 14
categories = ["10", "20", "30"]
max_per_pbCycle = 2  # ← Limite pour éviter trop de doublons par proba

# Tous les fichiers valides organisés
valid_files_by_cat_and_pb = defaultdict(lambda: defaultdict(list))
all_valid_files = []

# Lecture des fichiers .apx
for filename in os.listdir(folder_path):
    if not filename.endswith(".apx"):
        continue

    # Extrait numArg et pbCycle depuis le nom du fichier
    match = re.search(r'numArg(\d+)-pbCycle([\d.]+)', filename)
    if not match:
        continue

    numArg = match.group(1)
    pbCycle = match.group(2)
    full_path = os.path.join(folder_path, filename)

    try:
        arguments, attacks = pygarg.dung.apx_parser.parse(full_path)
        extensions = extension_enumeration(arguments, attacks, semantics)
    except Exception as e:
        print(f"Erreur fichier {filename} : {e}")
        continue

    if len(extensions) < 2:
        continue

    valid_files_by_cat_and_pb[numArg][pbCycle].append((filename, numArg, pbCycle, len(extensions)))
    all_valid_files.append((filename, numArg, pbCycle, len(extensions)))

# Sélection équilibrée par catégorie
selected = []
used_files = set()

for cat in categories:
    cat_selected = []
    pb_map = valid_files_by_cat_and_pb.get(cat, {})

    # 1. Prendre au max `max_per_pbCycle` par pbCycle
    for pb, files in pb_map.items():
        for f in files[:max_per_pbCycle]:
            if len(cat_selected) < target_per_category:
                cat_selected.append(f)
                used_files.add(f[0])

    # 2. Compléter si on n'en a pas encore 14
    if len(cat_selected) < target_per_category:
        additional = [
            f for pb in pb_map for f in pb_map[pb]
            if f[0] not in used_files
        ]
        cat_selected.extend(additional[:target_per_category - len(cat_selected)])
        used_files.update(f[0] for f in cat_selected)

    selected.extend(cat_selected)

# Compléter le total s’il manque
if len(selected) < target_total:
    remaining = target_total - len(selected)
    leftovers = [f for f in all_valid_files if f[0] not in used_files]
    selected.extend(leftovers[:remaining])

#  Résumé
print(f"\n Fichiers sélectionnés : {len(selected)}")
for cat in categories:
    count = sum(1 for f in selected if f[1] == cat)
    print(f"   - numArg{cat} : {count} fichiers")

# Sauvegarde CSV
with open("fichiers_equilibres_diversifies.csv", "w", newline="") as f_csv:
    writer = csv.writer(f_csv)
    writer.writerow(["filename", "numArgs", "pbCycle", "num_extensions"])
    for filename, cat, pb, ext in selected:
        writer.writerow([filename, cat, pb, ext])

