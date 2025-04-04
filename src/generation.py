import random

def vectorization(extension, all_args):
    """
    Transforme une extension (liste d'arguments acceptés) en vecteur binaire.
    Les arguments dans l'extension sont mappés à 1, les autres à -1.
    """
    return {arg: 1 if arg in extension else -1 for arg in all_args}


def uniformes_genertation_votes(vec_verite, n_votants, fiabilite):
    """
    Génère des votes binaires (1 ou -1) avec une fiabilité uniforme.
    Retourne un dictionnaire : {v1: {...}, v2: {...}, ...}
    """
    print(vec_verite)
    arguments = list(vec_verite.keys()) # Liste des clés (arguments) à partir du vecteur de vérité (tq : {'a': 1, 'b': -1, 'c': -1, 'd': 1})
    n_arguments = len(arguments) # Nombre total d'arguments
    n_correct = round(fiabilite * n_arguments) # Nombre d'arguments qui devront être en accord avec la vérité, le reste en désaccord
    print(f"Nombre d'arguments : {n_arguments}, Nombre d'arguments corrects par votants : {n_correct}")

    votes = {}

    for i in range(n_votants):
        vote = {}
        #print("passage grande boucle")
        shuffled_args = arguments.copy()
        random.shuffle(shuffled_args)
        correct_args = shuffled_args[:n_correct]
        incorrect_args = shuffled_args[n_correct:]

        for arg in correct_args:
            #print("vote arg", vec_verite[arg], arg)
            vote[arg] = vec_verite[arg]
        for arg in incorrect_args:
            vote[arg] = -vec_verite[arg]

        sorted_vote = {arg: vote[arg] for arg in sorted(vote.keys())}
        votes[f"v{i+1}"] = sorted_vote

    return votes


def vote_generation(extensions, all_args):
    """
    Demande à l'utilisateur de choisir une extension comme vérité et une fiabilité,
    puis génère les votes correspondants sous forme {v1: {...}, v2: {...}, ...}
    """
    print("\nExtensions calculées :")
    for i, ext in enumerate(extensions):
        print(f"  [{i}] {ext}")

    choix = int(input("\nChoisissez l'indice de l'extension qui servira de vérité : "))
    fiabilite = float(input("Entrez la fiabilité souhaitée (entre 0 et 1) : "))
    n_votants = int(input("Entrez le nombre de votants à générer : "))

    verite = vectorization(extensions[choix], all_args)
    votes = uniformes_genertation_votes(verite, n_votants, fiabilite)

    print(f"\nVérité choisie (vecteur) : {verite}")
    print(f"\nVotes générés (fiabilité = {fiabilite}) :")
    for name, vote in votes.items():
        print(f"  {name} : {vote}")

    return votes, verite