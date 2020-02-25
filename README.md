# Projets-applicatifs
Ce répertoire contient les 3 projets applicatifs à faire et à rendre à notre professeur M. Laurent Simon.

# Percolation

Le dossier percolation contient un notebook jupyter dans lequel on réalise une analyse du **seuil de percolation**. L'expérience consiste à étudier le seuil de densité initiale de forêt à partir duquel on peut observer un basculement dans la propagation du feu. Voici une simulation avec deux foyers :

![Alt Text](https://github.com/Younzer/Projets-applicatifs/blob/master/percolation/percolation.gif)

### Concernant le code
Afin de ne pas avoir à gérer les points au bord de la map, nous utilisons la fonction **pad** de ***Numpy*** et effectuons la propagation sur l'ensemble de cette map, ce qui nous évite de nous encombrer de conditions lourdes. Ensuite, nous utilisons la fonction **unpad** qui permet de retrouver une map avec la taille d'origine, c'est-à-dire avant padding.

On calcule pour chaque pourcentage de densité initiale (1% puis 2%, 3%, etc jusqu'à 100%) la moyenne du ratio densité finale / densité initiale, et ce sur ***500 itérations***. 

### Résultats
Nous avons déterminé ce seuil en laissant la possibilité de faire démarrer à plusieurs endroits le feu, et en considérant différentes tailles de forêt. Nous pouvons observer (cf. Fig. 1) que faire varier le nombre de foyers semble faire se décaler la courbe :
* vers la gauche si on augmente le nombre de foyers, 
* ou vers la droite si on le diminue

![Logo](https://github.com/Younzer/Projets-applicatifs/blob/master/percolation/seuil_foyers.png "Seuil en fonction du nombre de foyers")
<div align="center">Figure 1</div>

<br />
Faire varier la taille de la forêt permet de déterminer plus précisément le seuil de percolation. Ce dernier se trouve à l'intersection des courbes correspondant aux différentes tailles de forêt (cf. Fig 2). Nous pouvons observer que plus la taille de la forêt est importante, moins la courbe est lissée, et donc plus la pente qui caractérise le basculement est marquée. Cela semble logique car elle est moins sensible aux événements rares comme par exemple quand une forêt de petite densité prend quasiment entièrement feu, ou à l'inverse quand une forêt de grande densité est grandement épargnée. 

**Remarque :** Dans le graphe qui suit, nous avons simulé la propagation à partir d'un seul foyer.

![Logo](https://github.com/Younzer/Projets-applicatifs/blob/master/percolation/seuil_surface.png "Seuil en fonction de la superficie")
<div align="center">Figure 2</div>


### Conclusion
En conclusion de notre expérience, nous pouvons donc dire que le seuil varie si on fait varier le nombre de foyers (il diminue si on augmente le nombre de foyers et inversement), et qu'il est ***approximativement de 60%*** si on considère qu'il n'y a qu'un seul foyer au départ du feu.


# Pysat Sudoku

Pour ce projet applicatif, l'objectif était d'utiliser le solver Pysat afin de générer des grilles de Sudoku n'ayant qu'une seule solution possible.

### Code

##### Génération de grilles aléatoires

Nous avons d'abord fait en sorte de pouvoir créer à chaque fois des **grilles différentes**. Le point d'entrée est le suivant : 
![Logo](https://github.com/Younzer/Projets-applicatifs/blob/master/sudoku/images/entree.png "Point d'entrée")
<br />
Nous faisons appel à la fonction qui suit :
![Logo](https://github.com/Younzer/Projets-applicatifs/blob/master/sudoku/images/generate_random_grid.png "Génération de grille aléatoire")
<br />
<br />
La méthode est la suivante :
* Nous imposons au Solver de résoudre le Sudoku avec une liste d'indices déjà fixés, et ce aléatoirement.
* Si le Sudoku n'est pas solvable avec ces indices, par exemple s'il y a une contradiction avec deux "1" fixés préalablement dans une même ligne ou une même colonne ou encore un des 9 carrés regroupant 9 chiffres différents, alors on recommence et ce jusqu'à ce que le Sudoku ait une solution possible.

La liste d'indices est créée avec la fonction qui suit :
![Logo](https://github.com/Younzer/Projets-applicatifs/blob/master/sudoku/images/generateFixedHints.png "Génération d'indices aléatoires")
<br />
<br />
Dans l'appel à cette fonction, nous gérons immédiatement le fait que deux indices puissent être fixés sur une même case de la grille. La fonction qui suit permet de garder seulement le premier de ces indices :
![Logo](https://github.com/Younzer/Projets-applicatifs/blob/master/sudoku/images/remove_contradictions.png "Un seul indice par case")
<br />
<br />

##### Grille avec un minimum d'indices et une seule solution

Nous avons donc une grille **aléatoire** dont le solver a pu trouver **une** solution à partir des contraintes fixées. L'objectif est d'enlever des chiffres de cette grille pour qu'elle ne soit plus résolue mais à résoudre, tout en s'assurant qu'elle n'ait qu'**une seule solution possible**. C'est ce que nous faisons avec le bout de code qui suit :

![Logo](https://github.com/Younzer/Projets-applicatifs/blob/master/sudoku/images/get_sol.png "Génèration d'une grille à une seule solution")
<br />
<br />

Voici les étapes que nous suivons :
* Nous avons créé un attribut "_hints" qui au départ prend l'ensemble de la solution de la grille
* On créer la négation de cette solution
* Puis on répète ces étapes jusqu'à obtenir une nouvelle solution possible :
 * On enlève un indice "*_hints*" de manière aléatoire
 * On créer un nouveau solver auquel on ajoute les clauses interdisant d'obetnir la même solution
 * On ajoute les indices restants
 * On vérifie s'il y a une nouvelle solution possible, si non, on recommence.
 * Si on a une seconde solution possible, alors on rajoute le dernier indice enlevé de sorte à avoir une seule solution possible
 
Voici les fonctions que nous utilisons pour gérer les indices de l'instance solver :
![Logo](https://github.com/Younzer/Projets-applicatifs/blob/master/sudoku/images/fonctions.png "Fonctions ajoutées à la classe")
<br />
<br />

Voici ce que nous obtenons en sortie : la liste d'indices qui permet d'avoir une seule solution et la solution correspondante :
![Logo](https://github.com/Younzer/Projets-applicatifs/blob/master/sudoku/images/list_hints.png "Indices et solution")


### Ouverture

Il aurait été intéressant de pouvoir générer des grilles de différentes difficultés. On aurait pu considérer par exemple que moins il y a d'indices pour résoudre la grille et plus elle est difficile à rédoudre. Une solution pour générer des grilles de trois difficultés différentes serait alors la suivante :
* Pour une *grille facile*, on utiliserait une fonction qui cherche systématiquement s'il y a un indice "décisif" qui une fois retirés permettrait d'avoir plusieurs solutions possibles.
* Pour une *grille moyenne*, nous utiliserions la solution que nous utilisons déjà en retirant à chaque fois un indice de manière aléatoire.
* Pour une *grille difficile*, on chercherait parmis les indices restants s'il y en a un qui ne soit pas décisif, s'il y en a plusieurs on choisit de manière aléatoire à défault d'avoir une meilleure manière de choisir.
<br />
Bien sûr, cette solution peut être largement améliorée, et elle ne pourrait pas nous assurer d'avoir des grilles de niveaux bienx différents, surtout à cause du choix aléatoire d'indice à enlever, mais c'est une première approche qui peut être intéressant de tester.

