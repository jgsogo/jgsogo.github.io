ChimpPunch
==========

:date: 2015-09-15 19:00
:tags: information retrieval, startup
:slug: chimppunch
:status: draft

Como últimamente mucha gente me pregunta por **ChimpPunch** voy a dejar escritas aquí
algunas cosas para tenerlas como referencia. ChimpPunch fue un proyecto de *startup* que
inicié junto a `Rafael P. Campoamor`_ (CEO) y `Carlos Mañas`_ (UI/UX) allá por 2012, con la idea de
hacer un sistema que facilitara la gestión de redes sociales (la tríada *discover*,
*stream*, *analyze*) para las pequeñas empresas o marcas personales.

.. _Rafael P. Campoamor: https://twitter.com/rafacampoamor
.. _Carlos Mañas: https://twitter.com/oneeyedman

.. figure:: {filename}/images/chimppunch.png
   :align: center
   :alt: Logotipo de ChimpPunch

   El monete, imagen de ChimpPunch (dibujo de @oneyedman).

El producto no llegó a buen puerto; si no, en vez de estar utilizando `@buffer`_
ahora, tendríais a un monete mucho más simpático trabajando para vosotros ;D Sí llegamos a tener
un *MVP*, pero para salir en aquel momento nos faltaba (o eso creímos nosotros) mucho más de
*machine-learning* y de *analytics* de lo que teníamos; y una sucesión de desafortunadas casualidades
provocó que nos detuviéramos y ya no supimos arrancar de nuevo.

.. _@buffer: https://twitter.com/buffer

Aunque abandonamos el proyecto formalmente yo continué interesándome por la parte de
recolección de contenidos, clasificación,... y seguí mejorando y desarrollando algunos módulos,
convirtiéndolos en servicios y automatizando su funcionamiento. Fruto de ello he creado *bots*
para Twitter que mantienen con vida algunas cuentas como `@EstudiaHistoria`_,  `@chimp_news`_ o `@grupoalpino`_ y
también me he interesado más formalmente por la Inteligencia Artificial y el Procesamiento de
Lenguaje Natural, que se manifiestan hoy en el `Máster Universitario en Inteligencia Artificial`_
que hice el año pasado y el grupo de `Lingẅars`_ que estamos creando.

.. _@EstudiaHistoria: https://twitter.com/estudiahistoria
.. _@chimp_news: https://twitter.com/chimp_news
.. _@grupoalpino: https://twitter.com/grupoalpino
.. _Máster Universitario en Inteligencia Artificial: http://www.dia.fi.upm.es/masteria/?q=es/MUIA
.. _Lingẅars: http://lingwars.github.io/blog/


Diseño conceptual
-----------------
Como he indicado antes, ChimpPunch estaba dividido en tres módulos principales:

1. Recuperación de información: obtención, clasificación y recomendación de contenidos.
2. *Stream* de publicaciones: el cliente tiene a su alcance una herramienta para
   programar publicaciones y centralizar el trabajo de todas sus redes sociales y de
   todo su equipo.
3. Análisis: nuestra herramienta realiza un análisis *a posteriori* del comportamiento
   de las publicaciones para actualizar los modelos del motor de recomendación.

Recuperación de información
+++++++++++++++++++++++++++
En la figura de abajo muestro el diseño conceptual de la parte correspondiente a
**recuperación de información** de ChimpPunch:

1. El sistema está recogiendo continuamente documentos de un conjunto de fuentes dinámico
   (según clientes y sus comunidades) y clasificándolos por todo tipo de criterios:
   fuentes, autores, temáticas,...
1. Los clientes pueden establecer criterios y filtros de selección de contenidos, o bien dejar
   que ChimpPunch aprenda estos criterios en base a los intereses de la comunidad de seguidores
   de cada cliente.
1. El comportamiento de las noticias originales en los medios da un índice de popularidad, interés
   o viralidad que se utiliza para puntuarlas. Se crea así el conjunto de datos etiquetado sobre
   el que se trabaja para puntuar los nuevos contenidos que van recuperándose.
1. Cada cliente tiene acceso a una lista de contenidos adecuados a sus intereses (*discover*),
   clasificados por relevancia e impacto, que van a ser bien recibidos por su comunidad.

.. figure:: {filename}/images/chimppunch-conceptual.png
   :align: center
   :alt: Diseño conceptual de ChimpPunch

   Diseño conceptual de ChimpPunch con la división en módulos principales.

Stream de publicaciones
+++++++++++++++++++++++
En ChimpPunch dábamos la posibilidad de gestionar todas las redes sociales desde un único sitio
y además facilitábamos la posibilidad de que varias personas compartieran un único espacio
de trabajo online para realizar esta tarea.

Permitíamos al usuario definir horarios de publicación y programar tweets, nada nuevo hoy en día
cuando existen tantas herramientas de gestión de redes sociales.

Analitycs
+++++++++
El último módulo, en el que no llegamos a profundizar, consistía en la parte de análitica del
comportamiento de las publicaciones realizadas por el usuario. Habría dos niveles de análisis:

1. Estadística descriptiva: gráficos y tablas mostrando cómo se habían comportado las publicaciones,
   típicos dibujitos que muestran muchos datos, pero poca información realmente útil para el usuario.
   No obstante, estos datos se utilizarían para actualizar el modelo de recomendación de contenidos
   y personalizarlo para cada cliente (¿os suena Bayes?)
2. Información: en base a las interacciones con los contenidos pretendíamos facilitar al
   usuario datos sobre sus clientes que permitieran segmentarlos e identificar el tipo de
   publicaciones que consumían para ayudar en el diseño de campañas de marketing y maximizar
   las métricas de conversión.

ChimpPunch hoy
--------------
Aunque el proyecto en su conjunto se detuvo yo continué el desarrollo centrado en la parte de
recuperación de información y, a partir de ahí, he desarrollado dos aplicaciones que funcionan
como servicio y que están envejeciendo bastante bien:

* **chimp_scraper**: se trata de un servicio para obtener información estructurada de una web;
  parte de una base de datos introducida por el usuario (yo) con cadenas XPath y regex para
  obtener datos característicos de un post (autor, tags, fecha de publicación, fotos, contenido,...)
  y con ellos trata de obtener la misma información de cualquier otra URL que se le pase.
  Supongo que algo así debió ser el MVP de `Import.io`_.

.. _Import.io:

* **chimp_social_monitor**: servicio para monitorizar el comportamiento de una URL en redes
  sociales. Una vez que la URL está dada de alta se encarga de recoger información de Twitter,
  Facebook, G+ y LinkedIn, almacenarla y devolverla aplicando diferentes filtros.

Ambas aplicaciones las orquesto a través de una interfaz web **chimp_discovery** que se encarga
de interactuar con el usuario, almacenar sus preferencias, sus horarios de publicación y la
lista de publicaciones.

Como podéis ver el proyecto era completito y muy interesante. Una pena que se quedara en el cajón,
aunque indudablemente es una experiencia más que incorporar a la mochila de herramientas
y un conjunto de conocimientos muy importante.

