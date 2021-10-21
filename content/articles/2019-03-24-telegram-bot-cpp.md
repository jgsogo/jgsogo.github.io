---
lang: es
title: Un bot de Telegram con C++
date: 2019-03-24
author: jgsogo
category: C++
tags: 
  - chatbot
  - c++
  - telegram
  - conan
---

Un punto de encuentro habitual entre la programación y la lingüística son los chatbots, 
se trata de aplicaciones que permiten interactuar con los usuarios a través de plataformas
como WhatsApp o Telegram. Para alguien como yo, con interés en ambos campos, éste es un
lugar habitaual al que vuelvo una y otra vez, y así ha sido, esta vez desde el mundo
del C++.

<!--more-->

Hasta ahora siempre había hecho los chatbots utilizando Python, así funcionan el que
planteamos para Neutrón o el que utilizo para enterarme de ofertas en Wallapop, los ejecuto en
mi Raspberry y siempre tengo acceso a ellos a través de mi teléfono. Una interfaz sencilla,
siempre disponible y que no requiere de ninguna configuración de red.

En el mundo del C++ todo parece más complicado, todo lo que se encuentra en torno al
lenguaje parece estar relacionado con librerías, con técnicas para modernizar el código,
pero muy pocas veces podemos leer sobre ejemplos de aplicaciones o pequeños prototipos
creados con él. Pero yo creo que el ecosistema está madurando, que el lenguaje ha
adquirido ciertas características que aumentan su expresividad y el ecosistema se ha
dotado de herramientas que hacen más accesible el sentarse delante del ordenador y
programar la parte que nos interesa sin preocuparnos por todo lo demás.

¡Vamos allá!


## Arquitectura de un chatbot

Un bot de Telegram (extensible a prácticamente cualquier otro bot) es una aplicación
conectada continuamente al sistema de mensajería de Telegram y que responde a
notificaciones procedentes del servidor de mensajes.

<article-image
    src="/img/2019/architecture.png"
    alt="Arquitectura de un bot de Telegram"
    caption="Diagrama explicativo con la arquitectura de un bot de telegram"></article-image>

Los usuarios individualmente podrán iniciar una conversación con el bot como si fuera
un usuario más y conversarán con él en su chat privado; por lo tanto, y esto lo
tendremos que tener en cuenta a la hora de programar, el bot debe ser capaz de mantener
un número arbitrario de conversaciones simultaneas, sabremos a cuál se refiere cada
mensaje porque irá acompañado de un identificador único.

Apoyándonos en librerías existentes, nuestra tarea se reduce únicamente a programar cuáles
son las respuestas del bot a cada uno de los mensajes que los usuarios pueden enviarnos.


## La librería tgbot-cpp

Para construir nuestro ejemplo utilizaremos la librería 
<content-github-repository repo="reo7sp/tgbot-cpp">`tgbot-cpp`</content-github-repository>
de <content-github-user user="reo7sp">Oleg Morozenkov</content-github-user>
que podemos encontrar en Github. No necesitamos entrar en la librería para utilizarla, es
más nos bastará con tener unos conocimientos muy básicos, incluso de C++, para poder
echar a andar nuestro bot.

