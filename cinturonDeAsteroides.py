import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
ASTEROIDMINSIZE = 10
ASTEROIDMAXSIZE = 40
ASTEROIDMINSPEED = 1
ASTEROIDMAXSPEED = 8
ADDNEW_ASTEROID_RATE = 6
PLAYERMOVERATE = 5

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

def playerHasHitAsteroid(jugadorRect, asteroides):
    for a in asteroides:
        if jugadorRect.colliderect(a['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Cinturon de asteroides')


# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
motorsOn = pygame.mixer.Sound('sonidos/motores encendidos.wav')
explosion = pygame.mixer.Sound('sonidos/explosion.wav')
energyUp = pygame.mixer.Sound('sonidos/energy up.wav')
gameOverSound = pygame.mixer.Sound('sonidos/gameover.wav')
backGroundSound = pygame.mixer.Sound('sonidos/musica de fondo.wav')

# set up images
imagenNaveCentro = pygame.image.load('nave/nave_centro.png')
imagenNaveCentroMotorOn = pygame.image.load('nave/nave_centro_motor_on.png')
imagenNaveIzquierda = pygame.image.load('nave/nave_izquierda.png')
imagenNaveIzquierdaMotorOn = pygame.image.load('nave/nave_izquierda_motor_on.png')
imagenNaveDerecha = pygame.image.load('nave/nave_derecha.png')
imagenNaveDerechaMotorOn = pygame.image.load('nave/nave_derecha_motor_on.png')
jugadorRect = imagenNaveCentro.get_rect()
imagenAsteroide = pygame.image.load('meteoritos/m1.png')

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
        score += 1 

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
            nuevoAsteroide = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-tamano_asteroide), 0 - tamano_asteroide, tamano_asteroide, tamano_asteroide),
                        'speed': random.randint(ASTEROIDMINSPEED, ASTEROIDMAXSPEED),
                        'surface':pygame.transform.scale(imagenAsteroide, (tamano_asteroide, tamano_asteroide)),
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
        windowSurface.fill(BACKGROUNDCOLOR)

        # Pone las puntuaciones
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Pinta la nave y le da sonido a los motores si va hacia adelante
        if moverDerecha:
            if moverAdelante:
                windowSurface.blit(imagenNaveDerechaMotorOn, jugadorRect)
                motorsOn.play()
            else:   
                windowSurface.blit(imagenNaveDerecha, jugadorRect)
                motorsOn.stop()
                
        elif moverIzquierda:
            if moverAdelante:
                windowSurface.blit(imagenNaveIzquierdaMotorOn, jugadorRect)
                motorsOn.play()
            else:   
                windowSurface.blit(imagenNaveIzquierda, jugadorRect)
                motorsOn.stop()
        else:
            if moverAdelante:
                windowSurface.blit(imagenNaveCentroMotorOn, jugadorRect)
                motorsOn.play()
            else:   
                windowSurface.blit(imagenNaveCentro, jugadorRect)
                motorsOn.stop()
            

        # Dibuja los asteroides
        for a in asteroides:
            windowSurface.blit(a['surface'], a['rect'])

        pygame.display.update()

        # Comprueba la colision de algun asteroide con el jugador
        if playerHasHitAsteroid(jugadorRect, asteroides):
            if score > topScore:
                topScore = score 
            break

        mainClock.tick(FPS)

    # Para el juego y muestra la pantalla de Game Over
    backGroundSound.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 6), (WINDOWHEIGHT / 3))
    drawText('Pulsa una tecla para volver a jugar', font, windowSurface, (WINDOWWIDTH / 6) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
