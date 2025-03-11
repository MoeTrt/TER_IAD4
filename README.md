AD 4 : Évaluation de la Recherche de Vérité des Méthodes d’Agrégation d’Opinions en Argumentation

Encadré par : Jérôme DELOBELLE, jerome.delobelle@u-paris.fr

L’identification de la « vérité » est au cœur des applications pratiques des méthodes de délibération, en particulier sur les plateformes de délibération citoyenne. Ces plateformes traitent souvent de questions épistémiques, où la découverte de la vérité est essentielle. Évaluer la capacité des cadres de vote à identifier cette vérité est une condition préalable à leur utilisation efficace.
Bien que certains débats portent sur des questions sociétales ou éthiques subjectives (par exemple, la réglementation des armes à feu ou le droit à l’avortement), le travail qui nous intéresse se concentre sur des méthodes spécifiquement conçues pour recher- cher la vérité. Cette approche établit un lien entre les avancées théoriques dans les cadres d’argumentation (notamment l’argumentation formelle) et leurs applications concrètes. L’argumentation formelle a pour but de modéliser et raisonner sur des arguments et leurs interactions (e.g. relation d’attaque) avec notamment l’argumentation abstraite [1].
Pour la partie raisonnement, un des objectifs est de déterminer les ensembles d’arguments qui peuvent être conjointement acceptés. Ces ensembles d’arguments sont appelés des exten- sions et sont obtenus par différentes sémantiques (voir [2]). Récemment, une extension du cadre de Dung a été introduit : les systèmes d’argumentation basés sur l’opinion [3]. Ces systèmes permettent à chaque individu de voter pour ou contre les arguments mais aussi de s’abstenir. Plusieurs approches (sémantiques) ont également été introduites ou adaptées afin de prendre en considération les votes (en plus de la relation d’attaque) dans le calcul des extensions.
Ces sémantiques, appelées sémantiques d’opinions collectives, ont ensuite été évalué axiomatiquement par différentes propriétés. Si l’on considère que parmi l’ensemble des extensions, une de ces extensions correspond à la "vérité", il serait intéressant d’analyser la capacité de ces sémantiques à trouver cette vérité en fonction des votes donnés par les différents agents.

Grandes lignes du travail à effectuer :
— Comprendre et étudier certaines sémantiques d’opinions collectives
— Définir formellement le problème de recherche de la vérité étant donné un système d’argumentation et un ensemble de votes
— Implémenter ces approches
— Etablir un protocole expérimental pour tester ces approches
— Analyser, interpréter et comparer les résultats

# TER_IAD4

Projet M1 IAD

Compilation:

python main.py -f path/to/test_af.txt -s <PR|CO>
