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
##	9- Se implementan los asteroides oblicuos
##      10- Introducir planetas en segundo plano moviendose mas lentos para dar sensacion de desplazamiento
##
##      Pendientes:

##	11- Rutina de fin de juego con tabla de puntuaciones
##      12- Variar las tasas de aparicion de los asteroides y la velocidad de los mismos para hacer eljuego mas jugable,
##          con dificultad creciente 


import pygame, random, sys
from pygame.locals import *

INIT_ENERGY = 25
LASER_DURACION_MAX = 5
MEDIDA_NAVE = 50
PLANET_MOV_RATE = 30
NUM_MAX_PLANETAS = 11
PLANETMAXSIZE = 200
PLANETMINSIZE = 50
PLANETSPEED = 1
GIGANT_PLANET_RATE = 0.20


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
    imagenHumo_aEscala = pygame.transform.scale(imagenHumo[numAnimacion - 1], (MEDIDA_NAVE, MEDIDA_NAVE))
    
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
pygame.mixer.init()
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
sonidoLaser = pygame.mixer.Sound('sonidos/lazer.wav')

# set up images
imagenExplosion = []
imagenHumo = []
imagenPlaneta = []
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

imagenPlaneta.append(pygame.image.load('planetas/p1.png'))
imagenPlaneta.append(pygame.image.load('planetas/p2.png'))
imagenPlaneta.append(pygame.image.load('planetas/p3.png'))
imagenPlaneta.append(pygame.image.load('planetas/p4.png'))
imagenPlaneta.append(pygame.image.load('planetas/p5.png'))
imagenPlaneta.append(pygame.image.load('planetas/p6.png'))
imagenPlaneta.append(pygame.image.load('planetas/p7.png'))
imagenPlaneta.append(pygame.image.load('planetas/p8.png'))
imagenPlaneta.append(pygame.image.load('planetas/p9.png'))
imagenPlaneta.append(pygame.image.load('planetas/p10.png'))
imagenPlaneta.append(pygame.image.load('planetas/p11.png'))

imagenAsteroide = pygame.image.load('meteoritos/m1.png')
imagenAsteroideEnergetico = pygame.image.load('meteoritos/mx.png')
imagenFondo = pygame.image.load('Fondo/fondo.jpg').convert()
jugadorRect = imagenNaveCentro.get_rect()

#Redimensiono las imagenes de la nave
imagenNaveCentro_aEscala = pygame.transform.scale(imagenNaveCentro, (MEDIDA_NAVE, MEDIDA_NAVE))
imagenNaveIzquierda_aEscala = pygame.transform.scale(imagenNaveIzquierda, (MEDIDA_NAVE, MEDIDA_NAVE))
imagenNaveDerecha_aEscala = pygame.transform.scale(imagenNaveDerecha, (MEDIDA_NAVE, MEDIDA_NAVE))

imagenNaveCentroMotorOn_aEscala = pygame.transform.scale(imagenNaveCentroMotorOn, (MEDIDA_NAVE, MEDIDA_NAVE))
imagenNaveDerechaMotorOn_aEscala = pygame.transform.scale(imagenNaveDerechaMotorOn, (MEDIDA_NAVE, MEDIDA_NAVE))
imagenNaveIzquierdaMotorOn_aEscala = pygame.transform.scale(imagenNaveIzquierdaMotorOn, (MEDIDA_NAVE, MEDIDA_NAVE))

for i in range(0,5):
    imagenExplosion[i] = pygame.transform.scale(imagenExplosion[i], (MEDIDA_NAVE, MEDIDA_NAVE))

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
    planetas = []
    asteroidesDestruidos = []
    energia = INIT_ENERGY
    score = 0
    jugadorRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moverIzquierda = moverDerecha = moverAdelante = moverAtras = False
    contadorAsteroides = 0
    contadorPlanetas =  0 
    contadorMovPlanetas = 0
    contAnimacion = 0

    laser = {'disparado' : False,
             'origen': (0,0),
             'duracion': 0}

    # Posiciona los planetas
    i = 0
    for numPlaneta in range(0,7):
        i += 1
        posx = (i * 100)  % WINDOWWIDTH
        posy = ((i % 4) * 150)  % WINDOWHEIGHT
        
        if random.random() <= GIGANT_PLANET_RATE:
            tamano_Planeta = PLANETMAXSIZE
            speed = PLANETSPEED * 4     #Los planetas mas grandes estaran mas cerca y por tanto se moveran mas rapido
        else:
            tamano_Planeta = PLANETMINSIZE
            speed = PLANETSPEED
            
        imagen = pygame.transform.scale(imagenPlaneta[numPlaneta], (tamano_Planeta, tamano_Planeta))
        nuevoPlaneta = {'rect': pygame.Rect(posx, posy, tamano_Planeta, tamano_Planeta),
                    'speed': speed ,
                    'surface':imagen,
                    }
        planetas.append(nuevoPlaneta)
  
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
                        sonidoLaser.play()                     

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
                        'v_speed': random.randint(ASTEROIDMINSPEED, ASTEROIDMAXSPEED),
                        'h_speed': random.randint(-1 * ASTEROIDMAXSPEED, ASTEROIDMAXSPEED),
                        'surface':imagen,
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


        # Mueve los planetas
        contadorMovPlanetas += 1
        if contadorMovPlanetas == PLANET_MOV_RATE:
            contadorMovPlanetas = 0
            for p in planetas:
                p['rect'].move_ip(0, p['speed'])
            
        # Mueve a los asteroides 
        for a in asteroides:
            a['rect'].move_ip(a['h_speed'], a['v_speed'])

        # Pinta el fondo
        windowSurface.blit(imangenFondo, (0,0))
        
    
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

         # Dibuja los planetas
        for p in planetas:
            windowSurface.blit(p['surface'], p['rect'])

        # Dibuja el laser      
        if laser['disparado']:
            color_amarillo = (255,255,0)
            pygame.draw.rect(windowSurface, color_amarillo , (laser['origen'][0], laser['origen'][1], 5, -1 * 700))
            
            laser['duracion'] += 1
            if laser['duracion'] > LASER_DURACION_MAX:
                laser['disparado'] = False
           
        # Dibuja los asteroides
        for a in asteroides:
            windowSurface.blit(a['surface'], a['rect'])


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

        pygame.display.update()

        # Comprueba la colision de algun asteroide con el jugador
        hayChoque = jugadorChocaAsteroide(jugadorRect, asteroides)
        if hayChoque:
            if hayChoque == 'choque destructivo':
                sonidoExplosion.play()
                energia -= 10
                # Hace la explosion si la energia baja de 0
                if energia < 0:
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
