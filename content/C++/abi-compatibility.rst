ABI compatibility is not a MAJOR problem
========================================

:date: 2019-04-22 13:30
:tags: abi, c++, package management, cpprussia
:slug: abi-compatibility-russia

.. contents::

Todo gran poder conlleva una gran responsabilidad, o toda ventaja eventualmente
terminará convirtiéndose en un problema. En C++ tenemos la gran suerte de
desarrollar aplicaciones nativas, esto nos permite acceder a los recursos del
sistema y obtener un rendimiento en nuestras aplicaciones difícilmente alcanzable
desde otros lenguajes interpretados o que corren sobre máquinas virtuales; sin
embargo, al mismo tiempo, nuestra aplicaciones están compiladas a código máquina
y las ejecuta directamente el sistema operativo así que los datos que intercambian
entre ellas y las llamadas que se realizan entre librerías deben seguir unas
convenciones particulares para que todo funcione. Si alguna de estas convenciones
no se cumple nuestra aplicación fallará.

Este tipo de fallos en tiempo de ejecución debidos a incompatibilidades entre
las aplicaciones o con el sistema operativo generalmente están relacionados con
lo que se conocemos como **compatibilidad binaria** o **ABI compatibility**.

API y ABI, madre e hija
-----------------------

La ABI (Application Binary Interface) no debe confundirse con la API (Application
Programming Interface) aunque veremos que están relacionadas. La API es el
conjunto de funciones y datos que una librería expone para que otra los utilice
y poder construir aplicaciones sobre ella; mientras que la ABI es la interfaz
a nivel binario entre dos módulos de un programa.

La API funciona como un contrato que publica la librería. En este contrato se
indican los nombres de las funciones, los parámetros que reciben, su tipo, el 
tipo de retorno y por supuesto el comportamiento que cabe esperar de su ejecución.
Algunas de las cosas listadas anteriormente las verificará el lenguaje durante 
el proceso de compilación, otras deberán estar especificadas en la documentación.

Por su parte, la ABI es algo más compleja, y depende de muchos más factores: por
supuesto del código fuente (las funciones publicadas, los tipos de datos, tamaño
y disposición de las estructuras de datos,...), pero también de otros muchos 
aspectos que no están bajo el control del desarrollador sino del entorno en que
se genera la aplicación ejecutable final o incluso del contexto en el que va
a ejecutarse. Todos estos son aspectos más relacionados con el mundo de la integración
continúa y el DevOps que con la programación a la que estamos acostumbrados, pero
cada vez son más importantes para cualquier desarrollador de software actual.

Compatibilidad binaria
----------------------

Cuando compilamos una aplicación el código fuente que hemos escrito se transforma
en código máquina, los nombres utilizados por el linker ya no son los mismos que 
había en los archivos de texto (estos nuevos nombres se conocen como *mangled names*
y dependen de factores asociados con el compilador) y en el momento de ejecutar
el programa todas estas funciones y variables deberán estar en los módulos que
conforman la aplicación o en las librerías de las que ésta depende.

Así ocurre que una aplicación compilada con un compilador específico no funcionará
con las librerías compiladas por otro compilador, utilizando otro conjunto de
*flags* o con las librerías correspondientes a otra sistema operativo.
Debemos ser muy cuidadosos para no mezclar librerías una vez que el proyecto
crece si es que estamos distribuyendo binarios para diferentes compiladores o 
plataformas.

Compilar desde fuentes
----------------------

Una estrategia demasiado habitual y que asegura un resultado correcto
consiste en compilar toda la aplicación desde el código fuente cada vez
que se quiere generar un entregable. Nos aseguramos así de que el compilador,
su versión y todas las opciones y *flags* son los mismos para todas las 
librerías del proyecto y que el producto generado es congruente en todas 
sus partes.

Sin embargo, como hemos indicado anteriormente, hay algunas librerías
proporcionadas por el sistema operativo en el que se ejecuta la aplicación 
y éstas deben ser también compatibles con ella. Se puede llevar esta
aproximación de compilar siempre desde fuentes al extremo de compilar la
aplicación final en la máquina que la va a ejecutar, nos aseguraremos así 
también de que las versiónes de las librerías del sistema que utilizamos 
para linkar serán las mismas que al ejecutar.

Esta aproximación, a pesar de garantizar un resultado correcto, tiene algunos
incovenientes que la hacen inviable en muchos casos: **los elevados de tiempos
de compilación** y algunas plataformas en las que querremos ejecutar nuestra
aplicación, pero en las que **no podemos permitirnos instalar un compilador** 
para generarla (sistemas con pocos recursos, dispositivos embebidos,
microprocesadores,...).

De esto modo surge, para un caso más general, la necesidad de otras 
aproximaciones que permitan reaprovechar librerías ya compiladas asegurando
la trazabilidad de los binarios desde el código fuente y preservando 
toda la información relevante del proceso de compilación.

Explosión combinatoria
----------------------

