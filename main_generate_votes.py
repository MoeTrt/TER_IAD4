import os
import csv
import random
import pygarg.dung.apx_parser
from pygarg.dung.solver import extension_enumeration
from src.generation import vote_generation

input_dir = "./benchmark/AF/WS"
output_dir = "./benchmark/OBAF/WS"

semantics_list = ["PR", "CO"]
fiabilites = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
modes = ["uniforme", "non_uniforme"]
n_votants = 5
n_repetitions = 5

for filename in os.listdir(input_dir):
    if not filename.endswith(".apx"):
        continue

    graph_path = os.path.join(input_dir, filename)
    graph_name = os.path.splitext(filename)[0]

    try:
        args, attacks = pygarg.dung.apx_parser.parse(graph_path)
    except Exception as e:
        print(f"Erreur fichier {filename} : {e}")
        continue

    output_graph_dir = os.path.join(output_dir, graph_name)
    os.makedirs(output_graph_dir, exist_ok=True)

    info_csv_path = os.path.join(output_graph_dir, "info_generation.csv")
    with open(info_csv_path, "w", newline="") as info_file:
        info_writer = csv.writer(info_file)
        info_writer.writerow([
            "fichier_af", "fichier_apx", "num_arg", "num_ext", "semantique", "methode", 
            "fiabilite", "fiabilite_observee", "repetition", "verite"
        ])

        for semantics in semantics_list:
            try:
                extensions = extension_enumeration(args, attacks, semantics)
            except Exception as e:
                print(f"Erreur extensions {filename} / {semantics} : {e}")
                continue

            if not extensions:
                print(f"Pas d'extension pour {filename} avec {semantics}")
                continue

            for mode in modes:
                for fiab in fiabilites:
                    for rep in range(1, n_repetitions + 1):
                        votes, verite_ext, fiab_obs = vote_generation(
                            extensions, args, mode, fiab, n_votants
                        )

                        apx_name = f"{semantics}_{mode}_{fiab:.1f}_rep{rep}.apx"
                        apx_path = os.path.join(output_graph_dir, apx_name)

                        with open(apx_path, "w") as apx_file:
                            
                            for arg in args:
                                apx_file.write(f"arg({arg}).\n")
                                
                            for att in attacks:
                                apx_file.write(f"att({att[0]},{att[1]}).\n")

                            for vote in votes.values():
                                line = "vote(" + ",".join(str(vote[arg]) for arg in args) + ").\n"
                                apx_file.write(line)

                        info_writer.writerow([
                            filename, apx_name, len(args), len(extensions), semantics, mode, fiab, fiab_obs, rep, verite_ext
                        ])

    print(f" Générations terminées pour {graph_name}")