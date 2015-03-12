
```
<pre>
Me quedé con las ganas de hacer algunas cosas, asi que le pregunté a Lucio si podría hacer un branch.
Dijo que sí, asi que le doy.

Esta pagina en particular dá una vista desde lo alto, sin detalles, de temas que pueden interesarme. Lo que está marcado con '+' ya lo hice, lo que está con w es lo que estoy viendo.

Arranco con branch1 ; si necesito mas serán con sufixes (branch1_1...)
 
Metanle un pipe a trash en el correo si las notificaciones de codesite joden.

En milestones voy poniendo los cambios que voy haciendo. 
 
Areas  de Trabajo:
(el orden es aleatorio)
 
Away of problems:
+	main.py muy gordo
w       GameLayer muy gordo

Toward Features:
         Zombies eyes:
              quedaria un buen efecto si los ojos de los zombies fueran luminosos.
              posiblemente la forma mas facil de implementar seria si despues de rendir iluminacion
               se hace otra pasada rindiendo ojos ( usando un offset pos= R*rotation respecto de c/zombi)
         Zombi behavoir:
              Ampliar estados para facilitar la modulacion del gameplay.
              Quizas colaborar con Swarm.

 ScriptDirector:

        Responsabilidad:
               secuencia el gameplay
               (posiblemente) despache gameplay events
               (quizas) proporciona al editor info acerca de que eventos hay disponibles
        Descripcion Inicial:
                Tomaria un file de text simple de la forma
                 <line>=<time> <event_name> <event_params>
                Ej: 1.00 spawn_zombie_at  122,123, visual_variant,...
  
                Cuando llega el tiempo pedido llama al class method registrado para name con el
                 string de todos los params ( o una lista ...), que tipicamente seria de la form
                .CreateInstance(...) o SpawnInstance(...
                Hay que evitar que ScriptDirector se convierta en otro kitchen sink, por eso hay que
                encontrar la forma de autoregistrar / escanear. Algo onda como se declaran los
                EventHandlers ?   

 Swarms:

        considerar si spawnear zombies o mini-swarms
 
 User Friendly:
          pantalla de presentacion comandos help; quizas popup help ingame.
          pause command ?
 
 Navigation:
          Aca hay mucho por explorar, posiblemente solo me dedique a algunas de ellas.
          Mejorar el arbol inicial (en paralelo con IA para no desarrollar al pepe)
           agregar a cada wpt el radio libre
           tipos de waypoints, para indicar situacion especial ( hint navegacion dificil,
           valor estrategico abertura ... ) No mas de tres, incluyendo el comun.
           ser mas selectivo al agregar arcos, seguramente ahora hay exceso
           Luego de entrarlos todos hacer un prune del grafo para reducir el nro de datos
           que debe procesar la IA
           Analizar grafo + geometria para obtener puntos estrategicos
           Analizar grafo + geometria para obtener rutas, rutas alternativas, rutas colaborativas,
           zonas de crowding, cobertura...
 
 Parientes:
  Darles mas iniciativa propia.
  Estudiar si hay mas actividades que puedan hacer

  Ayuda Dev:
            Hacer el startup mas rapido en modo dev
           el agregado de musica me parece que alargó bastante; meterlo en un condicional
           load/save de grafo precompilado de navegacion (tarda en generarse y va a tardar mas)
          Facilitar el setup de una situacion de testeo:
           load_freeze, save_freeze: si fuese facil
           si lo anterior ademas es rapido y compacto; secuencia automatica de freezes, digamos
           1 por segundo, solo los ultimos 10 segundos.
          Zoom y no lights elegibles en modo dev
 

Gameplay Decisions:
Parientes: Ahora aportan poco al juego, por un lado porque se vienen tantos zombies que no hay tiempo de hacer nada ( esto se soluciona con ScriptDirector tweekeando el script)
  
  Un problema de la idea actual es que al recibir notificacion de evento interesante ( parpadeo en el hud) hay que escrollear mucho. Probar usar teclas para hacer switch al POV del pariente, por ejemplo 'space'-> father , 1..3-> otros. El pariente seguiria necesitando IA, pero las ordenes las dariamos desde el POV del pariente.
 Si lo anterior no vá, agregar alguna pista de en que direccion esta el pariente.

 Size: quizas un poco apretado; considerar si mapa mas grande visto desde mas arriba. da mas espacio para planear (desde el punto de vista del jugador humano). No mucho, si no no se aprecia el arte.

 fisica: el player pawn parece engancharse mucho (macetas por ejemplo). Experimentar.

</pre>
```