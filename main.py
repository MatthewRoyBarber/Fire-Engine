"""
Main program for Fire Engine
"""
from include import *


if __name__ == "__main__":
    """Starts the program"""

    # Initializes the TileCache objects to hold the necessary images (that are loaded into the programs memory)
    sprite_cache = TileCache(*RES)
    map_cache = TileCache(*RES)
    tile_cache = TileCache(*RES)

    # Initilizes PyGame
    pygame.init()

    # Initilizes the dimensions of the prorgam's display window
    display_dimensions = (768, 512)
    pygame.display.set_mode(display_dimensions)
    
    pygame.display.set_caption("Fire Engine")
    
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)
    
    level = Level('example.map', map_cache)
    
    # Starts rendering the game, and contiously processes user inputs
    test_mode = Game(level, sprite_cache, map_cache, tile_cache)
    test_mode.main()
