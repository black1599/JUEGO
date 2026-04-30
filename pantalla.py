
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


