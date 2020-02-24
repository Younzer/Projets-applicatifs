# Percolation

Ce dépôt contient un notebook jupyter dans lequel on réalise une analyse du **seuil de percolation**. L'expérience consiste à étudier le seuil de densité initiale de forêt à partir duquel on peut observer un basculement dans la propagation du feu. Voici une simulation avec deux foyers :

![Alt Text](https://github.com/Younzer/Projets-applicatifs/blob/master/percolation/percolation.gif)

### Concernant le code
Afin de ne pas avoir à gérer les points au bord de la map, nous utilisons la fonction **pad** de ***Numpy*** et effectuons la propagation sur l'ensemble de cette map, ce qui nous évite de nous encombrer de conditions lourdes. Ensuite, nous utilisons la fonction **unpad** qui permet de retrouver une map avec la taille d'origine, c'est-à-dire avant padding.

On calcule pour chaque pourcentage de densité initiale (1% puis 2%, 3%, etc jusqu'à 100%) la moyenne du ratio densité finale / densité initiale, et ce sur ***500 itérations***. 

### Résultats
Nous déterminé ce seuil en laissant la possibilité de faire démarrer à plusieurs endroits le feu, et en considérant différentes tailles de forêt. Nous pouvons observer (cf. Fig. 1) que faire varier le nombre de foyers semble faire se décaler la courbe :
* vers la droite si on augmente le nombre de foyers, 
* ou vers la gauche si on le diminue

![Logo](https://github.com/Younzer/Projets-applicatifs/blob/master/percolation/seuil_foyers.png "Seuil en fonction du nombre de foyers")
<div align="center">Figure 1</div>
Faire varier la taille de la forêt permet de déterminer plus précisément le seuil de percolation. Ce se trouve à l'intersection des courbes (cf. Fig 2). Nous pouvons observer que plus la taille de la forêt est importante, moins la courbe est lissée, et donc la pente qui caractérise le basculement est plus abrupte. Cela semble logique car elle est moins sensible aux événements rares comme par exemple quand une forêt de petite densité prend quasiment entièrement feu, ou à l'inverse quand une forêt de grande densité est grandement épargnée. Dans le grapge qui suit, nous avons simuler la propagation à partir d'un seul foyer.
![Logo](https://github.com/Younzer/Projets-applicatifs/blob/master/percolation/seuil_surface.png "Seuil en fonction de la superficie")
<div align="center">Figure 2</div>
### Conclusion
En conclusion de notre expérience, nous pouvons donc dire que le seuil varie si on fait varier le nombre de foyers, et qu'il est ***approximativement de 60%*** si on considère qu'il n'y a qu'un seul foyer au départ du feu.
