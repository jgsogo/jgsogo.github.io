Geolocalización de estaciones (ADIF)
====================================

:date: 2015-08-27 18:34
:tags: renfe, railway, geo, cartodb, trilateration
:slug: renfe-project-geo-stations

.. contents::

Dentro del `proyecto RENFE`_ una de las partes más importantes es determinar la posición de las
estaciones en el mapa (latitud y longitud). Una vez más tengo que reunir información de diversas
fuentes y hacerla coherente para generar el *dataset* que necesito, en concreto voy a utilizar
las siguientes fuentes:

* Renfe_: en su web podemos consultar un listado de estaciones.
* ADIF_: en la sección "infraestructuras y estaciones" se pueden obtener las coordenadas GPS
  de algunas estaciones.
* `La Estación de Tren`_: ofrece un listado de estaciones con coordenadas GPS etiquetadas manualmente.
* `Github - railopendata`_: con datos georreferenciados de estaciones y líneas.

Una vez obtenida la información de estas fuentes tengo que utilizar algunos **algoritmos** para
relacionarlos, hacerlos coherentes y completarlos. Y por supuesto, un poquito de ayuda manual
nunca les va a venir mal.

.. _proyecto RENFE: {filename}/Projects/renfe_project.rst
.. _Renfe: http://www.renfe.com/
.. _ADIF: http://adif.es
.. _La Estación de Tren: http://www.laestaciondetren.net/
.. _Github - railopendata: https://github.com/jgcasta/railopendata


