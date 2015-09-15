Lingẅars: Desafíos y juegos
===========================

:date: 2015-09-15 19:00
:tags: lingwars, django, architecture, plugins
:slug: lingwars-games

Esta semana he estado entretenido creando una arquitectura web para que el grupo
de Lingẅars pueda publicar online juegos y desafíos de forma sencilla. Básicamente
el objetivo que perseguía era que se puediera crear un juego implementando un par
de funciones y que el sistema lo dotara automáticamente de presencia en la web,
registro de las respuestas de los jugadores y, además, de jugabilidad a través de
la línea de comandos (principalmente para pruebas).

Y con más o menos éxito, con muchos cambios y mejoras aún pendientes, el objetivo
creo que se ha cumplido y lo podéis ver funcionando en la `web <http://games.lingwars.com/>`__.
Como siempre, también tenéis disponible el `código fuente en Github <https://github.com/lingwars/lingwars-games>`__.

Arquitectura
------------
El proyecto está dividido en dos partes diferenciadas:

* el **núcleo** con el motor para ejecutar los juegos y la aplicación web,
* los **juegos** propiamente dichos.

Básicamente he propuesto una arquitectura donde los juegos se añaden como *plugins*
y podrían ser tanto clases aisladas como aplicaciones de Django que hicieran uso de
la base de datos. En la primera versión ya planteo un ejemplo ilustrativo de cada
una de estas opciones.

El **núcleo** está formado por la aplicación :code:`appweb.engine` que se encarga de
buscar juegos en los directorios indicados en la configuración:

.. code:: python

    LINGWARS_GAMES_DIRS = [
        os.path.join(BASE_DIR, '../games'),
    ]

Este motor buscará identificar juegos en las aplicaciones instaladas
(`ver <https://github.com/Lingwars/lingwars-games/blob/7e2a3b0cbad1ad3ce08d39e92d8299f4c627a9ea/appweb/engine/apps.py#L29-L47>`__):

.. code:: python

    # Registered apps
    app_games_module = []
    for app in apps.get_app_configs():
        if isinstance(app, GameConfig):
            app_games_module.append(app.module.__path__[0])
            log.debug(u"\t - %s: %s" % (app.name, app.verbose_name))
            id = app.name.rsplit('.', 1)[1]
            if game_model.objects.filter(id=id, available=True).exists():
                raise RuntimeError(u"A game with id '%s' already exists" % id)

            game = app.get_game()
            assert_game(game)

            obj, created = game_model.objects.get_or_create(id=str(id), defaults={'title': app.verbose_name, 'is_app': True})
            obj.available = True
            obj.is_app = True
            obj.author = getattr(game, 'author', None)
            obj.save()
            self.games[id] = game

...y también en los paquetes y archivos presentes en los directorios indicados
(`ver <https://github.com/Lingwars/lingwars-games/blob/7e2a3b0cbad1ad3ce08d39e92d8299f4c627a9ea/appweb/engine/apps.py#L52-L72>`__):

.. code:: python

    # Simple games, just a 'game.py' file inside dir
    for dir in getattr(settings, 'LINGWARS_GAMES_DIRS', []):
        for item in os.listdir(dir):
            current_path = os.path.abspath(os.path.join(dir, item))
            if current_path in app_games_module:
                #log.debug(u"\t%s already included as app-game" % current_path)
                pass
            else:
                try:
                    module = '%s.game' % (item)
                    game = import_string(module)
                    assert_game(game)
                    log.debug(u"\t - %s" % module)

                    obj, created = game_model.objects.get_or_create(id=str(item), defaults={'title': getattr(game, 'title', item), 'is_app': False})
                    obj.available = True
                    obj.is_app = False
                    obj.save()
                    self.games[item] = game
                except ImportError as e:
                    log.warn(u"\t - %s: does not contain a game object" % module)

En el primer caso las aplicaciones deberán ser instancias de una clase :code:`GameConfig` que debe proporcionar
una instancia del juego. En el segundo caso los juegos deben estar disponibles como un objeto llamado
:code:`game` en la raíz del paquete.

Para los dos casos se realiza una comprobación para cerciorarse de que el objeto devuelto
tiene una interfaz válida para jugar, es decir, implementa un código como este:

.. code-block:: python

    class MyAwesomeGame(GameBase):
        title = 'My Awesome Game'
        author = 'Me myself'
        description = "In this game you blablabla"

        def make_question(self, *args, **kwargs):
            question = {
                'query': "Question to the user",
                'options': ["list", "of", "answers",]
                }
            response = {
                'answer': <index of correct answer>,  # Esto debe ser el índice de la respuesta correcta en la lista.
                'info': "Some info to the user"
                }
            return question, response

        def score(self, response, user_answer):
            # Check the `user_answer`, it should be equal to response['answer']
            # :param:`response` contains the same data created in `make_question`
            u = user_answer.get('answer', None)
            try:
                u = int(u)
            except TypeError:
                return 0
            else:
                return 1 if u == response.get('answer') else 0

Resultados
----------
Con un trozo de código tan sencillo como éste, el sistema se encarga de añadir el juego
a la página principal, proponer una interfaz de juego (actualmente sólo para juegos de
tipo *multiple choice*), recoger estadísticas de uso y crear un ranking.

.. figure:: {filename}/images/lingwars_games-main_page.png
   :align: center
   :alt: Página principal

   En la página principal aparecen todos los juegos que no han sido desactivados en la
   interfaz de administración.

.. figure:: {filename}/images/lingwars_games-play.png
   :align: center
   :alt: Playing a game

   Cada juego dispone de tres pestañas: una de información que muestra el histórico de
   utilización del juego, otra donde se plantea el juego (esta) y una tercera que
   muestra la clasificación de los usuarios registrados que la han utilizado.


Confío en que pronto haya más desafíos y juegos, y de mucha más calidad que los que
he planteado como ejemplo. Pero mientras tanto:
`jugad, jugad y poneos a prueba <http://games.lingwars.com/>`__. ¡Aceptad el reto!
