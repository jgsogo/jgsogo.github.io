Geolocalización de estaciones (ADIF)
====================================

:date: 2015-08-27 18:34
:tags: renfe, railway, geo, cartodb
:slug: renfe-project-geo-stations

.. contents::

Dentro del `proyecto RENFE`_ una de las partes más importantes es determinar la posición de las
estaciones en el mapa (latitud y longitud). Una vez más hemos de reunir información de diversas
fuentes y hacerla coherente para generar el *dataset* que necesitamos, en concreto vamos a
combinar datos de las siguientes fuentes:

* Renfe_: en su web podemos consultar un listado de estaciones.
* ADIF_: en la sección "infraestructuras y estaciones" se puede obtener las coordenadas GPS
  de algunas estaciones.
* `La Estación de Tren`_: ofrece un listado de estaciones con sus coordenadas GPS etiquetadas manualmente.

Una vez obtenida la información de estas fuentes tengo que utilizar algunos **algoritmos** para
relacionarlos, hacerlos coherentes y completarlos. Y por supuesto, un poquito de ayuda manual
nunca les va a venir mal.

.. _proyecto RENFE: {filename}/Projects/renfe_project.rst
.. _Renfe: http://www.renfe.com/
.. _ADIF: http://adif.es
.. _La Estación de Tren: http://www.laestaciondetren.net/


