import pygame

# Dimensiones del tablero
ANCHO = 800
ALTO = 800
DIMENSION = 8  # 8x8
TAMANO_CASILLA = ALTO // DIMENSION

# Colores
BLANCO = (255, 255, 255)
NEGRO = (170, 170, 170)

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ajedrez")
    reloj = pygame.time.Clock()
    
    dibujar_tablero(pantalla)

    # Bucle principal del juego
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

def dibujar_tablero(pantalla):
    """ Dibuja las casillas del tablero """
    for fila in range(DIMENSION):
        for columna in range(DIMENSION):
            if (fila + columna) % 2 == 0:
                color = BLANCO
            else:
                color = NEGRO
            pygame.draw.rect(pantalla, color, pygame.Rect(columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))

if __name__ == "__main__":
    main()