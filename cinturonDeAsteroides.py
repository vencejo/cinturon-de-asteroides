##Juego en pyGame para el curso de programacion avanzada en Python de la UGR
##
##Se parte del juego "dodger" que aparece en el libro "Invent with Python"
##de AI Sweigart's , vease inventwithpython.com
##
##Los graficos y los sonidos estan extraidos de www.spriters-resource.com y de
##www.freesound.org respectivamente

##Lista de modificaciones sobre el juego original: 
##
##	1- Introducido un fondo
##	2- Introducido sonido ambiente
##	3- Cambiados los sprites 
##	4- Se anima el movimiento del personaje
##	5- Se crea la animacion de la explosion
##	6- Se crean los asteroides benevolos
##	7- Se implementa la barra de energia (aumenta al recolecar asteroides energeticos y disminuye al chocar con los
##		asteroides malos o cuando activamos el laser), si llega a cero la nave explota, 
##		cuanto mayor es la energia mayor la velocidad de la nave.
##
##	8- Se implementa el laser

##      Pendientes:

##	9- Se implementan los asteroides oblicuos
##
##	10- Rutina de fin de juego con tabla de puntuaciones
##
##      11- Introducir planetas en segundo plano moviendose mas lentos para dar sensacion de desplazamiento
##
##      12- Variar las tasas de aparcion de los asteroides y la velocidad de los mismos para hacer eljuego mas jugable,
##          con dificultad creciente 


import pygame, random, sys
from pygame.locals import *

INIT_ENERGY = 25

LASER_DURACION_MAX = 5

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
DISPLAYMODE = (600,600)
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
ASTEROIDMINSIZE = 10
ASTEROIDMAXSIZE = 40
ASTEROIDMINSPEED = 1
ASTEROIDMAXSPEED = 8
ADDNEW_ASTEROID_RATE = 6
PLAYERMOVERATE = 5
TASA_ASTEROIDES_ENERGETICOS = 0.1

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Al pulsar la tecla esc se sale del juego
                    terminate()
                return
            
def jugadorChocaAsteroide(jugadorRect, asteroides):
    """Devuelve falso si no hay choque o una cadena informativa si lo hay 
    si el choque es energertico elemina el asteroide"""
    for a in asteroides[:]:
        if jugadorRect.colliderect(a['rect']) and a['energetico'] == True:
            asteroides.remove(a)
            return 'choque energetico'
        elif jugadorRect.colliderect(a['rect']):
            asteroides.remove(a)
            return 'choque destructivo'
        
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def animaExplosion():
    """ Anima los sprites que componen la explosion """
    intervalo = 100

    for i in range(1,6):
        windowSurface.blit(imagenExplosion[i], jugadorRect)
        pygame.time.wait(intervalo)
        pygame.display.update()


def anima_explosion_asteroides(asteroidesDestruidos, numAnimacion):
    """ Cada vez que se llama a esta funcion hace un paso de la animacion """

    #Redimensiono la imagen
    medida = 50
    imagenHumo_aEscala = pygame.transform.scale(imagenHumo[numAnimacion - 1], (medida, medida))
    
    #La muestro en pantalla
    for a in asteroidesDestruidos:
        windowSurface.blit(imagenHumo_aEscala, a['rect'])
        

def muestraBarraEnergia(energia):
    """ Dibuja una barra de energia vertical coloreada. Tonos rojos para poca energia y verdes para energias altas """
    nivel_rojo = 255 - energia
    if nivel_rojo < 0:
        nivel_rojo = 0
        
    nivel_verde = energia
    if nivel_verde > 255:
        nivel_verde = 255
    
    color = (nivel_rojo,nivel_verde,0)
    
    pygame.draw.rect(windowSurface, color , (560, 560, 20, -1 * energia))
   
  
# set up pygame
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Cinturon de asteroides')


# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
sonidoMotorsOn = pygame.mixer.Sound('sonidos/motores encendidos.wav')
sonidoExplosion = pygame.mixer.Sound('sonidos/explosion.wav')
sonidoPickup = pygame.mixer.Sound('sonidos/pickup.wav')
gameOverSound = pygame.mixer.Sound('sonidos/gameover.wav')
backGroundSound = pygame.mixer.Sound('sonidos/musica de fondo.wav')

