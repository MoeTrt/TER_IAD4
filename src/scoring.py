def V_ec(extensions, all_arguments):
    """
    Retourne un dictionnaire contenant les vecteurs V_ec(E) pour plusieurs extensions.
    extensions: Liste de tuples contenant les extensions sous forme d'ensembles d'arguments.
    all_arguments: Liste de tous les arguments du cadre argumentatif.
    return: Dictionnaire {extension: {argument: 1 ou -1}}
    """
    vec_dict = {}

    for extension in extensions:
        vec = {}  
        for arg in all_arguments:
            if arg in extension:
                vec[arg] = 1  
            else:
                vec[arg] = -1  
        vec_dict[extension] = vec
    
    return vec_dict

def cal_satisfaction(votes,extensions):
    """ Calcul la satisfaction d'un votant pour une extension """
    return ()