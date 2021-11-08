---
lang: es
title: WordNet-blast. Con `boost::add_edge` hemos topado.
date: 2015-08-20
author: jgsogo
category: C++
tags: 
  - profiling
  - boost-graph-library
  - _ITERATOR_DEBUG_LEVEL
  - workaround
---


<content-github-repository repository="jardon-u/wordnet-blast">WordNet-blast</content-github-repository>
es una biblioteca de C++ creada por [Ugo Jardonnet](http://logserv.free.fr/) para construir en memoria el gráfico de
[WordNet](http://wordnet.princeton.edu/) y permitir un acceso rápido a los *synsets* y sus
relaciones.

<!--more-->

Encontré esta librería buscando recursos lingüísticos para mi tesis de fin de máster, en ella
necesitaba cálcular la distancia semántica entre conceptos y para ello utilizaba el grafo de WordNet,
así que esta librería, que utiliza la Boost Graph Library (BGL), resultaba perfecta para lo que
quería hacer.

<base-alert type="next">
En todo lo que se sigue hay que tener en cuenta que las pruebas se han
realizado con Microsoft Visual Studio Premium 2013. Version 12.0.40418.00 Update 5 RC.
</base-alert>

Sin embargo, había un **problema**: el tiempo empleado en la construcción del grafo en memoria era
excesivo cuando se ejecutaba en *debug* (hablo de minutos) lo que complicaba las tareas de depuración.
Así que aprovechando unos días de relax me he dedicado a darle un lavado de cara a la librería y a
tratar de acelerar la construcción del grafo en
<content-github-repository repository="jgsogo/wordnet-blast">mi repositorio</content-github-repository>.

Sin embargo, no he sido capaz (aún). Me he encontrado con un caballo de batalla contra el que no quiero
pelear: la función ``_Orphan_me``, que, tal y como se ve en la imagen siguiente, supone más del 90% del tiempo
de ejecución de la aplicación:

<article-image
    src="/img/2015/wordnet-blast_profiling_1.png"
    caption="Profiling librería wordnet-blast"></article-image>

Esta función es llamada desde ``boost::add_edge`` cuando se crea un nuevo arco en el grafo. es decir, cada
vez que añadimos una nueva relación al grafo de WordNet que estamos construyendo en memoria:

<article-image
    src="/img/2015/wordnet-blast_profiling_2.png"
    caption="Profiling librería wordnet-blast"></article-image>

Si buscamos el código de la función podemos ver que sólo se ejecuta en caso de que la macro de preprocesador
``_ITERATOR_DEBUG_LEVEL`` valga 2. Es decir, que sólo tenemos que preocuparnos si estamos compilando con
Microsoft y en debug (salvo que establezcamos este valor nosotros mismos) (**NOTA** Esta macro se añade en
Microsoft Visual Studio 2010).

```cpp
	void _Orphan_me()
		{	// cut ties with parent
 #if _ITERATOR_DEBUG_LEVEL == 2
		if (_Myproxy != 0)
			{	// adopted, remove self from list
			_Iterator_base12 **_Pnext = &_Myproxy->_Myfirstiter;
			while (*_Pnext != 0 && *_Pnext != this)
				_Pnext = &(*_Pnext)->_Mynextiter;

			if (*_Pnext == 0)
				_DEBUG_ERROR("ITERATOR LIST CORRUPTED!");
			*_Pnext = _Mynextiter;
			_Myproxy = 0;
			}
 #endif /* _ITERATOR_DEBUG_LEVEL == 2 */
		}
```

Para más información sobre ``_ITERATOR_DEBUG_LEVEL`` puedes consultar esta
[documentación de Microsoft](https://msdn.microsoft.com/en-us/library/hh697468.aspx), o este
[vídeo de Stephan T. Lavavej](https://channel9.msdn.com/Series/C9-Lectures-Stephan-T-Lavavej-Advanced-STL/C9-Lectures-Stephan-T-Lavavej-Advanced-STL-3-of-n):

<iframe src="https://channel9.msdn.com/Series/C9-Lectures-Stephan-T-Lavavej-Advanced-STL/C9-Lectures-Stephan-T-Lavavej-Advanced-STL-3-of-n/player" width="640" height="360" allowFullScreen frameBorder="0"></iframe>


### Workaround
Entonces, ¿qué podemos hacer? Básicamente eliminar todas las comprobaciones que se realizan por defecto
en debug (``_ITERATOR_DEBUG_LEVEL == 2``) y cambiar el valor de esta macro. Debemos tener en cuenta que
al eliminar todas estas comprobaciones, en caso de error en el código, tendremos un comportamiento indeterminado
en vez de la *amigable* alerta *Debug Assertion* que nos indica que algo ha ido mal y nos permite ir al punto
del código donde ha sucedido.

Como siempre, hay solución/workaround, pero hay que tener muy presente cuáles son las consecuencias (*side effects*).

Seguimos trabajando en ello.