# set up images
imagenExplosion = []
imagenHumo = []
imagenNaveCentro = pygame.image.load('nave/nave_centro.png')
imagenNaveCentroMotorOn = pygame.image.load('nave/nave_centro_motor_on.png')
imagenNaveIzquierda = pygame.image.load('nave/nave_izquierda.png')
imagenNaveIzquierdaMotorOn = pygame.image.load('nave/nave_izquierda_motor_on.png')
imagenNaveDerecha = pygame.image.load('nave/nave_derecha.png')
imagenNaveDerechaMotorOn = pygame.image.load('nave/nave_derecha_motor_on.png')
imagenExplosion.append(pygame.image.load('explosion/explosion1.png'))
imagenExplosion.append(pygame.image.load('explosion/explosion2.png'))
imagenExplosion.append(pygame.image.load('explosion/explosion3.png'))
imagenExplosion.append(pygame.image.load('explosion/explosion4.png'))
imagenExplosion.append(pygame.image.load('explosion/explosion5.png'))
imagenExplosion.append(pygame.image.load('explosion/explosion6.png'))

imagenHumo.append(pygame.image.load('humo/smoke_puff_0001.png'))
imagenHumo.append(pygame.image.load('humo/smoke_puff_0002.png'))
imagenHumo.append(pygame.image.load('humo/smoke_puff_0003.png'))
imagenHumo.append(pygame.image.load('humo/smoke_puff_0004.png'))
imagenHumo.append(pygame.image.load('humo/smoke_puff_0005.png'))
imagenHumo.append(pygame.image.load('humo/smoke_puff_0006.png'))

imagenAsteroide = pygame.image.load('meteoritos/m1.png')
imagenAsteroideEnergetico = pygame.image.load('meteoritos/mx.png')
imagenFondo = pygame.image.load('Fondo/fondo.jpg').convert()
jugadorRect = imagenNaveCentro.get_rect()

#Redimensiono las imagenes de la nave
medida = 50
imagenNaveCentro_aEscala = pygame.transform.scale(imagenNaveCentro, (medida, medida))
imagenNaveIzquierda_aEscala = pygame.transform.scale(imagenNaveIzquierda, (medida, medida))
imagenNaveDerecha_aEscala = pygame.transform.scale(imagenNaveDerecha, (medida, medida))

imagenNaveCentroMotorOn_aEscala = pygame.transform.scale(imagenNaveCentroMotorOn, (medida, medida))
imagenNaveDerechaMotorOn_aEscala = pygame.transform.scale(imagenNaveDerechaMotorOn, (medida, medida))
imagenNaveIzquierdaMotorOn_aEscala = pygame.transform.scale(imagenNaveIzquierdaMotorOn, (medida, medida))

for i in range(0,5):
    imagenExplosion[i] = pygame.transform.scale(imagenExplosion[i], (medida, medida))

# set up background
imangenFondo = pygame.transform.scale(imagenFondo, DISPLAYMODE)
windowSurface.blit(imangenFondo, (0,0))

