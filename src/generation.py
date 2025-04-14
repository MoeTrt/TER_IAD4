import random

def vectorization(extension, all_args):
    """
    Transforme une extension (liste d'arguments acceptés) en vecteur binaire.
    Les arguments dans l'extension sont mappés à 1, les autres à -1.
    """
    return {arg: 1 if arg in extension else -1 for arg in all_args}

def uniformes_genertation_votes(vec_verite, n_votants, fiabilite):
    """
    Génère des votes binaires avec fiabilité uniforme pour chaque votant.
    Chaque votant respecte la même fiabilité.
    """
    arguments = list(vec_verite.keys())
    n_arguments = len(arguments)
    n_correct = round(fiabilite * n_arguments)

    votes = {}
    for i in range(n_votants):
        vote = {}
        shuffled_args = arguments.copy()
        random.shuffle(shuffled_args)
        correct_args = shuffled_args[:n_correct]
        incorrect_args = shuffled_args[n_correct:]

        for arg in correct_args:
            vote[arg] = vec_verite[arg]
        for arg in incorrect_args:
            vote[arg] = -vec_verite[arg]

        sorted_vote = {arg: vote[arg] for arg in sorted(vote.keys())}
        votes[f"v{i+1}"] = sorted_vote

    return votes

def not_uniformes_generation_votes(vec_verite, n_votants, fiabilite):
    """
    Génère des votes binaires avec une fiabilité non uniforme.
    Le nombre total de votes corrects est réparti aléatoirement parmi tous les votes.
    """
    arguments = list(vec_verite.keys())
    n_arguments = len(arguments)

    total_votes = n_votants * n_arguments
    total_correct_votes = round(fiabilite * total_votes)

    # Initialisation
    voters = [f"v{i+1}" for i in range(n_votants)]
    votes = {v: {} for v in voters}

    # Créer toutes les paires (votant, argument)
    positions = [(v, a) for v in voters for a in arguments]
    correct_positions = random.sample(positions, total_correct_votes)

    for v, a in positions:
        if (v, a) in correct_positions:
            votes[v][a] = vec_verite[a]
        else:
            votes[v][a] = -vec_verite[a]

    return votes


def vote_generation(extensions, all_args):
    """
    Gère l'interaction avec l'utilisateur et génère les votes selon le mode choisi :
    - 'uniforme' : chaque votant respecte la même fiabilité
    - 'non_uniforme' : fiabilité répartie globalement (ex. 4 votes corrects sur 16)
    """
    print("\nExtensions disponibles :")
    for i, ext in enumerate(extensions):
        print(f"  [{i}] {ext}")

    choix = int(input("\nChoisissez l'indice de l'extension qui servira de vérité : "))
    verite = vectorization(extensions[choix], all_args)

    mode = input("Choisissez le mode de génération ('uniforme' ou 'non_uniforme') : ").strip().lower()

    if mode == 'uniforme':
        fiabilite = float(input("Entrez la fiabilité souhaitée (entre 0 et 1) : "))
        n_votants = int(input("Entrez le nombre de votants : "))
        votes = uniformes_genertation_votes(verite, n_votants, fiabilite)

    elif mode == 'non_uniforme':
        fiabilite = float(input("Entrez la fiabilité globale souhaitée (entre 0 et 1) : "))
        n_votants = int(input("Entrez le nombre de votants : "))
        votes = not_uniformes_generation_votes(verite, n_votants, fiabilite)

    else:
        raise ValueError("Mode inconnu. Choisissez 'uniforme' ou 'non_uniforme'.")

    print(f"\nVérité choisie : {verite}")
    print(f"\nVotes générés (mode = {mode}, fiabilité = {fiabilite}) :")
    for name, vote in votes.items():
        print(f"  {name} : {vote}")

    return votes, verite
