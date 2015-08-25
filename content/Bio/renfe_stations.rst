RENFE -- Geolocalización de estaciones
======================================

:date: 2015-08-25 18:34
:tags: renfe, railway, geo
:slug: renfe-geo-stations

.. contents::

Hace unos días me propuse hacer un mapa dinámico con CartoDB_ en el que se
mostraran los trenes de RENFE moviéndose con la única intención de probar la herramienta y experimentar
con sus posibilidades. El caso es que el proyecto crece, los datos no están tan disponibles como
uno quisiera y empiezan a aparecer los famosos *"ya que..."*.

.. _CartoDB: https://cartodb.com/

En este artículo trato de recapitular los pasos que he ido dando para geoposicionar las estaciones
de RENFE dejando constancia de los recursos y usuarios en los que me he apoyado. Sirva como
agradecimiento a los que han aportado su granito de arena.


Estado del arte
---------------
Como siempre lo primero es buscar un poco por Internet para ver quién ha hecho algo ya y, como siempre,
sin necesidad de bucear demasiado aparecen algunos resultados:

* Victoriano_ tiene un mapa donde muestra los `trenes de larga distancia en 2013`__ (ver imagen más abajo),
  sin embargo no es exactamente lo que busco. De todos modos, una pena que los datasets sean privados.
   
  .. figure:: {filename}/images/renfe-stations-victoriano.png
     :align: center
     :alt: Renfe - Trenes de larga distancia 2013

     **Renfe - Trenes de larga distancia 2013**.
     Los puntos naranjas son la estaciones según el nº de trenes que salen de esa estación.
     El azul es el nº de conexiones posibles con billete único que vende Renfe en viaje directo
     o con transbordo. Autor: Victoriano_
    
* Buscando un poco más encontramos los mapas de Astroide_, otro usuario de CartoDB que nos ofrece unos
  mapas mucho más interesantes para lo que queremos hacer, y que además ofrece públicamente los
  datasets: un mapa dinámico con los `trenes de largo recorrido`_ y otro con los `trenes de mercancias`_,
  que reproduzco a continuación:
  
  .. figure:: {filename}/images/renfe-stations-astroide-largadistancia.png
     :align: center
     :alt: Renfe - Trenes de larga distancia

     **Renfe - Trenes de Larga Distancia**.
     Recorrido efectuado por trenes de Larga Distancia. Estudio del uso de bases de datos NoSQL en
     la Fundación de los Ferrocarriles Españoles. Autor: Astroide_
    
    
  .. figure:: {filename}/images/renfe-stations-astroide-mercancias.png
     :align: center
     :alt: Renfe - Trenes de mercancias

     **Trenes de mercancías**.
     Reconstrucción del movimiento de los trenes de mercancías. Estudio del uso de bases de datos NoSQL en
     la Fundación de los Ferrocarriles Españoles. Autor: Astroide_
  
  Estos dos mapas son públicos y los datasets pueden descargarse, uno de ellos me será de muchísima
  utilidad: la información con las líneas de la infraestructura (pero esto es otra historia).
   
.. _Victoriano: https://twitter.com/victorianoi
__ https://victoriano-v21.cartodb.com/viz/aac847aa-e882-11e2-bc2b-d90ab36db2dd/public_map
.. _Astroide: https://astroide.cartodb.com/maps
.. _trenes de largo recorrido: https://astroide.cartodb.com/viz/83f346cc-18bc-11e5-a62d-0e9d821ea90d/public_map
.. _trenes de mercancias: https://astroide.cartodb.com/viz/5b6b5838-1aa7-11e5-858b-0e018d66dc29/public_map


Los mapas de Astroide muestran básicamente el resultado al que quiero llegar, pero el problema que
me planteo no es tanto obtener el mapa como disfrutar del camino hasta conseguirlo. Además, echo de
menos los trenes de media distancia y regionales, ¡y las estaciones!. Me pregunto: ¿cómo quedará el
mapa si se combinan todos estos trenes en una única visualización y mostramos también las estaciones?


Definición del problema
-----------------------
El reto sigue presente a pesar de los recursos que se han encontrado: para realizar mi mapa dinámico con
las circulaciones de trenes necesito posicionar las estaciones, conseguir los horarios de los trenes y
luego muestrear su posición a lo largo de un día o de una semana para mostrarlos en el mapa.

Las estaciones
++++++++++++++
En este artículo vamos a hablar de las estaciones.
