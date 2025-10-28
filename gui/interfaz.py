import pygame
import os
import chess  # <-- Importamos la biblioteca

# Dimensiones del tablero
ANCHO = 600
ALTO = 600
DIMENSION = 8
TAMANO_CASILLA = ALTO // DIMENSION

# Colores (Usando la paleta verde)
BLANCO = (190, 190, 190)
NEGRO  = (50, 50, 50)
RESALTADO = (186, 202, 68) # Para la casilla seleccionada

IMAGENES = {}

def cargar_imagenes():
    """Carga todas las imágenes de piezas (blancas y negras)"""
    # IMPORTANTE: Tus imágenes usan 'h' (horse) y 't' (tower)
    # python-chess usa 'n' (knight) y 'r' (rook).
    # La función 'mapear_pieza_a_imagen' se encarga de "traducir" esto.
    piezas = ['tw', 'hw', 'bw', 'qw', 'kw', 'pw',
              'tb', 'hb', 'bb', 'qb', 'kb', 'pb']
    for pieza in piezas:
        ruta = f"imagenes/{pieza}.png"
        if os.path.exists(ruta):
            IMAGENES[pieza] = pygame.transform.scale(
                pygame.image.load(ruta),
                (TAMANO_CASILLA, TAMANO_CASILLA)
            )
            print(f"✅ Imagen {pieza}.png cargada correctamente")
        else:
            print(f"⚠️ No se encontró la imagen: {ruta}")

def mapear_pieza_a_imagen(pieza):
    """
    Traduce un objeto Pieza de 'python-chess' al nombre de archivo de imagen.
    Ej: Piece(chess.PAWN, chess.WHITE) -> 'pw'
    Ej: Piece(chess.KNIGHT, chess.BLACK) -> 'hb' (usando tu 'h' de horse)
    """
    # Mapeo de tipos de pieza a tus prefijos
    tipo_map = {
        chess.PAWN: 'p',
        chess.KNIGHT: 'h', # Usando 'h' de 'horse'
        chess.BISHOP: 'b',
        chess.ROOK: 't',   # Usando 't' de 'tower'  
        chess.QUEEN: 'q',
        chess.KING: 'k'
    }
    # Mapeo de color
    color_map = {
        chess.WHITE: 'w',
        chess.BLACK: 'b'
    }
    
    # Combinamos: ej. 'p' + 'w' = 'pw'
    return tipo_map[pieza.piece_type] + color_map[pieza.color]

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ajedrez con Lógica de 'python-chess'")
    reloj = pygame.time.Clock()
    
    # --- ¡CAMBIO CLAVE! ---
    # Ya no usamos una lista de listas. Usamos el tablero real de la biblioteca.
    board = chess.Board()
    
    cargar_imagenes()

    casilla_seleccionada = None  # (fila, col) de la *primera* casilla en la que se hizo clic
    
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                col = pos_mouse[0] // TAMANO_CASILLA
                fila = pos_mouse[1] // TAMANO_CASILLA
                
                if casilla_seleccionada is None:
                    # --- Primer clic: Seleccionar una pieza ---
                    
                    # Convertimos (fila, col) de Pygame a un índice de 'python-chess' (0-63)
                    # Pygame (0,0) es Arriba-Izquierda. Chess (a8) es Arriba-Izquierda.
                    # Pygame fila 0 es rank 8. Pygame fila 7 es rank 1.
                    # Fórmula: chess.square(file_index, rank_index)
                    cuadro_idx = chess.square(col, 7 - fila)
                    
                    pieza = board.piece_at(cuadro_idx)
                    
                    # Si hay una pieza en esa casilla, la seleccionamos
                    if pieza is not None:
                         # Solo seleccionamos si es del turno correcto
                        if (pieza.color == chess.WHITE and board.turn == chess.WHITE) or \
                           (pieza.color == chess.BLACK and board.turn == chess.BLACK):
                            casilla_seleccionada = (fila, col)
                
                else:
                    # --- Segundo clic: Mover la pieza ---
                    fila_origen, col_origen = casilla_seleccionada
                    
                    # Convertir origen y destino a formato 'python-chess'
                    cuadro_origen = chess.square(col_origen, 7 - fila_origen)
                    cuadro_destino = chess.square(col, 7 - fila)
                    
                    # Crear el objeto 'Move'
                    # Nota: Esto también maneja promociones de peón simples (asume Reina)
                    move = chess.Move(cuadro_origen, cuadro_destino)
                    if board.piece_at(cuadro_origen).piece_type == chess.PAWN:
                        if (cuadro_destino >= 56 and board.turn == chess.WHITE) or \
                           (cuadro_destino <= 7 and board.turn == chess.BLACK):
                            move = chess.Move(cuadro_origen, cuadro_destino, promotion=chess.QUEEN)

                    # --- ¡Validación de movimiento! ---
                    if move in board.legal_moves:
                        board.push(move)  # Aplicar el movimiento si es legal
                    
                    # Reiniciar la selección, sea legal o no
                    casilla_seleccionada = None

        # Dibujado
        dibujar_tablero(pantalla)
        dibujar_resaltado(pantalla, casilla_seleccionada)
        
        # Pasamos el objeto 'board' para que se dibuje
        dibujar_piezas(pantalla, board) 
        
        pygame.display.flip()
        
        # Comprobar si hay Jaque Mate o Ahogado
        if board.is_checkmate():
            print("¡Jaque Mate!")
            corriendo = False
        elif board.is_stalemate():
            print("¡Ahogado (Tablas)!")
            corriendo = False
            
        reloj.tick(60)

    pygame.quit()

def dibujar_tablero(pantalla):
    """Dibuja las casillas del tablero"""
    for fila in range(DIMENSION):
        for columna in range(DIMENSION):
            color = BLANCO if (fila + columna) % 2 == 0 else NEGRO
            pygame.draw.rect(pantalla, color, pygame.Rect(
                columna * TAMANO_CASILLA,
                fila * TAMANO_CASILLA,
                TAMANO_CASILLA,
                TAMANO_CASILLA
            ))

def dibujar_resaltado(pantalla, casilla_seleccionada):
    """
    Dibuja un cuadrado resaltado en la casilla seleccionada.
    """
    if casilla_seleccionada is not None:
        fila, col = casilla_seleccionada
        pygame.draw.rect(pantalla, RESALTADO, pygame.Rect(
            col * TAMANO_CASILLA,
            fila * TAMANO_CASILLA,
            TAMANO_CASILLA,
            TAMANO_CASILLA
        ), 5) # Grosor 5

def dibujar_piezas(pantalla, board):
    """
    Dibuja las piezas en el tablero leyendo desde el objeto 'board' de python-chess.
    """
    # Iteramos por los 64 cuadros del tablero (0 a 63)
    for i in range(64):
        pieza = board.piece_at(i)
        
        if pieza is not None:
            # Convertimos el índice (0-63) a (fila, col) de Pygame
            # Fila 0 de Pygame = Rango 8 de Ajedrez (índices 56-63)
            # Fila 7 de Pygame = Rango 1 de Ajedrez (índices 0-7)
            fila = 7 - (i // 8)
            col = i % 8
            
            # Obtenemos el nombre de la imagen (ej. 'pw', 'hb')
            nombre_imagen = mapear_pieza_a_imagen(pieza)
            
            if nombre_imagen in IMAGENES:
                pantalla.blit(IMAGENES[nombre_imagen], pygame.Rect(
                    col * TAMANO_CASILLA,
                    fila * TAMANO_CASILLA,
                    TAMANO_CASILLA,
                    TAMANO_CASILLA
                ))

if __name__ == "__main__":
    main()



    