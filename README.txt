Juego en pyGame para el curso de programacion avanzada en Python de la UGR

Se parte del juego "dodger" que aparece en el libro "Invent with Python" de AI Sweigart's , vease inventwithpython.com

Agradecimientos tambien a Timothy Downs por su implementacion del modulo inputbox

Los graficos y los sonidos estan extraidos de www.spriters-resource.com y de www.freesound.org respectivamente

SCREENCAST:
    
    http://youtu.be/sVeu33pNoNY

ARGUMENTO:

	Tu mision es dificil, conducir tu nave por el peligroso cinturon de asteroides de Aldebaran para 		recolectar la preciosa energia que hay escondidad dentro de los asteroides blancos.

	Armado solo con tus reflejos y tu laser tendras que intentar recolectar la maxima energia antes de 
	un minuto 

CONTROLES:
	Flechas para mover la nave, espacio para disparar el laser.

	El laser consume algo de la energia que recolectas.
	Cuanto mas energia tengas mas velocidad tendra tu nave
	
Lista de modificaciones sobre el juego original: 

	
	1- Introducido un fondo
	2- Introducido sonido ambiente
	3- Cambiados los sprites 
	4- Se anima el movimiento del personaje
	5- Se crea la animacion de la explosion
	6- Se crean los asteroides benevolos
	7- Se implementa la barra de energia 
		(aumenta al recolecar asteroides energeticos y disminuye al chocar con los
		asteroides malos o cuando activamos el laser), si llega a cero la nave explota, 
		cuanto mayor es la energia mayor la velocidad de la nave.
	8- Se implementa el laser
	9- Se implementan los asteroides oblicuos
        10- Introducir planetas en segundo plano moviendose mas lentos para dar sensacion de desplazamiento
	11- Rutina de fin de juego con tabla de puntuaciones
        12- Variar las tasas de aparicion de los asteroides y la velocidad de los mismos 
		para hacer el juego mas jugable, con dificultad creciente 


