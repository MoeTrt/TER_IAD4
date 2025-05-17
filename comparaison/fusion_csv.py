import csv

# Évite l'erreur liée à la taille des champs
csv.field_size_limit(10_000_000)

files = [
    ("obaf_results_BA.csv", "BA"),
    ("obaf_results_WS.csv", "WS")
]

output_file = "obaf_results.csv"

with open(output_file, "w", newline="") as out_csv:
    writer = None
    header_written = False

    for file_path, source_label in files:
        with open(file_path, newline="") as src_csv:
            reader = csv.reader(src_csv)
            header = next(reader)

            # Écrit l'en-tête une seule fois, avec "type" en premier
            if not header_written:
                writer = csv.writer(out_csv)
                writer.writerow(["type"] + header)
                header_written = True

            # Ajoute le type en début de chaque ligne
            for row in reader:
                writer.writerow([source_label] + row)

print(f" Fichier fusionné généré : {output_file}")
