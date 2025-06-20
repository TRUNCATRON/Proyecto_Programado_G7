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

#Funcion creacion de textos para pantallas
def mostrar_texto(texto, tamano, color, x, y, centrado=True):
    fuente = pygame.font.SysFont(None, tamano)
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(x, y)) if centrado else render.get_rect(topleft=(x, y))
    pantalla.blit(render, rect)
    return rect

#Funcion para obtener posicion x mas lejana de los obstaculos
def ultimo_obs(obstaculo):
    if not obstaculo:
        return 0
    return max([obs.x for obs in obstaculo])

#Muestra pantalla de inicio
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
                    return
                if boton_salida.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(30)

#Muestra pantalla final
def pantalla_fin(punt_final):
    while True:
        pantalla.fill(GRIS)
        mostrar_texto("Has Perdido", 80, ROJO, ANCHO // 2, ALTURA // 3)
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

#Funcion para generar obstaculos y alivianar a funcion juego()
def crear_obstaculos(obstaculos, spawn_piso, spawn_techo):
    spawn_piso += 1
    spawn_techo += 1

    if spawn_piso > random.randint(50, 100) and ANCHO - ultimo_obs(obstaculos) > DIST_MIN:
        obstaculos.append(pygame.Rect(ANCHO, PISO - 50, 35, 50))
        spawn_piso = 0

    if spawn_techo > random.randint(150, 260) and ANCHO - ultimo_obs(obstaculos) > DIST_MIN:
        obstaculos.append(pygame.Rect(ANCHO, TECHO, 35, 120))
        spawn_techo = 0

    return spawn_piso, spawn_techo

#Se crea funcion para actualizar el movimienro del carro
def actualizar_carro(carro_y, carro_vel_y, salto, carro_altura, agachado):
    #Gravcedad
    carro_vel_y += 1
    carro_y += carro_vel_y

    if carro_y >= PISO - carro_altura:
        carro_y = PISO - carro_altura
        salto = False
    if carro_y <= TECHO:
        carro_y = TECHO
        carro_vel_y = 0

    if agachado and not salto:
        altura_actual = carro_altura // 2
        y_actual = carro_y + carro_altura // 2
    else:
        altura_actual = carro_altura
        y_actual = carro_y

    return carro_y, carro_vel_y, salto, y_actual, altura_actual


#Funcion principal del juego
def juego():
    carro_ancho, carro_altura = 50, 50
    carro_x = 100
    carro_y = PISO - carro_altura
    carro_vel_y = 0
    salto = False
    agachado = False

    obstaculos = []
    obstaculo_ancho = 35
    obstaculo_vel = 8
    spawn_piso = 0
    spawn_techo = 0

#texto puntaje
    puntaje = 0
    tiempo_punt = 0
    letra_puntaje = pygame.font.SysFont(None, 50)

    corriendo = True
    while corriendo:
        clock.tick(FPS)
        pantalla.fill(BLANCO)

        #dibuja piso y techo
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


        # Llamar funcion para crear obstaculos
        spawn_piso, spawn_techo = crear_obstaculos(obstaculos, spawn_piso, spawn_techo)

        for obs in obstaculos:
            obs.x -= obstaculo_vel

            #Comprobacion de visibilidad de los osbtraculos
        obstaculos = [obs for obs in obstaculos if obs.x + obstaculo_ancho > 0]

        #Invocar funcion de movimiento de carro
        carro_y, carro_vel_y, salto, y_actual, altura_actual = actualizar_carro(carro_y, carro_vel_y, salto, carro_altura, agachado)

        rect_carro = pygame.Rect(carro_x, y_actual, carro_ancho, altura_actual)

        for obs in obstaculos:
            if rect_carro.colliderect(obs):
                corriendo = False

        pygame.draw.rect(pantalla, ROJO, (carro_x, y_actual, carro_ancho, altura_actual))
        for obs in obstaculos:
            pygame.draw.rect(pantalla, VERDE, obs)

        tiempo_punt += clock.get_time()
        if tiempo_punt >= 1000:
            puntaje += 15
            tiempo_punt = 0

        texto_puntaje = letra_puntaje.render(f"Puntaje actual: {puntaje}", True, VERDE)
        pantalla.blit(texto_puntaje, (10, 10))

        pygame.display.flip()

    pantalla_fin(puntaje)


pantalla_inicio()
juego()