# MPVRP-CC-Groupe-1
# MPVRP-CC Solver

## Description

Ce projet propose un solveur pour le **Multi-Product Vehicle Routing Problem with Cross-Docking (MPVRP-CC)**.  
Le solveur utilise une approche **constructive gloutonne** pour générer rapidement des solutions réalisables, adaptées à différentes tailles d’instances (small, medium, large).  

Bien que les solutions générées ne soient pas toujours optimales, elles respectent les contraintes principales :  
- Capacité des véhicules  
- Satisfaction de la demande  
- Structure des itinéraires  

Le projet constitue une base pour des améliorations futures, comme l’intégration d’OR-Tools ou l’utilisation de méta-heuristiques pour optimiser la qualité des solutions.


## Contenu du projet

mpvrpcc_solver_large.py   # Script principal du solveur
large/                    # Dossier contenant les instances de grande taille (.dat)
solutions/                # Dossier où les solutions générées seront enregistrées




## Prérequis

- Python 3.x  
- Modules standard : `os`, `time`, `math`, `platform` (aucune installation externe nécessaire)



## Utilisation

1. Placer vos fichiers d’instances `.dat` dans le dossier `large/ ou medium/ ou easy/`.  
2. Exécuter le solveur :

```bash
python mpvrpcc_solver_large.py
```

3. Les solutions seront générées dans le dossier `solutions/` avec le préfixe `Sol_`.


## Format des fichiers d’instances

Chaque fichier `.dat` doit respecter le format suivant :  


G D P S K         # G : garages, D : dépôts, P : produits, S : stations, K : véhicules
...               # Matrice distances des garages (ignorée)
vid cap garage prod   # Véhicules (id, capacité, garage, produit)
id x y               # Dépôts
id x y demand1 demand2 ... demandP   # Stations avec leurs demandes pour chaque produit


## Fonctionnement du solveur

- **Lecture des instances** : le script lit les fichiers `.dat` et extrait les informations sur les véhicules, dépôts et stations.  
- **Construction de la solution** : pour chaque véhicule, le solveur attribue les demandes des stations correspondant au produit transporté, jusqu’à épuisement de la capacité.  
- **Écriture de la solution** : la solution est sauvegardée au format officiel MPVRP-CC, avec métriques et temps d’exécution.  


## Limitations

- Les solutions sont **gloutonnes et non optimales**, surtout pour les grandes instances.  
- Le solveur ne gère pas les changements de produits entre tournées, ce qui limite la flexibilité.  
- Certaines améliorations futures sont possibles :  
  - Intégration d’OR-Tools pour l’optimisation des tournées  
  - Prise en compte des coûts de changement de produit  
  - Utilisation de méta-heuristiques pour améliorer la qualité des solutions  


## Résultats observés

- **Instances small** : solutions instantanées (<0,1 s), toutes les demandes satisfaites, fichiers conformes.  
- **Instances medium** : solutions valides en quelques dixièmes de seconde, stabilité conservée.  
- **Instances large** : solutions valides mais distances parfois élevées, performances temporelles excellentes, solutions dans la moyenne acceptable.  


