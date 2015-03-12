Basico:
  * terminar imagenes
  * poner skin nuevo
  * waypointing -> claudio. crea el grafo, encuentra el min path (en testbed).siguiendo
  * agregar familiares -> NicoEchaniz (lwcyphr)
  * hacer que los zombies y la gente se mueva con un pathfinding decente
  * ponerle energia
  * que cuando te toquen los zombies te saquen energia (lwcyphr)
  * que cuando alguien o un zombie se queda sin energia se muere (lwcyphr)
  * que cuando se queda sin energia el UserAgente de game over
  * que se pueda disparar (ricardo)
  * que los familiares puedan pegar con lo que tienen en la mano (lwcyphr)
  * que los disparos le saquen energia a los agentes
  * que se te acaben las balas
  * crear loader de zonas de spawn
  * cada tanto spawnear balas en una zona de spawn
  * que puedas levantar las balas y que se te recarguen las municiones
  * que puedas dar ordenes a tus familiares

AI:
  * que tus familiares ataquen decentemente
  * que los zombies vayan a lugares que hacen sentido -> claudio, leer mas abajo

COLLISION:
  * ~~correcta colisiones entre distintos shapes (ricardo)~~
  * ~~colisión de rayos para line-of-sight (ricardo)~~
  * colisión de balas para disparar (ricardo)

GAMEPLAY:
  * definir mapa de la casa segun jugabilidad
  * definir algoritmo de oleada de zombies -> claudio , ver mas abajo
  * definir danio de armas

PANTALLAS
  * menu ppal
  * perdiste

POLISH:
  * luces
  * caritas + mensajes
  * musica
  * sfx
  * cut-scenes


Cludio consulta:
IA , Navigation , boids , zombies , gameplay:

Zombies:
propondria de momento estados-comportamientos
> initial\_patrol : no queremos en general que el zombie se mande derecho; haria un paseito por afuera, digamos que solo te atacaria si estas cerca y/o afuera . tendria una lista de waypoints a seguir; cuando llega al ultimo pasa a modo seeker o al guardian
(nota: quizas generar un segundo grafo de navegacion para esta etapa, asi no hace entrada prematura)

> seeker: fija a un bueno como blanco. Podemos modular la seleccion de blanco, de modo que en determinados niveles los ataques se concentren en un actor en particular. si llega al seeker o pasa cerca de otro bueno, pasa a modo engaged


> guardian: patrulla en las cercanias de un spawn point de goodies, pasa a modo engaged si bueno se acerca a menos de determinada distancia

> engaged: ataca a matar o morir. se comunica con otros atacantes para no apilarse del mismo.


Estrategia de zombie spawn y gameplay:
Iria liberando de a grupitos (un pequeño swarm), posiblemente con objetivos compatibles.

minioleada: Soltar dos o tres de estos grupitos, no tan separados en el tiempo, con diferentes objetivos ( o al menos diferentes grupos de entrada )

El nivel es un intervalo fijo de tiempo (2-3 min), en el cual has varias minioleadas,
separadas por breves intervalos de tiempo.

En el cambio de nivel hay un intervalo de tranquilidad mayor, que permite prepararse (y quizas curar a los heridos ?)

Les parece si empiezo a tocar Zombies con esos objetivos en mente ?