La librería tiene algunas dependencias que necesitaremos tener en nuestro sistema
para poder compilarla, puedes utilizar diferentes estrategias para instalarlas en tu
ordenador, personalmente te recomiendo que utilices [`Conan`](https://conan.io),
pero siéntete libre de luchar contra los elementos utilizando las armas que 
consideres oportunas.

Si optas por Conan, simplemente tendrás que seguir los siguientes pasos:

```bash
pip install conan
conan profile show default
```

Si utilizas GCC, échale un ojo a este trozo de la documentación donde se habla de la
compatibilidad binaria: [How to manage the GCC>=5 ABI](https://docs.conan.io/en/latest/howtos/manage_gcc_abi.html),
probablemente quieras modificar la *libcxx* que Conan ha elegido por defecto.

Una vez instalado Conan, añade los repositorios remotos necesarios de donde se
descargarán las recetas:

```bash
conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan
conan remote add jgsogo https://api.bintray.com/conan/jgsogo/conan-packages
```

E instala la librería, así la tendremos disponible para próximos pasos:

```bash
conan install tgbot_cpp/1.1@jgsogo/stable --build=missing
```


## Ejemplo de bot, lo mínimo necesario

El mínimo ejemplo que podemos construir con un bot es uno que nos conteste siempre 
lo mismo, pero nos servirá de ejemplo para probar que todo funciona. Este ejemplo
es el que ya nos ofrece la documentación de su librería: un bot que responde con
un simple `"Hi!"` cuando nos conectamos a él y que después nos devuelve el mismo
mensaje que le hemos enviado:


```cpp[main.cpp]
#include <stdio.h>
#include <tgbot/tgbot.h>

int main() {
    // Initialize the bot
    TgBot::Bot bot("PLACE YOUR TOKEN HERE");

    // Connect to events and define actions using callbacks
    bot.getEvents().onCommand("start", [&bot](TgBot::Message::Ptr message) {
        bot.getApi().sendMessage(message->chat->id, "Hi!");
    });
    bot.getEvents().onAnyMessage([&bot](TgBot::Message::Ptr message) {
        printf("User wrote %s\n", message->text.c_str());
        if (StringTools::startsWith(message->text, "/start")) {
            return;
        }
        bot.getApi().sendMessage(message->chat->id, "Your message is: " + message->text);
    });

    // Run the infinite loop
    try {
        printf("Bot username: %s\n", bot.getApi().getMe()->username.c_str());
        TgBot::TgLongPoll longPoll(bot);
        while (true) {
            printf("Long poll started\n");
            longPoll.start();
        }
    } catch (TgBot::TgException& e) {
        printf("error: %s\n", e.what());
    }
    return 0;
}
```

En el código anterior hay tres partes diferenciadas:

* La construcción del bot, un objeto de la clase `TgBot::Bot` al que hay que pasarle
  un *token* (más adelante hablaremos de esto).
* Conectar nuestras acciones a los eventos generados por el bot, hay dos tipos de estos
  eventos:

  - los comandos, son aquellos que el usuario introduce precedidos por `/`
    (ejemplos típicos serían `/start` o `/help`), y
  - los mensajes de texto, todos ellos entrarán a través del evento `onAnyMessage`.

  Como se puede ver en el ejemplo, se están conectando unos *callbacks* a cada uno de los
  eventos anteriores, su implementación se corresponde con la que presentamos al introducir
  el ejemplo del bot.

* Ejecutar el bot utilizando un bucle infinito.


## Cómo compilarlo

Si provienes de Python o de otros lenguajes interpretados quizá esto te sorprenda, pero el
código de C++ hay que compilarlo, no basta con ejecutarlo como si fuera un *script*, no;
necesitamos generar el binario de la aplicación, el `.exe`, que será lo que ejecutemos.
En esto se basan los mayores logros y desencantos de este lenguaje.

Para compilarlo utilizaré [CMake](https://cmake.org/) y por lo tanto hará falta un fichero `CMakeLists.txt`
para nuestro proyecto:

```cmake[CMakeLists.txt]
cmake_minimum_required(VERSION 2.8.12)
project(BotHelloWorld CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(bot_hello_world main.cpp)
target_link_libraries(bot_hello_world ${CONAN_LIBS})
set_target_properties(bot_hello_world PROPERTIES CXX_STANDARD 11)
```

Mejor que copiar los *snippets* de código que aparecen aquí es que te clones el repositorio que
hemos preparado en el [grupo de usuarios de C++ de Madrid](https://madridccppug.github.io/meetups/)
con algunos ejemplos y que lo compiles desde allí:

```bash
git clone https://github.com/madridccppug/workshop-telegram-bot.git
cd workshop-telegram-bot/hello_world

mkdir build && cd build
conan install .. --build=missing
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .

./bin/bot_hello_world
```

### El token, tu bot

Si has llegado hasta aquí, habrás visto que el bot necesita un token para funcionar, y si has
echado un vistazo al código fuente también sabrás que en nuestros utilizamos la variable de 
entorno `MADRIDCCPPUG_BOT_TOKEN` para pasarle este token a nuestro bot.

Cada **token identifica a un bot diferente**, es la clave que permite que tu programa se
identifique contra los servidores de Telegram y que el intercambio de mensajes entre los usuarios
y tu bot llegue a tu aplicación en vez de hacerlo a cualquier otra. Conseguir un *token* es
muy sencillo, sólo tendrás que iniciar una conversación (utilizando Telegram) con el 
[BotFather](https://telegram.me/BotFather), el bot de Telegram que te permite dar de alta nuevos bots. 

<article-image
    src="/img/2019/botfather.png"
    alt="Logotipo BotFather"
    caption="The BotFather"></article-image>


## Otros bots de ejemplo

En el repositorio que te has clonado anteriormente tienes disponibles otros ejemplos de bots,
todos ellos se compilan y funcionan de la misma forma:

* `random_chat`: se trata de un bot que conecta dos a dos a los usuarios que están
  hablando con él en ese momento, tal y como hacía el [Chatroulette](https://es.wikipedia.org/wiki/Chatroulette)
  pero en formato conversacional.
* `wordnet_game`: este bot es un trivial de definiciones en inglés. El bot muestra una
  definición y ofrece cuatro palabras, sólo una de ellas se corresponde con la definición. 
  Para programar este juego he utilizado también la librería
  <content-github-repository repo="jardon-u/wordnet-blast">wordnet-blast</content-github-repository>
  que permite el acceso desde C++ a la base de datos de [WordNet](https://wordnet.princeton.edu/)
  de la cual, sin lugar a dudas, merece la pena hablar en otra ocasión.

___

## Notas y materiales

* Repositorio con ejemplos: <content-github-repository repo="madridccppug/workshop-telegram-bot">https://github.com/madridccppug/workshop-telegram-bot</content-github-repository>
* Diapositivas correspondientes a la presentación del 21 de marzo de 2019 en grupo
  de usuarios de C++ de Madrid: [https://docs.google.com/presentation/d/1B5pPftL06dW1k87M5eyMk-MwfkqXWhzXmXrN0kKP0dk/edit?usp=sharing](https://docs.google.com/presentation/d/1B5pPftL06dW1k87M5eyMk-MwfkqXWhzXmXrN0kKP0dk/edit?usp=sharing)