# Muestra la pantalla de bienvenida
drawText('Cinturon de Asteroides', font, windowSurface, (WINDOWWIDTH / 10), (WINDOWHEIGHT / 3))
drawText('Pulse una tecla para empezar', font, windowSurface, (WINDOWWIDTH / 10) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    #Inicializa el juego
    asteroides = []
    asteroidesDestruidos = []
    contAnimacion = 0
    energia = INIT_ENERGY
    score = 0
    jugadorRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moverIzquierda = moverDerecha = moverAdelante = moverAtras = False
    contadorAsteroides = 0

    laser = {'disparado' : False,
             'origen': (0,0),
             'duracion': 0}
  
    backGroundSound.play()

    while True: 
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    moverDerecha = False
                    moverIzquierda = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moverIzquierda = False
                    moverDerecha = True
                if event.key == K_UP or event.key == ord('w'):
                    moverAtras = False
                    moverAdelante = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moverAdelante = False
                    moverAtras = True
                if event.key == K_SPACE:
                    if energia > 5:
                        energia -= 3
                        laser['disparado'] = True
                        laser['origen'] = (jugadorRect.left + 25,jugadorRect.top)
                        laser['duracion'] = 0

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT or event.key == ord('a'):
                    moverIzquierda = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moverDerecha = False
                if event.key == K_UP or event.key == ord('w'):
                    moverAdelante = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moverAtras = False

        # Pone mas asteroides en la parte alta de la pantalla si son necesarios       
        contadorAsteroides += 1
        if contadorAsteroides == ADDNEW_ASTEROID_RATE:
            contadorAsteroides = 0
            tamano_asteroide = random.randint(ASTEROIDMINSIZE, ASTEROIDMAXSIZE)
            esEnergetico = (random.random() > 1 - TASA_ASTEROIDES_ENERGETICOS)
            if esEnergetico:
                imagen = pygame.transform.scale(imagenAsteroideEnergetico, (tamano_asteroide, tamano_asteroide))
            else:
                imagen = pygame.transform.scale(imagenAsteroide, (tamano_asteroide, tamano_asteroide))
                
            nuevoAsteroide = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-tamano_asteroide), 0 - tamano_asteroide, tamano_asteroide, tamano_asteroide),
                        'speed': random.randint(ASTEROIDMINSPEED, ASTEROIDMAXSPEED),
                        'surface':imagen,
                        'animationTime': random.random(),
                        'energetico': esEnergetico,
                        }
            asteroides.append(nuevoAsteroide)

        # Mueve al jugador
        energy_factor = energia / INIT_ENERGY
        vel_jugador =  PLAYERMOVERATE + energy_factor
        if moverIzquierda and jugadorRect.left > 0:
            jugadorRect.move_ip(-1 * vel_jugador , 0)
        if moverDerecha and jugadorRect.right < WINDOWWIDTH:
            jugadorRect.move_ip(vel_jugador, 0)
        if moverAdelante and jugadorRect.top > 0:
            jugadorRect.move_ip(0, -1 * vel_jugador)
        if moverAtras and jugadorRect.bottom < WINDOWHEIGHT:
            jugadorRect.move_ip(0, vel_jugador)

        # Mueve a los asteroides hacia abajo
        for a in asteroides:
            a['rect'].move_ip(0, a['speed'])


        # Pinta el fondo
        windowSurface.blit(imangenFondo, (0,0))
        
        # Dibuja el laser      
        if laser['disparado']:

            color_blanco = (255,255,255)
            pygame.draw.rect(windowSurface, color_blanco , (laser['origen'][0], laser['origen'][1], 5, -1 * 700))
            
            laser['duracion'] += 1
            if laser['duracion'] > LASER_DURACION_MAX:
                laser['disparado'] = False

        
         # Elimina los asteroides que han caido al fondo de la pantalla y los que son alcanzados por el laser
        for a in asteroides[:]:
            if a['rect'].top > WINDOWHEIGHT:
                asteroides.remove(a)
            if laser['disparado'] and (a['rect'].top < laser['origen'][1]) and (a['rect'].left < laser['origen'][0] + 25) and (a['rect'].left > laser['origen'][0] - 25):
                asteroides.remove(a)
                asteroidesDestruidos.append(a)

        # Anima la explosion de los asteroides destruidos
        if len(asteroidesDestruidos) > 0:
            contAnimacion += 1
            if contAnimacion > 6:
                asteroidesDestruidos = []
                contAnimacion = 0
            else:
                anima_explosion_asteroides(asteroidesDestruidos, contAnimacion)

        # Pone las puntuaciones
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('Energy: %s' % (energia), font, windowSurface, 10, 550)
        muestraBarraEnergia(energia)

        # Pinta la nave y le da sonido a los motores si va hacia adelante
        if moverDerecha:
            if moverAdelante:
                windowSurface.blit(imagenNaveDerechaMotorOn_aEscala, jugadorRect)
                sonidoMotorsOn.play()
            else:   
                windowSurface.blit(imagenNaveDerecha_aEscala, jugadorRect)
                sonidoMotorsOn.stop()
                
        elif moverIzquierda:
            if moverAdelante:
                windowSurface.blit(imagenNaveIzquierdaMotorOn_aEscala, jugadorRect)
                sonidoMotorsOn.play()
            else:   
                windowSurface.blit(imagenNaveIzquierda_aEscala, jugadorRect)
                sonidoMotorsOn.stop()
        else:
            if moverAdelante:
                windowSurface.blit(imagenNaveCentroMotorOn_aEscala, jugadorRect)
                sonidoMotorsOn.play()
            else:
                windowSurface.blit(imagenNaveCentro_aEscala, jugadorRect)
                sonidoMotorsOn.stop()

           
        # Dibuja los asteroides
        for a in asteroides:
            windowSurface.blit(a['surface'], a['rect'])

        pygame.display.update()

        # Comprueba la colision de algun asteroide con el jugador
        hayChoque = jugadorChocaAsteroide(jugadorRect, asteroides)
        if hayChoque:
            if hayChoque == 'choque destructivo':

                energia -= 10
                # Hace la explosion si la energia baja de 0
                if energia < 0:
                    sonidoExplosion.play()
                    animaExplosion()
                    pygame.time.wait(2000)
                    sonidoExplosion.stop()
                    if score > topScore:
                        topScore = score 
                    break
            else:
                # Suma puntos
                score += 10
                sonidoPickup.play()
                energia += 10

        mainClock.tick(FPS)

        

    # Para el juego y muestra la pantalla de Game Over
    backGroundSound.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 6), (WINDOWHEIGHT / 3))
    drawText('Pulsa una tecla para volver a jugar', font, windowSurface, (WINDOWWIDTH / 6) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
