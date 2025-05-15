import csv

# Évite l'erreur liée à la taille des champs
csv.field_size_limit(10_000_000)

# Fichiers source avec leurs labels
files = [
    ("obaf_results_BA.csv", "BA"),
    ("obaf_results_WS.csv", "WS")
]

output_file = "results.csv"

with open(output_file, "w", newline="") as out_csv:
    writer = None
    header_written = False

    for file_path, source_label in files:
        with open(file_path, newline="") as src_csv:
            reader = csv.reader(src_csv)
            header = next(reader)

            # Écrit l'en-tête une seule fois, avec "source" en premier
            if not header_written:
                writer = csv.writer(out_csv)
                writer.writerow(["source"] + header)
                header_written = True

            # Ajoute la source en début de chaque ligne
            for row in reader:
                writer.writerow([source_label] + row)

print(f"✅ Fichier fusionné généré : {output_file}")
