Variadic templates and std::tuple - Motivación
==============================================

:date: 2016-03-21 12:54
:tags: variadic templates, metaprogramming, django queryset
:slug: variadic-templates-std-tuple-motivation


Debo confesar que me he pasado prácticamente todo el fin de semana dándole
vueltas a las *variadic templates* para utilizarlas con las estructuras ``std::tuple``.
Y debo confesar que me parece impresionante lo que se puede conseguir (y eso
que me imagino que no he raspado más que la superficie), son una herramienta
increiblemente potente para construir librerías genéricas sin incrementar la
`complejidad ciclomática`_ del programa.

.. _`complejidad ciclomática`: https://en.wikipedia.org/wiki/Cyclomatic_complexity


Motivación
----------

A raíz de un proyecto personal me he tenido que enfrentar a la ingesta de *grandes*
cantidades de datos en formato tabular (básicamente un dump de una base de datos)
y, aunque ya había hecho algo al respecto [#]_ quería darle una vuelta al tema y darme una
excusa para probar las *variadic* junto con las tuplas. 

Quería reproducir una manera eficiente y fuertemente tipada de leer los datos de los archivos,
acceder a ellos, filtrarlos, proyectarlos,... en cierto modo quería la simplicidad y
potencia que pone a nuestra disposición los *managers* y las *querysets* de Django, 
pero quería descansar un poco de Python e implementarlo en C++.

Aún no lo he conseguido, ni mucho menos, todavía hay mucho trabajo por delante, pero creo
que la línea de desarrollo elegida promete y quiero compartirlo.

.. [#] Hago referencia al proyecto txt_table_ que, visto lo visto, ya ha caducado.
.. _txt_table: https://github.com/jgsogo/txt_table


std::tuple - a single row
-------------------------

La librería estándar proporciona desde hace tiempo (C++11) una clase que permite almacenar un
conjunto heterogeneo de valores de tamaño fijo (no tienes excusa para no conocerla). Desde
mi punto de vista es una estructura ideal para representar una fila de una tabla de una base
de datos. El ejemplo de cppreference_ me parece estupendo:

.. _cppreference: http://en.cppreference.com/w/cpp/utility/tuple

.. code:: cpp

    #include <tuple>
    #include <iostream>
    #include <string>
    #include <stdexcept>
     
    std::tuple<double, char, std::string> get_student(int id)
    {
        if (id == 0) return std::make_tuple(3.8, 'A', "Lisa Simpson");
        if (id == 1) return std::make_tuple(2.9, 'C', "Milhouse Van Houten");
        if (id == 2) return std::make_tuple(1.7, 'D', "Ralph Wiggum");
        throw std::invalid_argument("id");
    }
     
    int main()
    {
        auto student0 = get_student(0);
        std::cout << "ID: 0, "
                  << "GPA: " << std::get<0>(student0) << ", "
                  << "grade: " << std::get<1>(student0) << ", "
                  << "name: " << std::get<2>(student0) << '\n';
     
        double gpa1;
        char grade1;
        std::string name1;
        std::tie(gpa1, grade1, name1) = get_student(1);
        std::cout << "ID: 1, "
                  << "GPA: " << gpa1 << ", "
                  << "grade: " << grade1 << ", "
                  << "name: " << name1 << '\n';
    }

Si tuviéramos una tabla con el GPA, el *grade* y el *name* de un conjunto de estudiantes, yo
querría representar cada fila de esta forma, fuertemente tipada, así no hay problemas y todo
queda claro.


std::vector<std::tuple> - the queryset
--------------------------------------

Pero en una base de datos lo que tenemos es un conjunto de filas, de elementos ``std::tuple<...>``
de los del apartado anterior; un vector de estos elementos sería la representación en memoria de
un queryset_ de Django; sólo habría que dotarlo de la funcionalidad adecuada.

.. _queryset: https://docs.djangoproject.com/es/1.9/ref/models/querysets/

.. code:: cpp

    #include <tuple>
    #include <vector>
    
    class StudentsManager {
        public:
            typedef std::tuple<int, double, char, std::string> row_type;
            typedef std::vector<row_type> queryset_type;
        public:
            static void all(queryset_type& qs) {
                qs.push_back(std::make_tuple(0, 3.8, 'A', "Lisa Simpson"));
                qs.push_back(std::make_tuple(1, 2.9, 'C', "Milhouse Van Houten"));
                qs.push_back(std::make_tuple(2, 1.7, 'D', "Ralph Wiggum"));
            }
    };
    
    int main() {
        StudentsManager::queryset_type queryset;
        StudentsManager::all(queryset);
        
        // Dump all students
        for (auto& item: queryset) {
            std::cout << "ID: " << std::get<0>(item) << ", "
                      << "GPA: " << std::get<1>(item) << ", "
                      << "grade: " << std::get<2>(item) << ", "
                      << "name: " << std::get<3>(item) << '\n';
        }
    }

Y podríamos crear fácilmente funciones que sirvieran para realizar las operaciones más
comunes con este conjunto de datos:

.. code:: cpp

    [...]
        // Sort according to function
        auto sorted_students = std::sort(queryset.begin(), queryset.end(),
            [](const StudentsManager::row_type& lhs, const StudentsManager::row_type& rhs) {
                return std::get<2>(lhs) < std::get<2>(rhs);
            });
            
        // Filter by field value
        auto gradeA_students = filter(queryset, 'A');
        
    [...]
    

El problema surge al generalizar
--------------------------------

Como tengo alma de programador no me vale con crear una clase que actúe como *manager* para
cada uno de mis modelos, sino que quiero generalizar. Y el problema es que quiero **generalizar
en dos dimensiones: tipo de elementos y número de columnas de la tabla**.

Generalizar en tipo de elementos es fácil, ahí están las plantillas. Algo como lo que sigue
podría valer:

.. code:: cpp

    #include <tuple>
    #include <vector>
    
    template <typename T1, typename T2, typename T3, typename T4>
    class GenericManager {
        public:
            typedef typename std::tuple<T1, T2, T3, T4> row_type;
            typedef std::vector<row_type> queryset_type;
        public:
            static void all(queryset_type& qs);
                       
    };
    
Y ya tengo un manager genérico ``GenericManager`` con el que puedo reutilizar el código, pero
sólo para tablas que tengan cuatro columnas, eso sí, éstas pueden ser de cualquier tipo.

Un poco más difícil es generalizar el número de columnas, hace un tiempo lo habría hecho
utilizando Boost.Preprocessor_, tengo algunos ejemplos de hace 10 años donde lo usaba, realmente
estoy orgulloso de haberme enfrentado a ese problema de esa forma en aquel momento; pero hoy
no es ése el camino que quiero seguir.

.. _Boost.Preprocessor: http://www.boost.org/doc/libs/1_60_0/libs/preprocessor/doc/index.html


El buen camino
--------------

Hay una solución mucho más elegante, las **variadic-templates**, con ellas
podemos generalizar de una manera tan maravillosa como ésta:

.. code:: cpp

    #include <tuple>
    #include <vector>
    
    template <typename... Args>
    class GenericManager {
        public:
            typedef typename std::tuple<Args...> row_type;
            typedef std::vector<row_type> queryset_type;
        public:
            static void all(queryset_type& qs);
                       
    };
    
¿No es fantástico? Con esta generalización puedo hacer cosas realmente útiles, puedo crear una clase
que se comporte realmente como un *manager* genérico y una clase *queryset* que implemente
una funcionalidad afín a la que está disponible en Django.

De momento estoy trabajando en ello, básicamente reuniendo respuestas de StackOverflow en un único
sitio y haciéndolas funcionar. Pronto un segundo post con detalles de implementación y ejemplos.