No parece muy complicado mantener una base de datos que contenga todos los binarios
posibles de cada librería con la que trabajamos y les asocie la información del
código fuente y las herramientas utilizadas para generarlos (descartemos desde ya
la opción de darle un nombre diferente a cada binario o de guardarlos en 
diferentes directorios). Si nuestra aplicación la vamos a distribuir para 
diferentes plataformas utilizando diferentes compiladores, deberemos:

* generar distintos binarios para Windows, Linux, Macos, Android,... y para cada una
  de sus versiones, distribuciones o sabores que puedan ser incompatibles.
* almacenar diferentes binarios para cada compilador que utilicemos y que
  produzca una ABI diferente: GCC, Visual Studio, clang, Sun,...
* considerar que los *flags* y las opciones de compilación o de optimización de
  cada uno de los compiladores pueden generar binarios incompatibles, y también 
* tener en cuenta las opciones de la propia librería que producirán binarios
  incompatibles: algunas librerías permiter activar *features* opcionales,
  seleccionar algún tipo de dato,... todo ello puede tener impacto en la
  interfaz binaria generada.

Son unos cuantos factores a tener en cuenta y si pensamos que cada uno de ellos
se puede combinar con cada uno de los de los otros grupos nos daremos cuenta de
que el número de binarios diferentes que se pueden generar a partir de un mismo
código fuente no es despreciable. Muchos de ellos quizá no tengan sentido o sean
directamente inalcanzables (p.ej.: actualmente no es posible comopilar una aplicación de
C++ utilizando Visual Studio en Linux), pero aún así el número final es bastante elevado.

Si aún así el número no te parece suficientemente elevado ten en cuenta que
normalmente los proyectos no constan de una única librería sino que una aplicación
de software se construye reutilizando el código de varias, todas ellas forman un
grafo más o menos grande donde cada uno de los nodos puede tener diferentes
configuraciones y combinarse con todas las configuraciones de todos los demás.
Según el tamaño del grafo, así será el problema de explosión combinatoria.

Gestionar el problema
---------------------

Una vez que se conocen todos los elementos que pueden afectar a la compatibilidad
binaria y se automatiza el proceso para recogerlos y almacenarlos junto al
binario generado parece que la compatibilidad binaria no es un gran problema. Si
mantenemos un orden en esta base de datos de binarios, igual que los almacenamos
podremos recuperarlos utilizando como índices la configuración, las opciones,
las dependencias y toda la información necesaria para identificarlos 
biunívocamente. En vez de compilar un binarios, podremos hacer una búsqueda en
la base de datos y, en caso de que ya haya uno para la configuración requerida,
descargarlo en vez de lanzar la compilación.

El problema de la compatibilidad binaria ya no parece un gran problema, se trata
más bien de un problema de gestión que requiere orden, disciplina y un proceso
meticuloso para gestionarlo.

Podemos diseñar una herramienta y configurar una base de datos, poner a nuestros
desarrolladores a implementar algo parecido y dedicar los recursos necesarios
a construir este sistema en vez de continuar desarrollando las herramientas que
realmente aportan valor a nuestros clientes. Podemos desarrollar nuestra
solución *in-house* centrada en nuestro caso de uso, y modificarla cuando
aparezcan nuevas necesidades, quizá podems contratar a un consultor externo para
que nos ayude en el proceso.

Al cabo del tiempo habremos construído un sistema que nos permite ahorrar
muchísimas horas en tiempos de compilación, agilizando los procesos de 
integración y de calidad antes de entregar al cliente final. Tendremos más
información sobre nuestros entegrables y habremos conseguido cierta trazabilidad
entre el código fuente y los binarios, que nos permitirá ser más eficientes
a la hora de solucionar bugs.

Aún así, este sistema servirá únicamente para nuestra compañía, para nuestras
librerías, cada desarrollador tendrá que aprender a utilizarlo y adaptarse a
él y **cada nueva librería tendrá que ser modificada para amoldarse**, no se
tratará de un estándar de facto que nos vaya a permitir integrar otras librerías
desarrolladas por la comunidad o incluso por otras empresas a las que estemos
comprando sus librerías sin tener que modificarlas o hacer ciertos ajustes.

Una solución para todos
-----------------------

El trabajo que realizo en Conan persigue este escenario ideal en el que tanto
las librerías de la comunidad como las desarrolladas por las empresas se
adapten a unas convenciones que permitan implementar un mundo como el que
he descrito anteriormente. Un mundo donde los esfuerzos de diferentes agentes se
combinen para facilitar la vida a los desarrolladores:

compilar una librería
y empezar a utilizar las funcionalidades que proporciona no debería ser un
problema, un mismo equipo nunca debería compilar 

 evitar compilar
contin evitar compilar continuamente los mismos binarios, donde
se agilizen los tiempos de desarrollo


Al tener en cuenta todos estos factores, 

. Cuando somos una compañía
que vende una aplicación o una librería en formato binario


; además
no está definida por el estándard de C++. 

Durante la compilación tiene lugar el proceso de conversión del código fuente
en la aplicación (o librería) nativa
La compilación es el proceso mediante el cual 
Los errores en tiempo de ejecución relacionados con 
