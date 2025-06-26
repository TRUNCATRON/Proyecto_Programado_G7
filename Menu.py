import pygame
from wagon_wild import juego

pygame.init()

#Pantalla
ANCHO, ALTURA = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTURA))
pygame.display.set_caption("Wagon Wild")

#Icono (momentaneo)
icono = pygame.image.load('imagenes/img_menu/icono juego.png')
pygame.display.set_icon(icono)

#Imagen background (momentaneo)
fondo = pygame.image.load('imagenes/img_menu/fondo.png')
fondo = pygame.transform.scale(fondo, (ANCHO, ALTURA))

#titulo del juego
titulo_img = pygame.image.load('imagenes/img_menu/titulo.png')
titulo_img = pygame.transform.scale_by(titulo_img, 0.8)
titulo_pos = ((ANCHO - 300) // 2, 40)

def mostrar_titulo():
    pantalla.blit(titulo_img, titulo_pos)

#Imagen botones (momentaneo)
inicio_img = pygame.image.load('imagenes/img_menu/inicio.png')
inicio_img = pygame.transform.scale_by(inicio_img, 1.2)
inicio_pos = (277, 200)
inicio_rect = inicio_img.get_rect(topleft=inicio_pos)

instrucciones_img = pygame.image.load('imagenes/img_menu/instrucciones.png')
instrucciones_img = pygame.transform.scale_by(instrucciones_img, 1.2)
instrucciones_pos = (277, 250)
instrucciones_rect = instrucciones_img.get_rect(topleft=instrucciones_pos)

salir_img = pygame.image.load('imagenes/img_menu/salir.png')
salir_img = pygame.transform.scale_by(salir_img, 1.2)
salir_pos = (277, 300)
salir_rect = salir_img.get_rect(topleft=salir_pos)

#imagen instrucciones
instrucciones_pantalla_img = pygame.image.load('imagenes/img_menu/instrucciones_pantalla.png')
instrucciones_pantalla_img = pygame.transform.scale_by(instrucciones_pantalla_img, 1.6)
instrucciones_pantalla_pos = ((ANCHO - 600) // 2, (ALTURA - 300) // 2)
instrucciones_pantalla_rect = instrucciones_pantalla_img.get_rect(topleft=instrucciones_pantalla_pos)

#crear boton
def dibujar_botones():
    pantalla.blit(inicio_img, inicio_pos)
    pantalla.blit(instrucciones_img, instrucciones_pos)
    pantalla.blit(salir_img, salir_pos)


#ciclo principal
mostrar_instrucciones = False
correr = True
while correr:

    #background
    pantalla.blit(fondo, (0, 0))

    mostrar_titulo()
    #dibujar botones
    dibujar_botones()

    #mostrar o ocultar instrucciones
    if mostrar_instrucciones:
        pantalla.blit(instrucciones_pantalla_img, instrucciones_pantalla_rect)

    pygame.display.update()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            correr = False

        #detectar acciones mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if mostrar_instrucciones:
                if  instrucciones_pantalla_rect.collidepoint(evento.pos) and pygame.mouse.get_pressed()[0]:
                    mostrar_instrucciones = False
                    print("Ocultar instrucciones")

            else:

                if inicio_rect.collidepoint(evento.pos) and pygame.mouse.get_pressed()[0]:
                    juego()

                    print("Iniciar juego")

                elif instrucciones_rect.collidepoint(evento.pos) and pygame.mouse.get_pressed()[0]:
                    mostrar_instrucciones = True
                    print("Mostrar instrucciones")

                elif salir_rect.collidepoint(evento.pos) and pygame.mouse.get_pressed()[0]:
                    print("Salir juego")
                    correr = False

pygame.quit()