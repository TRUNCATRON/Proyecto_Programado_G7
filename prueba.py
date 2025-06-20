import pygame
import sys
import random

pygame.init()

ANCHO, ALTURA = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTURA))
pygame.display.set_caption("Wagon Wild")

clock = pygame.time.Clock()
FPS = 60

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 0, 0)
VERDE = (0, 200, 0)
GRIS = (180, 180, 180)
PISO = ALTURA - 50
TECHO = 195
DIST_MIN = 150


def mostrar_texto(texto, tamano, color, x, y, centrado=True):
    fuente = pygame.font.SysFont(None, tamano)
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(x, y)) if centrado else render.get_rect(topleft=(x, y))
    pantalla.blit(render, rect)
    return rect

def ultimo_obs(obstaculo):
    if not obstaculo:
        return 0 
    return max([obs.x for obs in obstaculo])


def pantalla_inicio():
    while True:
        pantalla.fill(GRIS)
        mostrar_texto("Wagon Wild", 80, NEGRO, ANCHO // 2, ALTURA // 3)

        boton_inicio = mostrar_texto("Inicio", 50, ROJO, ANCHO // 2, ALTURA // 2)
        boton_salida = mostrar_texto("Salir", 40, ROJO, ANCHO // 2, ALTURA // 2 + 70)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_inicio.collidepoint(evento.pos):
                    return  # Inicia juego
                if boton_salida.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(30)

def pantalla_fin(punt_final):
    while True:
        pantalla.fill(GRIS)
        mostrar_texto("Has Perdido", 80, ROJO, ANCHO // 2, ALTURA // 3)
        #muestra puntaje a la hora de chocar
        mostrar_texto(f"Su puntaje fue: {punt_final}", 30, VERDE, ANCHO // 2, ALTURA // 2 - 20) 

        boton_reiniciar = mostrar_texto("Reiniciar", 40, NEGRO, ANCHO // 2, ALTURA // 2 + 20)
        boton_salir = mostrar_texto("Salir", 40, NEGRO, ANCHO // 2, ALTURA // 2 + 80)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reiniciar.collidepoint(evento.pos):
                    juego()
                if boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(30)

def juego():
    carro_ancho, carro_altura = 50, 50
    carro_x = 100
    carro_y = PISO - carro_altura
    carro_vel_y = 0
    salto = False
    gravedad = 1
    agachado = False

    obstaculos = []
    obstaculo_ancho = 35
    obstaculo_alto = 50
    obstaculo_techo_ancho = 35
    obstaculo_techo_alto = 120
    obstaculo_vel = 8
    spawn_piso = 0
    spawn_techo = 0

    #cosas para texto de puntaje
    puntaje = 0
    tiempo_punt = 0
    letra_puntaje = pygame.font.SysFont(None, 50) 

    running = True
    while running:
        clock.tick(FPS)
        pantalla.fill(BLANCO)

        # Dibujo techo y piso
        pygame.draw.line(pantalla, NEGRO, (0, PISO), (ANCHO, PISO), 2)
        pygame.draw.line(pantalla, NEGRO, (0, TECHO), (ANCHO, TECHO), 2)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if ((evento.key == pygame.K_SPACE) or (evento.key == pygame.K_UP) or (evento.key == pygame.K_w)) and not salto:
                    carro_vel_y = -15
                    salto = True
                if (evento.key == pygame.K_DOWN) or (evento.key == pygame.K_s):
                    agachado = True
            if evento.type == pygame.KEYUP:
                if (evento.key == pygame.K_DOWN) or (evento.key == pygame.K_s):
                    agachado = False

        carro_vel_y += gravedad
        carro_y += carro_vel_y

        #Evitar que carro sobrepase el piso
        if carro_y >= PISO - carro_altura:
            carro_y = PISO - carro_altura
            salto = False

        #Evitar que el carro sobrepase el techo
        if carro_y <= TECHO:
            carro_y = TECHO
            carro_vel_y = 0

        # Crear obstaculso piso
        spawn_piso += 1
        if spawn_piso > random.randint(50, 100):
            if ANCHO - ultimo_obs(obstaculos) > DIST_MIN:
                nuevo_obs_piso = pygame.Rect(ANCHO, PISO - obstaculo_alto, obstaculo_ancho, obstaculo_alto)
                obstaculos.append(nuevo_obs_piso)
                spawn_piso = 0

        # Crear obstaculos techo
        spawn_techo += 1
        if spawn_techo > random.randint(150, 260):
            if ANCHO - ultimo_obs(obstaculos) > DIST_MIN:
                nuevo_obs_techo = pygame.Rect(ANCHO, TECHO, obstaculo_techo_ancho, obstaculo_techo_alto)
                obstaculos.append(nuevo_obs_techo)
                spawn_techo = 0

        # Mover obstaculos
        for obs in obstaculos:
            obs.x -= obstaculo_vel

        # Eliminar obstaculos fuera de pantalla
        obstaculos = [obs for obs in obstaculos if obs.x + obstaculo_ancho > 0]

        if agachado and not salto:
            altura_actual = carro_altura // 2
            y_actual = carro_y + carro_altura // 2
        else:
            altura_actual = carro_altura
            y_actual = carro_y

        rect_carro = pygame.Rect(carro_x, y_actual, carro_ancho, altura_actual)

         # Col. obstaculos
        for obs in obstaculos:
            if rect_carro.colliderect(obs):
                running = False

         # Se dibuja 'carrito' y obstacsulos
        pygame.draw.rect(pantalla, ROJO, (carro_x, y_actual, carro_ancho, altura_actual))
        for obs in obstaculos:
            pygame.draw.rect(pantalla, VERDE, obs)

        tiempo_punt += clock.get_time()
        if tiempo_punt >= 1000:
            puntaje += 15
            tiempo_punt = 0

        texto_puntaje =letra_puntaje.render(f"Puntaje actual: {puntaje}", True, VERDE)
        pantalla.blit(texto_puntaje, (10, 10))

        pygame.display.flip()

    #mostrar pant fin de juego
    pantalla_fin(puntaje)

#incio juego desde menuy
pantalla_inicio()
juego()