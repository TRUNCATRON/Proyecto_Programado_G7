import pygame
import sys
import random


pygame.init()

ANCHO, ALTURA = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTURA))
pygame.display.set_caption("Wagon Wild")
fondo_imagen = pygame.image.load("imagenes/img_juego/fondo juego.png")
piedra_techo = pygame.image.load("imagenes/img_juego/estalactita.png")
piedra_piso = pygame.image.load("imagenes/img_juego/estalagmita.png")
carrito = pygame.image.load("imagenes/img_juego/carrito.png")
carrito_agachado = pygame.image.load("imagenes/img_juego/carrito_agachado.png")

#Escala
piedra_techo = pygame.transform.scale(piedra_techo, (30,120))
piedra_piso = pygame.transform.scale(piedra_piso,(40,50))
carrito = pygame.transform.scale_by(carrito, 0.39)
carrito_agachado = pygame.transform.scale_by(carrito_agachado, 0.39)

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

#Funcion para que fondo se vaya moviendo
def agregar_fondo(fondo, x, velocidad):
    pantalla.blit(fondo, (x, 0))
    pantalla.blit(fondo, (x + ANCHO, 0))
    x -= velocidad
    if x <= -ANCHO:
        x=0
    return x


#Muestra pantalla de inicio

#Muestra pantalla final
def pantalla_fin(punt_final):
    while True:
        pantalla.fill(GRIS)
        mostrar_texto("Has Perdido", 80, ROJO, ANCHO // 2, ALTURA // 3)
        mostrar_texto(f"Su puntaje fue: {punt_final}", 30, NEGRO, ANCHO // 2, ALTURA // 2 - 20)

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

    if spawn_piso > random.randint(50, 100) and ANCHO - ultimo_obs([obs[0] for obs in obstaculos]) > DIST_MIN:
        rect_piso = pygame.Rect(ANCHO, PISO - 50, 35, 50)
        obstaculos.append((rect_piso, piedra_piso))
        spawn_piso = 0

    if spawn_techo > random.randint(150, 260) and ANCHO - ultimo_obs([obs[0] for obs in obstaculos]) > DIST_MIN:
        rect_techo = pygame.Rect(ANCHO, TECHO + 1.5, 35 , 120)
        obstaculos.append((rect_techo, piedra_techo))
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

#Funcion con valores importantes del juego
def iniciar_valores():
    carro_x = 100
    carro_ancho = 50
    carro_altura = 50
    carro_y = PISO - carro_altura
    carro_vel_y = 0
    carro_salto = False
    carro_agachado = False

    obstaculos = []
    spawn_piso = 0
    spawn_techo = 0

    puntaje = 0
    tiempo_punt = 0
    x_fondo = 0
    fondo_escalado = pygame.transform.scale(fondo_imagen, (ANCHO, ALTURA))

    return (carro_x, carro_y, carro_vel_y, carro_salto, carro_agachado,
            carro_ancho, carro_altura, obstaculos,
            spawn_piso, spawn_techo, puntaje, tiempo_punt,
            x_fondo, fondo_escalado)

#Funcion para administrar saltos, agaches
def manejar_eventos(carro_salto, carro_agachado, carro_vel_y):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if (evento.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w)) and not carro_salto:
                carro_vel_y = -15
                carro_salto = True
            if evento.key in (pygame.K_DOWN, pygame.K_s):
                carro_agachado = True
        if evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_DOWN, pygame.K_s):
                carro_agachado = False
    return carro_salto, carro_agachado, carro_vel_y

#Funcion que revisa colisiones
def verificar_colision(carro_x, y_actual, carro_ancho, altura_actual, obstaculos):
    rect_carro = pygame.Rect(carro_x, y_actual, carro_ancho, altura_actual)
    for rect, _ in obstaculos:
        if rect_carro.colliderect(rect):
            return True
    return False

#Funcion que junta las actualizaciones del juego (movimiento, obstaculos)
def actualizar_estado(carro_y, carro_vel_y, carro_salto, carro_altura, carro_agachado, obstaculos, spawn_piso, spawn_techo):
    spawn_piso, spawn_techo = crear_obstaculos(obstaculos, spawn_piso, spawn_techo)

    for obs in obstaculos:
        obs[0].x -= 8

    obstaculos = [obs for obs in obstaculos if obs[0].x + 35 > 0]

    carro_y, carro_vel_y, carro_salto, y_actual, altura_actual = actualizar_carro(carro_y, carro_vel_y, carro_salto, carro_altura, carro_agachado)

    return carro_y, carro_vel_y, carro_salto, y_actual, altura_actual, obstaculos, spawn_piso, spawn_techo

#Fucncion de puntaje actualizado
def actualizar_puntaje(puntaje, tiempo_punt, clock):
    tiempo_punt += clock.get_time()
    if tiempo_punt >= 1000:
        puntaje += 15
        tiempo_punt = 0
    return puntaje, tiempo_punt

#Dibuja elementos presents en el juego
def dibujar(carro_x, y_actual, carro_ancho, altura_actual, obstaculos, puntaje, fuente, fondo, x_fondo):
    pantalla.blit(fondo, (x_fondo, 0))
    pantalla.blit(fondo, (x_fondo + ANCHO, 0))
    pygame.draw.line(pantalla, NEGRO, (0, PISO), (ANCHO, PISO), 2)
    pygame.draw.line(pantalla, NEGRO, (0, TECHO), (ANCHO, TECHO), 2)
    carro_altura = 50

    if altura_actual < carro_altura:

        pantalla.blit(carrito_agachado, (carro_x, y_actual))
    else:
        pantalla.blit(carrito, (carro_x, y_actual))
    for rect, imagen in obstaculos:
        pantalla.blit(imagen, rect)

    texto_puntaje = fuente.render(f"Puntaje actual: {puntaje}", True, ROJO)
    pantalla.blit(texto_puntaje, (10, 10))
    pygame.display.flip()



#Funcion principal del juego
def juego():
    (carro_x, carro_y, carro_vel_y, carro_salto, carro_agachado,
     carro_ancho, carro_altura, obstaculos,
     spawn_piso, spawn_techo, puntaje, tiempo_punt,
     x_fondo, fondo_escalado) = iniciar_valores()

    letra_puntaje = pygame.font.SysFont(None, 50)
    corriendo = True

    while corriendo:
        clock.tick(FPS)
        x_fondo = agregar_fondo(fondo_escalado, x_fondo, 5)

        carro_salto, carro_agachado, carro_vel_y = manejar_eventos(carro_salto, carro_agachado, carro_vel_y)

        (carro_y, carro_vel_y, carro_salto, y_actual, altura_actual,
         obstaculos, spawn_piso, spawn_techo) = actualizar_estado(
            carro_y, carro_vel_y, carro_salto, carro_altura, carro_agachado, obstaculos, spawn_piso, spawn_techo)

        if verificar_colision(carro_x, y_actual, carro_ancho, altura_actual, obstaculos):
            corriendo = False

        puntaje, tiempo_punt = actualizar_puntaje(puntaje, tiempo_punt, clock)

        dibujar(carro_x, y_actual, carro_ancho, altura_actual, obstaculos, puntaje, letra_puntaje, fondo_escalado, x_fondo)

    pantalla_fin(puntaje)

if __name__ == "__main__":
    juego()