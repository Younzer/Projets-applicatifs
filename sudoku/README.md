# Pysat Sudoku

Pour ce projet applicatif, l'objectif était d'utiliser le solver Pysat afin de générer des grilles de Sudoku n'ayant qu'une seule solution possible.

### Code

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
![Logo](![Logo](https://github.com/Younzer/Projets-applicatifs/blob/master/sudoku/images/generateFixedHints.png "Génération d'indices aléatoires") "Un seul indice par case")
<br />
<br />

### Sortie
