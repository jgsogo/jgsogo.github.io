Title: Factorización de matrices no negativas
Date: 2015-03-05 12:54
Tags: machine-learning
Slug: non-negative-matrix-factorization


Ayer tuve la ocasión de conocer a [Carlos J. Gil Bellosta][datanalytics] gracias a la charla que dio en el *meetup*
de [*Machine Learning*][iv-meetup-machine-learning] en [La Nave Nodriza][la-nave-nodriza].
La verdad es que fui a la charla por el ponente, y luego además el tema me pareció interesantísimo.

La Factorización de Matrices no Negativas o Factorización No Negativa de Matrices (*Non-negative Matrix Factorization*, NMF)
es un método que nos permite representar una matriz positiva como producto de otras dos matrices positivas; es prima
hermana de otras representaciones como *Principal Component Analysis* (PCA) o *Singular Value Decomposition* (SVD).
Todas ellas buscan encontrar una representación de un conjunto de datos que nos permita reducir la dimensionalidad del
problema y, al mismo tiempo, mostrar ciertas características subyacentes del conjunto de datos.

Estas técnicas se utilizan en los **sistemas de recomendación** para identificar patrones, similaridades entre usuarios
o productos y elaborar recomendaciones.

En el blog de Carlos podéis encontrar las transparencias de la charla y algunos enlaces interesantes a este y muchos
otros temas, os dejo [aquí][datanalytics-iv-meetup-machine-learning] el enlace.


Definición del modelo
=====================


Algunos enlaces de interés y temas que mencionar:

 * [Proyecto fin de carrera](http://bibing.us.es/proyectos/abreproy/11088/fichero/Proyecto+Fin+de+Carrera%252F7.pdf)
 * [Carlos Gil Bellosta](http://www.datanalytics.com/2015/03/05/iv-meetup-machine-learning-spain-diapositivas-y-enlaces/)
 * Latent Dirichlet Allocation y su relación con NMF


Aplicaciones
============

Habrá que hablar de:

 * Sistema de recomendación
 * Topic modelling


Me encantó la conclusión de Carlos: ¿es esta la versión low-cost del Latent Dirichlet Allocation?

[iv-meetup-machine-learning]: http://www.meetup.com/MachineLearningSpain/events/220799458/ "IV Meetup Machine Learning Spain"
[datanalytics]: http://www.datanalytics.com/ "Datanalytics"
[la-nave-nodriza]: http://www.lanavenodriza.com/ "La Nave Nodriza"
[datanalytics-iv-meetup-machine-learning]: http://www.datanalytics.com/2015/03/05/iv-meetup-machine-learning-spain-diapositivas-y-enlaces/ "IV Meetup Machine Learning Spain: Diapositivas y Enlaces"