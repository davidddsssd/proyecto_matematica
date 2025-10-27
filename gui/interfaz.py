import pygame
import os

# Dimensiones del tablero
ANCHO = 600
ALTO = 600
DIMENSION = 8  # 8x8
TAMANO_CASILLA = ALTO // DIMENSION

# Colores
BLANCO = (255, 255, 255)
NEGRO = (170, 170, 170)

IMAGENES = {}

def cargar_imagenes():
    pieza = 'wb'
    ruta = f"imagenes/{pieza}.png"
    if os.path.exists(ruta):
        IMAGENES[pieza] = pygame.transform.scale(
            pygame.image.load(ruta),
            (TAMANO_CASILLA, TAMANO_CASILLA)
        )
        print("✅ Imagen wb.png cargada correctamente")
    else:
        print(f"⚠️ No se encontró la imagen: {ruta}")

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ajedrez - Prueba de wb")
    reloj = pygame.time.Clock()
    
    cargar_imagenes()

    # Tablero vacío excepto una pieza (wb en el centro)
    tablero = [["--" for _ in range(DIMENSION)] for _ in range(DIMENSION)]
    tablero[3][3] = "wb"  # Colocamos el alfil blanco en el centro

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        dibujar_tablero(pantalla)
        dibujar_piezas(pantalla, tablero)
        
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

def dibujar_tablero(pantalla):
    """ Dibuja las casillas del tablero """
    for fila in range(DIMENSION):
        for columna in range(DIMENSION):
            color = BLANCO if (fila + columna) % 2 == 0 else NEGRO
            pygame.draw.rect(pantalla, color, pygame.Rect(
                columna * TAMANO_CASILLA,
                fila * TAMANO_CASILLA,
                TAMANO_CASILLA,
                TAMANO_CASILLA
            ))

def dibujar_piezas(pantalla, tablero):
    """ Dibuja las piezas en el tablero """
    for fila in range(DIMENSION):
        for columna in range(DIMENSION):
            pieza = tablero[fila][columna]
            if pieza != "--" and pieza in IMAGENES:
                pantalla.blit(IMAGENES[pieza], pygame.Rect(
                    columna * TAMANO_CASILLA,
                    fila * TAMANO_CASILLA,
                    TAMANO_CASILLA,
                    TAMANO_CASILLA
                ))
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ajedrez - Prueba de wb")
    reloj = pygame.time.Clock()
    
    cargar_imagenes()

    tablero = [["--" for _ in range(DIMENSION)] for _ in range(DIMENSION)]
    tablero[3][3] = "wb"  # solo el alfil blanco en el centro

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        dibujar_tablero(pantalla)
        dibujar_piezas(pantalla, tablero)
        
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
