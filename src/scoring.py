def compute_satisfaction(vote, vecE):
    """
    Calcule la satisfaction S_v(E) d'un votant par rapport à une extension.
    :param vote: Dictionnaire des votes {argument: -1, 0 ou 1}.
    :param vecE: Vecteur V_ec(E) de l'extension {argument: 1 ou -1}.
    :return: Score de satisfaction.
    """
    satisfaction = 0
    for arg, vote_value in vote.items():
        if vote_value == vecE[arg]:
            satisfaction += 1
    return satisfaction

def compute_dissatisfaction(vote, vecE):
    """
    Calcule la dissatisfactio   n D_v(E) d'un votant par rapport à une extension.
    :param vote: Dictionnaire des votes {argument: -1, 0 ou 1}.
    :param vecE: Vecteur V_ec(E) de l'extension {argument: 1 ou -1}.
    :return: Score de dissatisfaction (négatif).
    """
    dissatisfaction = 0
    for arg, vote_value in vote.items():
        if vote_value == -vecE[arg]:
            dissatisfaction -= 1
    return dissatisfaction


def compute_utility(vote, vecE):
    """
    Calcule l'utilité U_v(E) d'un votant par rapport à une extension.
    :param vote: Dictionnaire des votes {argument: -1, 0 ou 1}.
    :param vecE: Vecteur V_ec(E) de l'extension {argument: 1 ou -1}.
    :return: Score d'utilité (satisfaction + dissatisfaction).
    """
    return compute_satisfaction(vote, vecE) + compute_dissatisfaction(vote, vecE)

def leximin_sort(scores):
    """
    Trie une liste de scores selon le critère Leximin.
    :param scores: Liste de listes représentant les scores des extensions.
    :return: Liste triée selon Leximin.
    """
    print("score entrée : " , scores)
    test = sorted(scores, key=lambda x: tuple(x if isinstance(x, (list, tuple)) else [x]))
    print("score sortie leximin : " , test)
    return test # Conversion temporaire

def compute_distance(votes, vecE, aggregation, metric):
    """
    Calcule la distance d'une extension aux votes selon une méthode d'agrégation et un type de score.
    :param votes: Dictionnaire des votes de chaque votant {votant: {argument: vote}}.
    :param vecE: Vecteur de l'extension {argument: 1 ou -1}.
    :param aggregation: Méthode d'agrégation ('sum', 'min', 'leximin').
    :param metric: Type de score ('S' pour satisfaction, 'D' pour dissatisfaction, 'U' pour utility).
    :return: Distance calculée.
    """
    scores = []
    
    for vote in votes.values():
        if metric == 'S':
            score = compute_satisfaction(vote, vecE)
        elif metric == 'D':
            score = compute_dissatisfaction(vote, vecE)
        elif metric == 'U':
            score = compute_utility(vote, vecE)
        else:
            raise ValueError("Métrique inconnue. Choisir 'S', 'D' ou 'U'.")
        
        scores.append(score)
    
    if aggregation == 'sum':
        return sum(scores)
    elif aggregation == 'min':
        return min(scores)
    elif aggregation == 'leximin':
        return leximin_sort(scores)
    else:
        raise ValueError("Méthode d'agrégation inconnue. Choisir 'sum', 'min' ou 'leximin'.")


def compute_CSS(votes, extensions, all_arguments, aggregation, metric):
    """
    Calcule le CSS en trouvant l'extension qui maximise la distance.
    :param votes: Dictionnaire des votes {votant: {argument: vote}}.
    :param extensions: Liste des extensions possibles.
    :param all_arguments: Liste de tous les arguments.
    :param aggregation: Méthode d'agrégation ('sum', 'min', 'leximin').
    :param metric: Type de score ('S', 'D', 'U').
    :return: Liste des extensions maximisant la distance et la distance maximale.
    """
    best_extensions = []
    best_distance = None
    
    for extension in extensions:
        vecE = {arg: 1 if arg in extension else -1 for arg in all_arguments} # Vectorisation en fonction des arguments de l'AF en fonction de l'extension choisie
        distance = compute_distance(votes, vecE, aggregation, metric)
        print(distance,extension)
        
        if best_distance is None or distance > best_distance:
            best_distance = distance
            best_extensions = [extension]
        elif distance == best_distance:
            best_extensions.append(extension)
    
    return best_extensions, best_distance