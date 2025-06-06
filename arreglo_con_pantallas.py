import pygame
import sys

pygame.init()

ANCHO, ALTURA = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTURA))
pygame.display.set_caption("Wagon Wild")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GRAY = (180, 180, 180)
PISO = ALTURA - 50
TECHO = 195

def mostrar_texto(texto, tamaño, color, x, y, centrado=True):
    fuente = pygame.font.SysFont(None, tamaño)
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(x, y)) if centrado else render.get_rect(topleft=(x, y))
    pantalla.blit(render, rect)
    return rect

def pantalla_inicio():
    while True:
        pantalla.fill(GRAY)
        mostrar_texto("Wagon Wild", 80, BLACK, ANCHO // 2, ALTURA // 3)

        boton_start = mostrar_texto("Start", 50, RED, ANCHO // 2, ALTURA // 2)
        boton_exit = mostrar_texto("Exit", 40, RED, ANCHO // 2, ALTURA // 2 + 70)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_start.collidepoint(evento.pos):
                    return  # Inicia juego
                if boton_exit.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(30)

def pantalla_fin():
    while True:
        pantalla.fill(GRAY)
        mostrar_texto("You Lose", 80, RED, ANCHO // 2, ALTURA // 3)

        boton_reiniciar = mostrar_texto("Restart", 40, BLACK, ANCHO // 2, ALTURA // 2)
        boton_salir = mostrar_texto("Exit", 40, BLACK, ANCHO // 2, ALTURA // 2 + 70)

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

    obstaculos = []
    obstaculo_ancho = 35
    obstaculo_alto = 50
    obstaculo_techo_ancho = 35
    obstaculo_techo_alto = 100
    obstaculo_vel = 8
    spawn_piso = 0
    spawn_techo = 0

    running = True
    while running:
        clock.tick(FPS)
        pantalla.fill(WHITE)

        # Dibujo techo y piso
        pygame.draw.line(pantalla, BLACK, (0, PISO), (ANCHO, PISO), 2)
        pygame.draw.line(pantalla, BLACK, (0, TECHO), (ANCHO, TECHO), 2)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not salto:
                    carro_vel_y = -15
                    salto = True

        carro_vel_y += gravedad
        carro_y += carro_vel_y

        # Toque con piso
        if carro_y >= PISO - carro_altura:
            carro_y = PISO - carro_altura
            salto = False

        # Col. techo
        if carro_y <= TECHO:
            carro_y = TECHO
            carro_vel_y = 0


        # Crea obstaculos piso
        spawn_piso += 1
        if spawn_piso > 90:
            nuevo_obs_piso = pygame.Rect(ANCHO, PISO - obstaculo_alto, obstaculo_ancho, obstaculo_alto)
            obstaculos.append(nuevo_obs_piso)
            spawn_piso = 0

        # Crea obstaculos techo
        spawn_techo += 1
        if spawn_techo > 130:
            nuevo_obs_techo = pygame.Rect(ANCHO, TECHO, obstaculo_techo_ancho, obstaculo_techo_alto)
            obstaculos.append(nuevo_obs_techo)
            spawn_techo = 0

        # Mover obstaculos
        for obs in obstaculos:
            obs.x -= obstaculo_vel

        # Elimina obstaclos
        obstaculos = [obs for obs in obstaculos if obs.x + obstaculo_ancho > 0]

        # Col. obstaculos
        rect_carro = pygame.Rect(carro_x, carro_y, carro_ancho, carro_altura)
        for obs in obstaculos:
            if rect_carro.colliderect(obs):
                running = False

        # Se dibuja 'carrito' y obstacsulos
        pygame.draw.rect(pantalla, RED, (carro_x, carro_y, carro_ancho, carro_altura))
        for obs in obstaculos:
            pygame.draw.rect(pantalla, GREEN, obs)

        pygame.display.flip()

    pantalla_fin()

# Inicia desde pant. inicio
pantalla_inicio()
juego()