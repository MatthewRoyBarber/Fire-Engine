from include import *

class TileCache:
    """Loads a tileset into the program"""

    def __init__(self,  width, height):
        
        self.width = width
        self.height = height
        self.cache = {}

    def __getitem__(self, filename):
        """Special method that returns table of tiles or generates table if not created"""

        key = (filename, self.width, self.height)
        try:
            return self.cache[key]
        except KeyError:
            tile_table = self._load_tile_table(filename, self.width, self.height)
            self.cache[key] = tile_table
            return tile_table

    def _load_tile_table(self, filename, width, height):
        """Loads a tileset into the program, and slices up individiual tile graphics for easier use"""

        # Makes individual pixels be formatted in-line with the display format- a PyGame "subsurface"
        image = pygame.image.load(filename).convert()

        # Find dimension of loaded image
        image_width, image_height = image.get_size()  # Find dimension of loaded image

        # 2D array to hold all the tiles from the tileset
        tile_table = []

        # Iterates over every row of the map, map_y holds the verical position index, line holds the tiles for that row
        for tile_x in range(0, image_width/width):

            # Array to hold tiles from one line of the tileset
            line = []

            # line is inserted into tile_table, line will be modified below, as Python "passes by reference", tile_table will essentially update as line is changed
            tile_table.append(line)

            # Iterates over every tile of the line, map_x holds the horizontal position index, c holds the tile value
            for tile_y in range(0, image_height/height):

                # Tuple holding co-ordinates and dimensions of individual tiles
                rect = (tile_x*width, tile_y*height, width, height)

                # Makes a new subsurface using the "image" (tileset) as a parent and cutting an individual tile graphic out
                line.append(image.subsurface(rect).convert_alpha())
                
        return tile_table