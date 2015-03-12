# Introduction #
Los puntos de desarrollo interesantes los pongo acá, los mas nuevos arriba

```
------------------------------------------------------------------------------------------

Milestone 1
rev 269 branch1

Enflaquecido main, reorganizado codigo, introducido servicios con duracion session

main ahora tiene solo la responsabilidades
	startup: inicializar systemas y servicios que estaran disponibles durante toda la session.
	lanzar la escenana inicial

Reorganizacion de codigo:
GameLayer y los compañeros de escena fueron a gamescene.py
Lo que es intro u outro fué a intro_outro.py
	

Servicios:
	Los servicios se llaman con
	import gg
	gg.services["s_xxxxxx"]()

donde s_xxxxxx es el nombre del servicio.

	Los servicios se registran durante el startup, en main, cuando se importa el modulo que declara el servicio.
	Los servicios se declaran asi:

	def xxxxxx():
	...

	
	# publish services
	import gg
	gg.services["s_xxxxxx"] = xxxxxx

Por una cuestion de sanidad se pide que sea valido llamar a cualquier servicio luego de terminar el starup.
Para no tener que registrar informacion de parametros, se pide que no admitan parametros.
En el codigo actual se usan para registrar creadores de instancias de escenas.
------------------------------------------------------------------------------------------
```