Listado de estaciones
---------------------
La primera tarea que hay que realizar es obtener la lista (lo más completa posible) de estaciones. En
la web de Renfe tenemos un link [#]_, de donde podemos obtener con un simple *script* un primer listado.

.. [#] RENFE. Listado de estaciones. URL: https://venta.renfe.com/vol/estacionesAccesibleVXY.do

Cada estación tiene un nombre y un identificador. Este identificador es único y está formado por 5 dígitos,
sin embargo, en algunos casos se incorporan letras cuando no identifica una estación concreta sino una ciudad
que dispone de varias estaciones: :code:`MADRI` para Madrid, :code:`IRUN-` para Irún-Hendaya,... en cualquier
caso, cada estación de la ciudad posee un identificador numérico único.

Los identificadores numéricos, donde aparecen, son la primera opción para identificar las estaciones; sin
embargo, en muchos otros casos, tendremos que utilizar los nombres y comparar de forma inexacta cadenas de
texto para identificar la estación (ver `comparación inexacta de cadenas <{filename}/Algorithms/fuzzy-string-comparison.md>`__). Estos nombres alternativos
los guardaremos como *alias* de la estación para utilizarlos en búsquedas futuras.


Posicionamiento
---------------
Una vez obtenido el listado de estaciones tengo que georreferenciarlas sobre el mapa. Como he indicado
más arriba, para esta tarea utilizo varias fuentes:

ADIF
++++
En la web de ADIF se pueden consultar los datos GPS de algunas estaciones, extraerlos del HTML no es
complicado, tal y como se puede ver en la imagen siguiente:

.. figure:: {filename}/images/renfe-stations-adif-gps.png
   :align: center
   :alt: Coordenadas GPS de una estación en la web de ADIF

   Coordenadas GPS de una estación en la web de ADIF.

Sin embargo, las URLs de esta página siguen un patrón que no he podido identificar, aparece un identificador
numérico al final que impide construirlas de forma automática. Algunos ejemplos:

===== ============= =====
 ID    Nombre        URL
===== ============= =====
23004 Pontevedra    http://www.adif.es/es_ES/infraestructuras/estaciones/23004/informacion_000047.shtml
30002 Plasencia     http://www.adif.es/es_ES/infraestructuras/estaciones/30002/informacion_000141.shtml
74200 Huesca        http://www.adif.es/es_ES/infraestructuras/estaciones/74200/informacion_000099.shtml
===== ============= =====

Como consecuencia de ese parámetro debemos utilizar alguna otra técnica para acceder a las páginas de
detalle de cada una de las estaciones: se puede utilizar un script que trabaje con el mapa o partir de
la pestaña de "Llegadas y Salidas" a la que se puede acceder utilizando únicamente el identificador de
la estación (ej.: :code:`http://www.adif.es/AdifWeb/estacion_mostrar.jsp?e=20213`). Una vez ahí se puede
parsear la web para obtener el link de la pestaña "Información" donde tenemos las coordenadas GPS.

Podría parecer que aquí termina el trabajo, pero no es así; en la web de ADIF aparecen algo más de
240 estaciones, pero tenemos que geoposicionar unas 1300.

.. figure:: {filename}/images/renfe-stations-adif.png
   :align: center
   :alt: Mapa de estaciones

   Mapa de estaciones con las coordenadas GPS obtenidas de ADIF


La Estación de Tren
+++++++++++++++++++
**Fernando Solabre** es el autor de la web La Estación de Tren, en la que se muestra un listado de 1915 estaciones
geolocalizadas manualmente e identificadas por el nombre que aparece en los mapas. El trabajo realizado merece
una mención especial y me va a permitir posicionar muchas estaciones.

Para utilizar este dataset nos enfrentamos a dos dificultades: identificar la estación y convertir las coordenadas
de UTM a longitud/latitud. Para la primera de ellas utilizaremos la comparación inexacta de cadenas a la que
hemos hecho mención anteriormente, para la segunda utlizamos la librería de Python llamada utm_.

.. _utm: https://github.com/Turbo87/utm

Al automatizar el procesamiento de este conjunto de datos no tengo garantías de que la identificación de
las estaciones haya sido correcta, confío en que los algoritmos posteriores muestren incongruencias ante
un dato erroneo y me permita identificarlos.

Gracias a La Estación de Tren logro geoposicionar otras ¡692 estaciones!

.. figure:: {filename}/images/renfe-stations-laestaciondetren.png
   :align: center
   :alt: Mapa de estaciones

   Mapa de estaciones con las coordenadas GPS obtenidas de ADIF (naranja) y de La Estación de Tren (azul)

Sin embargo, existen unas 800 estaciones en este nuevo dataset que no es capaz de asociar a ninguna
de las existentes, ¿no hay trenes que hagan paradas en ellas? ¿Tan diferentes son los nombres?
¿Pertenecen a vías desmanteladas? Pues hay un poco de todo, será una información muy interesante a tratar
cuando tenga la información de las líneas desmanteladas.

Buscadores/Mapas
++++++++++++++++
Una tercera vía que he utilizado para geoposicionar las estaciones ha sido utlizar los servicios de
Internet que permiten obtener las coordenadas de un punto a partir de su dirección. Hay una
fantástica librería que nos permite hacerlo sin despeinarnos: geopy_.

.. _geopy: https://github.com/geopy/geopy

Como dato de entrada para todos estos servicios he utilizado el nombre de la estación con lo cual la
fiabilidad de los resultados es bastante baja en ocasiones (se obtienen estaciones dispersas
por toda la Tierra, pero sólo recogeré los datos de aquéllas que caigan en el entorno de la Península).

Puesto que dispongo de varias respuestas para cada estación puedo combinarlas para intentar mejorar
el resultado. Así filtro los *outliers* utilizando un test conocido como *median-absolute-deviation* (MAD_)
y posteriormente me quedo con la posición correspondiente a la media aritmética de todas las respuestas.

.. _MAD: https://stackoverflow.com/questions/22354094/pythonic-way-of-detecting-outliers-in-one-dimensional-observation-data/22357811#22357811

Con esta aproximación consigo localizar otras 330 estaciones, eso sí, no puedo darles el mismo
nivel de confianza que a las anteriores.

.. figure:: {filename}/images/renfe-stations-imaps.png
   :align: center
   :alt: Mapa de estaciones

   Mapa de estaciones con las coordenadas GPS obtenidas de ADIF (naranja), La Estación de Tren (azul)
   y las extraídas de mapas de internet (verde).

Tan sólo me han quedado 35 estaciones sin geolocalizar, lo cual considero que es un muy buen resultado. Además
puedo comprobar que estas estaciones están, en muchos casos, fuera de la Península o bien incluyen en su nombre
la partícula :code:`-BUS`, fácilmente identificable, que podría eliminar para repetir la búsqueda.


Estaciones sin datos
--------------------
Son muy pocas las estaciones que han quedado sin datos y para ellas he pensado aplicar un algoritmo probabilístico
basado en la posición del resto de estaciones y en los horarios de los trenes que pasan por ellas. La idea es
calcular la zona en la cual es máxima la probabilidad de encontrar un tren tomando como parámetros los tiempos
de paso por las estaciones y su velocidad. Básicamente un problema de **trilateración con errores en las medidas**.

Trilateración
+++++++++++++
"La trilateración_ es un método matemático para determinar las posiciones relativas de objetos usando la
geometría de triángulos de forma análoga a la triangulación. [...] La trilateración usa las localizaciones
conocidas de dos o más puntos de referencia, y la distancia medida entre el sujeto y cada punto de
referencia" (Wikipedia_).

.. _Wikipedia: https://es.wikipedia.org/wiki/Trilateraci%C3%B3n

Puesto que tenemos error en el cálculo de las distancias (no conocemos la velocidad del tren, ni
las curvas que hace la vía y también puede haber error en el posicionamiento de la estación) cada
una de ellas la voy a aproximar mediante una distribución normal que contenga el 95% entre la
distancia mínima estimada (velocidad mínima) y la máxima (velocidad máxima en línea recta).

Este algoritmo os lo cuento en otro artículo: (en construcción)


Proyección sobre las líneas
---------------------------
Un último paso, que también nos sirve para **validar las posiciones de las estaciones** (al menos para
detectar falsos positivos) consiste en proyectar la posición de las estaciones sobre el
mapa de líneas, de este modo si la distancia
de la estación a la vía más cercana supera cierto umbral podemos pensar que la posición de
partida no era correcta (o no tenemos información sobre la línea que pasa cerca de ese punto).

.. Incluir gráfica de resultados: cuántas estaciones geolocalizadas con cada tecnología y
   cuantas se han podido proyectar (y cuantas no)

.. Incluir figura con el mapa final: estaciones + líneas



Más sobre el proyecto
---------------------
El proyecto se desarrolla en los siguientes artículos:

* Mapa dinámico de circulaciones (`ver artículo <{filename}/Projects/renfe_project.rst>`__).
* Geolocalización de estaciones (ADIF)
* La infraestructura ferroviaria (ADIF) (en construcción).
* Circulaciones de trenes (RENFE) (en construcción).
