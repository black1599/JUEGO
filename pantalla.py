
###########CODIGO PARA PANTALLA PRELIMINAR############

#Importación de librerias
import pygame
import sys

pygame.init()

#Ventana de la pantalla del usuario
ANCHO, ALTO = 1100, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulador de Gestión de Energía")

#Reloj para los FPS
clock = pygame.time.Clock()

#Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
GRIS_OSC = (100, 100, 100)
VERDE = (50, 180, 80)
ROJO = (200, 60, 60)

#Texto
fuente_titulo = pygame.font.SysFont("arial", 16, bold=True)
fuente = pygame.font.SysFont("arial", 13)

# Función para dibujar texto
def texto(txt, f, color, x, y):
    s = f.render(txt, True, color)
    pantalla.blit(s, (x, y))


# Función para dibujar rectángulos
def rectangulo(rect, color_fondo, color_borde):
    pygame.draw.rect(pantalla, color_fondo, rect)
    pygame.draw.rect(pantalla, color_borde, rect, 2)
#bucle
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #limpiar pantalla
    pantalla.fill((230, 230, 230))

    # HUD superior
    rectangulo(pygame.Rect(10, 10, ANCHO - 20, 45), BLANCO, NEGRO)

    texto("NIVEL: 1", fuente_titulo, NEGRO, 30, 22)
    texto("DINERO: 500 €", fuente_titulo, NEGRO, 160, 22)
    texto("PRODUCCIÓN: 120 MW", fuente_titulo, NEGRO, 350, 22)
    texto("DEMANDA: 200 MW", fuente_titulo, NEGRO, 590, 22)

    # Panel izquierdo
    rectangulo(pygame.Rect(10, 65, 300, 100), BLANCO, NEGRO)

    texto("PRODUCCIÓN", fuente, NEGRO, 20, 75)
    texto("DEMANDA", fuente, NEGRO, 20, 105)

    #Barras visuales y balance
    pygame.draw.rect(pantalla, VERDE, pygame.Rect(130, 78, 100, 16))
    pygame.draw.rect(pantalla, ROJO, pygame.Rect(130, 108, 150, 16))

    texto("BALANCE:  -80 MW", fuente_titulo, ROJO, 20, 135)


    pygame.display.flip() #actualiza la pantalla
    clock.tick(60) #limite de fps