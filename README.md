# Argumentation Collective - CSS et COSAR

Ce projet s’inscrit dans le cadre d’une recherche expérimentale sur l’argumentation collective.  
Il vise à explorer et comparer différentes sémantiques d’agrégation d’opinions dans des graphes d’argumentation, en particulier **CSS** (Collective Semantics via Scoring) et **COSAR** (Collective Semantics via Argument Ranking).

Les expériences sont menées sur des graphes générés artificiellement, enrichis d’opinions individuelles, pour évaluer la capacité de chaque approche à retrouver une "vérité" de référence.

## Contenu des dossiers

- `apx_files/` : Fichiers `.apx` pour représenter les graphes d'argumentation.
- `benchmark/` :
  - `AF/` : Graphes sans opinions (argumentation abstraite).
  - `OBAF/` : Graphes avec opinions d’agents (Barabási–Albert et Watts–Strogatz).
- `comparaison/figures/` : Résultats et visualisations des expériences (figures pour BA et WS).
- `docs/article/` : Sources
- `src/` : Code source Python (implémentation de CSS, COSAR, métriques, parsing, generation de votes.).

### Lancer les scritps principaux

- `python mainCSS.py -f <fichier_obaf.apx> -s <CO|PR> -a <sum|min|leximin> -m <S|D|U>` : Exécute CSS sur un OBAF
- `python mainAR.py -f <fichier.apx>` : Exécute COSAR sur un OBAF

- `python script_css_ar.py` : Exécute CSS et COSAR sur le benchmark

Auteurs : Alix TIEO, Dounia HOUADRIA, Moe TRIQUET
