import pygame
  #usado para generar numeros random


pygame.init() #inicia Pygame

# Configuración de pantalla
ANCHO, ALTURA = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTURA))
pygame.display.set_caption("Wagon Wild")


# Reloj para controlar FPS
clock = pygame.time.Clock()
FPS = 60

# Colores (tentativo, solo por ahora hasta poder consolidar el resto del codigo)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PISO = ALTURA - 50

# Carrito
carro_ancho, carro_altura = 50, 50
carro_x = 100
carro_y = PISO - carro_altura
carro_vel_y = 0
salto = False #importante para la funcion de salto
gravedad = 1 #necesario para simular la caida luego de un salto

# Obstáculos
obstaculos = []
obstaculo_ancho = 40
obstaculo_alto = 60
obstaculo_vel = 6
spawn = 0

# Función para dibujar el carrito
def hacer_carrito(x, y):
    pygame.draw.rect(pantalla, (200, 0, 0), (x, y, carro_ancho, carro_altura))


# Función para dibujar obstáculos
def crear_obstaculos(obs_list):
    for obs in obs_list:
        pygame.draw.rect(pantalla, (0, 200, 0), obs)

# Bucle principal
running = True
while running:
    clock.tick(FPS)
    pantalla.fill(WHITE)


    # Suelo
    pygame.draw.line(pantalla, BLACK, (0, PISO), (ANCHO, PISO), 2)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not salto:
                carro_vel_y = -15
                salto = True

    # Movimiento del carrito
    carro_vel_y += gravedad
    carro_y += carro_vel_y
    if carro_y >= PISO - carro_altura:
        carro_y = PISO - carro_altura
        salto = False

    # Generar obstáculos
    spawn += 1
    if spawn > 90:
        nuevo_obs = pygame.Rect(ANCHO, PISO - obstaculo_alto, obstaculo_ancho, obstaculo_alto)
        obstaculos.append(nuevo_obs)
        spawn = 0

    # Mover obstáculos
    for obs in obstaculos:
        obs.x -= obstaculo_vel

    # Elimina obstáculos que salieron de pantalla
    obstaculos = [obs for obs in obstaculos if obs.x + obstaculo_ancho > 0]

    # Verificar colisiones
    rect_carro = pygame.Rect(carro_x, carro_y, carro_ancho, carro_altura)
    for obs in obstaculos:
        if rect_carro.colliderect(obs):
            running = False
    
    #Formacion
    hacer_carrito(carro_x, carro_y)
    crear_obstaculos(obstaculos)

    pygame.display.flip()

pygame.quit()