Listado de estaciones
---------------------
La primera tarea que hay que realizar es obtener la lista (lo más completa posible) de estaciones. En
la web de Renfe tenemos un link [#]_, de donde se puede obtener con un simple *script* un primer listado.

.. [#] RENFE. Listado de estaciones. URL: https://venta.renfe.com/vol/estacionesAccesibleVXY.do

Cada estación tiene un nombre y un identificador. Este identificador es único y está formado por 5 dígitos,
sin embargo, en algunos casos se incorporan letras cuando no se trata de una estación concreta sino una ciudad
que dispone de varias estaciones: :code:`MADRI` para Madrid, :code:`IRUN-` para Irún-Hendaya,... en cualquier
caso, cada estación de la ciudad posee un identificador numérico único.

Los identificadores numéricos, donde aparecen, son la primera opción para identificar las estaciones; sin
embargo, en muchos otros casos, tendremos que utilizar los nombres y comparar de forma inexacta cadenas de
texto para identificar la estación (ver `comparación inexacta de cadenas <{filename}/Algorithms/fuzzy_string_comparison.md>`__). Estos nombres alternativos
los guardaremos como *alias* de la estación para utilizarlos en búsquedas futuras.


Posicionamiento
---------------
Una vez obtenido el listado de estaciones tengo que georreferenciarlas sobre el mapa. Como he indicado
más arriba para esta tarea utilizo varias fuentes:

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

Como consecuencia de ese parámetro debo utilizar alguna otra técnica para acceder a las páginas de
detalle de cada una de las estaciones: se puede utilizar un script que trabaje con el mapa, o partir de
la pestaña de "Llegadas y Salidas" a la que se puede acceder utilizando únicamente el identificador de
la estación (ej.: :code:`http://www.adif.es/AdifWeb/estacion_mostrar.jsp?e=20213`). Una vez ahí se puede
parsear la web para obtener el link de la pestaña "Información" donde tenemos las coordenadas GPS.

Podría parecer que aquí termina el trabajo, pero no es así; en la web de ADIF aparecen solo
200-240 estaciones (depende de si hay trenes que llegan/salen a la hora de la consulta),
pero tengo que geoposicionar unas 1300.

.. figure:: {filename}/images/renfe-stations-adif.png
   :align: center
   :alt: Mapa de estaciones

   Mapa de estaciones con las coordenadas GPS obtenidas de ADIF


Railopendata
++++++++++++
José Gómez Castaño (`@jgcasta`_) mantiene un `repositorio en Github`_ con un conjunto no oficial de datos de
ferrocarril en el que aparecen las posiciones de las estaciones y las geometrías de las líneas. Los datos
son accesibles y están en formato geoJSON por lo que resultan ideales para utilizarlos aquí.

.. _@jgcasta: https://twitter.com/jgcasta
.. _repositorio en Github: https://github.com/jgcasta/railopendata

Gracias a este repositorio de información logro posicionar ¡932 estaciones! Sin duda este es un
recurso valiosísimo al que andemas le concedo un altísimo grado de credibilidad.


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

Gracias a La Estación de Tren logro geoposicionar solo 25 estaciones de las que aún me faltaban.

.. figure:: {filename}/images/renfe-stations-laestaciondetren.png
   :align: center
   :alt: Mapa de estaciones

   Mapa de estaciones con las coordenadas GPS obtenidas de ADIF (naranja) y de La Estación de Tren (azul)

Sin embargo, existen unas muchas estaciones en este nuevo dataset que no es capaz de asociar a ninguna
de las existentes, ¿no hay trenes que hagan paradas en ellas? ¿Tan diferentes son los nombres?
¿Pertenecen a vías desmanteladas? Pues hay un poco de todo, será una información muy interesante a tratar
cuando tenga los datos de las líneas desmanteladas.

Buscadores/Mapas
++++++++++++++++
Una tercera vía que he utilizado para geoposicionar las estaciones ha sido utlizar los servicios de
Internet que permiten obtener las coordenadas de un punto a partir de su dirección. Hay una
fantástica librería que nos permite hacerlo con facilidad: geopy_.

.. _geopy: https://github.com/geopy/geopy

Como dato de entrada para todos estos servicios he utilizado el nombre de la estación con lo cual la
fiabilidad de los resultados es bastante baja en ocasiones (se obtienen estaciones dispersas
por toda la Tierra, pero sólo recogeré los datos de aquéllas que caigan en el entorno de la Península).

Puesto que dispongo de varias respuestas para cada estación puedo combinarlas para intentar mejorar
el resultado. Así filtro los *outliers* utilizando un test conocido como *median-absolute-deviation* (MAD_)
y posteriormente me quedo con la posición correspondiente a la media aritmética de todas las respuestas.

.. _MAD: https://stackoverflow.com/questions/22354094/pythonic-way-of-detecting-outliers-in-one-dimensional-observation-data/22357811#22357811

Con esta aproximación no consigo localizar ninguna de las estaciones que aún me quedan por posicionar :/
nivel de confianza que a las anteriores.

.. figure:: {filename}/images/renfe-stations-imaps.png
   :align: center
   :alt: Mapa de estaciones

   Mapa de estaciones con las coordenadas GPS obtenidas de ADIF (naranja), La Estación de Tren (azul)
   y las extraídas de mapas de internet (verde).

Tan sólo me han quedado 85 estaciones sin geolocalizar, lo cual considero que es un muy buen resultado. Además
puedo comprobar que estas estaciones están, en muchos casos, fuera de la Península o bien incluyen en su nombre
la partícula :code:`-BUS` o :code:`(*)` (indicando que se trata de una ciudad con varias estaciones). En el
primer caso la solución es fácilmente programable, en el segundo caso se podría interpretar cuál es la estación
correcta según los tipos de trenes que la utilicen.


Estaciones sin datos
--------------------
Son muy pocas las estaciones que han quedado sin datos y para ellas he pensado aplicar un algoritmo probabilístico
basado en la posición del resto de estaciones y en los horarios de los trenes que pasan por ellas. La idea es
calcular la zona en la cual es máxima la probabilidad de encontrar un tren tomando como parámetros los tiempos
de paso por las estaciones adyacentes y su velocidad. Básicamente un problema
de **trilateración con errores en las medidas**.

Trilateración
+++++++++++++
"La trilateración_ es un método matemático para determinar las posiciones relativas de objetos usando la
geometría de triángulos de forma análoga a la triangulación. [...] La trilateración usa las localizaciones
conocidas de dos o más puntos de referencia, y la distancia medida entre el sujeto y cada punto de
referencia" (Wikipedia_).

.. _Wikipedia: https://es.wikipedia.org/wiki/Trilateraci%C3%B3n

Puesto que tengo error en el cálculo de las distancias (no conozco la velocidad del tren, ni
las curvas que hace la vía y también puede haber error en el posicionamiento de la estación) cada
una de ellas la voy a aproximar mediante una distribución de probabilidad construida a partir de los datos
de todas las composiciones que hacen parada en dicha estación.

Este algoritmo de trilateración os lo cuento en otro artículo: (`ver artículo <{filename}/Algorithms/trilateration_with_errors.rst>`__)

.. Hablar de los resultados.

Proyección sobre las líneas
---------------------------
Un último paso, que también sirve para **validar las posiciones de las estaciones** (al menos para
detectar falsos positivos), consiste en proyectar la posición de las estaciones sobre el
mapa de líneas; de este modo si la distancia de la estación a la vía más cercana supera cierto umbral
puedo pensar que la posición de partida era errónea (o no tengo información sobre la
línea que pasa cerca de ese punto).

.. figure:: {filename}/images/renfe-stations-histogram.png
   :align: center
   :alt: Histograma con el error de posicionamiento de las estaciones

   Histograma (función de densidad) con la distancia de las estaciones a la vía más próxima, según el origen
   del dato de posicionamiento.

Se puede observar cómo los datos provinientes de la web de ADIF y los disponibles a través de `@jgcasta`_)
se proyectan sobre vías que pasan muy
próximas a ellos, los datos obtenidos de la web La Estación de Tren parece que tienen un *bias*, aún así
la gran mayoría parecen próximos a los datos de infraestructura de los que disponemos. Por el contrario,
cuando los datos los obtenemos utilizando el nombre de la estación para buscar las coordenadas en mapas
de internet, la dispersión es mucho mayor, la función de densidad presenta una cola extremadamente larga.
Se confirman las sospechas que tenía sobre la calidad del origen de los datos.

NOTA.- Los datos anteriores están construidos es base al error de posicionamiento de las estaciones según
la fuente de datos, pero en cada grupo no se consideran las estaciones ya posicionadas por otros métodos,
por lo tanto, si aplicara cada método al conjunto completo de estaciones se obtendrían mayores densidades
con los errores más pequeños (o ese sería lo esperable).


Más sobre el proyecto
---------------------
El proyecto se desarrolla en los siguientes artículos:

* Mapa dinámico de circulaciones (`ver artículo <{filename}/Projects/renfe_project.rst>`__).
* Geolocalización de estaciones (ADIF)
* La infraestructura ferroviaria (ADIF) (`ver artículo <{filename}/Projects/renfe_project_lines.rst>`__).
* Circulaciones de trenes (RENFE) (`ver artículo <{filename}/Projects/renfe_project_trains.rst>`__).

