import random
import math

def vectorization(extension, all_args):
    """
    Transforme une extension (liste d'arguments acceptés) en vecteur binaire.
    Les arguments dans l'extension sont mappés à 1, les autres à -1.
    """
    return {arg: 1 if arg in extension else -1 for arg in all_args}


def uniformes_generation_votes(vec_verite, n_votants, fiabilite):
    """
    Génère des votes binaires avec fiabilité uniforme pour chaque votant.
    Chaque votant respecte la même fiabilité.
    """
    arguments = list(vec_verite.keys())
    n_arguments = len(arguments)
    
    votes = {}

    if fiabilite == 1.0:
        # Tous les votants votent parfaitement selon la vérité
        for i in range(n_votants):
            vote = {arg: vec_verite[arg] for arg in sorted(arguments)}
            votes[f"v{i+1}"] = vote
        return votes

    # Cas général : fiabilité partielle
    n_correct = math.ceil(fiabilite * n_arguments)

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
    total_votes = n_votants * len(arguments)

    voters = [f"v{i+1}" for i in range(n_votants)]
    votes = {v: {} for v in voters}
    positions = [(v, a) for v in voters for a in arguments]

    total_correct_votes = math.ceil(fiabilite * total_votes)

    if fiabilite == 1.0 :
        for v, a in positions:
            votes[v][a] = vec_verite[a]
    
    else :
        correct_positions = random.sample(positions, total_correct_votes)
        for v, a in positions:
            if (v, a) in correct_positions:
                votes[v][a] = vec_verite[a]
            else:
                votes[v][a] = -vec_verite[a]
    return votes

def calcul_fiabilite(votes, verite):
    """
    Calcule la fiabilité globale des votes :
    proportion de votes (argument par votant) qui sont conformes à la vérité.
    """
    total_votes = 0
    votes_corrects = 0

    for vote in votes.values():
        for arg, val in vote.items():
            if arg in verite:
                total_votes += 1
                if val == verite[arg]:
                    votes_corrects += 1

    if total_votes == 0:
        return 0.0
    return round(votes_corrects / total_votes, 4)

import random

def vote_generation(extensions, all_args, mode, fiabilite, n_votants):
    """
    Génère les votes automatiquement sans interaction utilisateur.
    - Choisit aléatoirement une vérité parmi les extensions.
    - Génère les votes selon le mode et la fiabilité donnés.
    """
    # Choix aléatoire de la vérité
    verite_ext = random.choice(extensions)
    verite = vectorization(verite_ext, all_args)

    # Génération des votes
    if mode == 'uniforme':
        votes = uniformes_generation_votes(verite, n_votants, fiabilite)
    elif mode == 'non_uniforme':
        votes = not_uniformes_generation_votes(verite, n_votants, fiabilite)
    else:
        raise ValueError("Mode inconnu. Choisissez 'uniforme' ou 'non_uniforme'.")

    # Calcul de la fiabilité réelle obtenue
    fiabilite_reelle = calcul_fiabilite(votes, verite)
    # print(fiabilite_reelle)

    return votes, verite_ext, fiabilite_reelle
