import pygame, random, sys
from pygame.locals import *

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
TASA_ASTEROIDES_ENERGETICOS = 0.9

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
            
# Devuelve falso si no hay choque o una cadena informativa si lo hay.
# si el choque es energertico elemina el asteroide
def jugadorChocaAsteroide(jugadorRect, asteroides):
    for a in asteroides[:]:
        if jugadorRect.colliderect(a['rect']) and a['energetico'] == True:
            asteroides.remove(a)
            return 'choque energetico'
        elif jugadorRect.colliderect(a['rect']):
            return 'choque destructivo'
        
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def animaExplosion():

    intervalo = 100

    for i in range(1,6):
        windowSurface.blit(imagenExplosion[i], jugadorRect)
        pygame.time.wait(intervalo)
        pygame.display.update()
   
  
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
    score = 0
    jugadorRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moverIzquierda = moverDerecha = moverAdelante = moverAtras = False
    contadorAsteroides = 0
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
            esEnergetico = (random.random() > TASA_ASTEROIDES_ENERGETICOS)
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
        if moverIzquierda and jugadorRect.left > 0:
            jugadorRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moverDerecha and jugadorRect.right < WINDOWWIDTH:
            jugadorRect.move_ip(PLAYERMOVERATE, 0)
        if moverAdelante and jugadorRect.top > 0:
            jugadorRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moverAtras and jugadorRect.bottom < WINDOWHEIGHT:
            jugadorRect.move_ip(0, PLAYERMOVERATE)

        # Mueve a los asteroides hacia abajo
        for a in asteroides:
            a['rect'].move_ip(0, a['speed'])
           

         # Elimina los asteroides que han caido al fondo de la pantalla
        for a in asteroides[:]:
            if a['rect'].top > WINDOWHEIGHT:
                asteroides.remove(a)

        # Pinta el fondo
        windowSurface.blit(imangenFondo, (0,0))

        # Pone las puntuaciones
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

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
                # Hace la explosion
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
                

        mainClock.tick(FPS)

        

    # Para el juego y muestra la pantalla de Game Over
    backGroundSound.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 6), (WINDOWHEIGHT / 3))
    drawText('Pulsa una tecla para volver a jugar', font, windowSurface, (WINDOWWIDTH / 6) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
