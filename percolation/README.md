# Percolation

Ce dépôt contient un notebook jupyter dans lequel on réalise une analyse du seuil de percolation. L'expérience consiste à étudier le seuil de densité initiale de forêt à partir duquel on peut observer un basculement dans la propagation du feu. Voici une simulation avec deux foyers.

![Alt Text](https://github.com/Younzer/Projets-applicatifs/blob/master/percolation/percolation.gif)

### Concernant le code
Afin de ne pas avoir à gérer les points au bord de la map, nous utilisons la fonction **pad** de ***Numpy*** et effectuons la propagation sur l'ensemble de cette map, ce qui nous évite de nous encombrer de conditions lourdes. Ensuite, nous utilisons la fonction **unpad** qui permet de retrouver une map avec la taille d'origine, c'est-à-dire avant padding.

### Résultats
Nous déterminé ce seuil en laissant la possibilité de faire démarrer à plusieurs endroits le feu, et en considérant différentes tailles de forêt. Nous pouvons observer (cf. Fig. 1) que faire varier le nombre de foyers semble faire se décaler la courbe :
* vers la droite si on augmente le nombre de foyers, 
* ou vers la gauche si on le diminue
![Logo](https://github.com/Younzer/Projets-applicatifs/blob/master/percolation/seuil_foyers.png "Title")
|(Fig. 1)|
