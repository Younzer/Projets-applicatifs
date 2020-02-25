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
* 

### Ouverture

Il aurait été intéressant de pouvoir générer des grilles de différentes difficultés. On aurait pu considérer par exemple que moins il y a d'indices pour résoudre la grille et plus elle est difficile à rédoudre. Une solution pour générer des grilles de trois difficultés différentes serait alors la suivante :
* Pour une *grille facile*, on utiliserait une fonction qui cherche systématiquement s'il y a un indice "décisif" qui une fois retirés permettrait d'avoir plusieurs solutions possibles.
* Pour une *grille moyenne*, nous utiliserions la solution que nous utilisons déjà en retirant à chaque fois un indice de manière aléatoire.
* Pour une *grille difficile*, on chercherait parmis les indices restants s'il y en a un qui ne soit pas décisif, s'il y en a plusieurs on choisit de manière aléatoire à défault d'avoir une meilleure manière de choisir.
<br />
Bien sûr, cette solution peut être largement améliorée, et elle ne pourrait pas nous assurer d'avoir des grilles de niveaux bienx différents, surtout à cause du choix aléatoire d'indice à enlever, mais c'est une première approche qui peut être intéressant de tester.
