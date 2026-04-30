
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

#bucle
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #limpiar pantalla
    pantalla.fill((230, 230, 230))

    pygame.display.flip() #actualiza la pantalla
    clock.tick(60) #limite de fps