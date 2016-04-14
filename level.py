from include import *

class Level:
    """Loads and store the level and it's particular properties"""

    def __init__(self, filename, map_cache):
        
        self.tileset = ''
        self.map = []
        self.items = {}
        self.key = {}
        self.width = 0  
        self.height = 0
        self.load_file(filename)
        self.map_cache = map_cache

    def load_file(self, filename):
        """Processes .map file for easy use in program"""

        # Array to hold what every tile in the level is
        self.map = []

        # Dictionary to the information that describes each tile
        self.key = {}

        # Allows for easier use of the ConfigParser module
        parser = ConfigParser.ConfigParser()

        # Parser loads map into program for later use
        parser.read(filename)

        # Holds the name of the tileset that the level uses
        self.tileset = parser.get("level", "tileset")

        # Each index of self.map holds one each index corresponding to a row of the map
        self.map = parser.get("level", "map").split("\n")

        # Iteration goes through every heading of the .map file
        for section in parser.sections():
        
            # Headings of 1 character are definitions of tile properties
            if len(section) == 1:

                # Parser recieves items ("key = value") from .map as tuples in an array, dict() makes the first item of each tuple a key and the respective second item the corresponding value
                desc = dict(parser.items(section))

                # Stores the tile information dictionary in a parent dictionary
                self.key[section] = desc

        # Iterates over every row of the map, map_y holds the verical position index, line holds the tiles for that row
        for y, line in enumerate(self.map):

            # Iterates over every tile of the line, map_x holds the horizontal position index, c holds the tile value
            for x, c in enumerate(line):
                if c not in self.key:
                    pass
                elif not self.is_wall(x, y) and 'sprite' in self.key[c]:
                    self.items[(x, y)] = self.key[c]
                    
        self.width = len(self.map[0])
        self.height = len(self.map)
        
        

    def get_tile(self, x, y):
        """Returns dictionary that describe a tile type"""
        
        # Error handling incase the co-ordinates entered are non-existent in the map
        try:

            # Finds the (keyboard) character in particular co-ordinate of self.map, y finding the array index, and x finding the string index
            char = self.map[y][x]

        except IndexError:
            return {}

        # Error handling incase 'char' key in self.key does not exist
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_bool(self, x, y, name):
        """Finds whether a tile has a flag (boolean value) of a specified attribute (key)"""

        # Recieves the boolean value of the passed name key, in the tile description dictionary self.key
        value = self.get_tile(x, y).get(name)  
        return value

    def is_wall(self, x, y):
        """Checks whether tile is a wall"""
        
        return self.get_bool(x, y, 'wall')

    def is_blocking(self, x, y):
        """Checks whether tile blocks movement"""
        
        if not 0 <= x < self.width or not 0 <= y < self.height:  # Tiles outside map automatically hinder movement
            return True
        return self.get_bool(x, y, 'block')  # block key contains a boolean value

    def render(self):
        """Renders (loads up images in program and displays them in the appropiate position) the map"""

        # Using 'wall' as a function rather than 'self.is_wall' makes the following code cleaner
        wall = self.is_wall

        # tiles refers to the pre-loaded/formatted tileset that the level uses
        tiles = self.map_cache[self.tileset]

        # tiles refers to the pre-loaded/formatted tileset that the level uses
        image = pygame.Surface((self.width*MAP_TILE_WIDTH, self.height*MAP_TILE_HEIGHT))

        # Stores any graphics which visually are infront of the map
        overlays = {}
        
        default_pos = 6, 0
                
        # Iterates over every row of the map, map_y holds the verical position index, line holds the tiles for that row
        # enumerate(array) creates a new array which for which every element contains a tuple (index of element, value of element)
        for map_y, line in enumerate(self.map):

            # Iterates over every tile of the line, map_x holds the horizontal position index, c holds the tile value
            for map_x, c in enumerate(line):
                
                if not c in self.key:
                    pass
                
                # Draw different tiles depending on neighbourhood
                elif wall(map_x, map_y):
                    
                    # If there is a wall above tile
                    if wall(map_x, map_y-1):  

                        # Wall below tile
                        if wall(map_x, map_y+1):
                            
                            if wall(map_x+1, map_y) and wall(map_x-1, map_y):  # Wall both sides of tile
                                tile = 4, 1
                            elif wall(map_x+1, map_y) and not wall(map_x-1, map_y):  # Wall right side of tile
                                tile = 3, 1
                            elif wall(map_x-1, map_y) and not wall(map_x+1, map_y):  # Wall left side of tile
                                tile = 5, 1
                            else:  # No walls either side of tile
                                tile = 0, 1
                                
                        # No wall below tile 
                        else:
                            
                            if wall(map_x+1, map_y) and wall(map_x-1, map_y):  # Wall both sides of tile
                                tile = 4, 2
                            elif wall(map_x+1, map_y) and not wall(map_x-1, map_y):  # Wall right side of tile
                                tile = 0, 2
                            elif wall(map_x-1, map_y) and not wall(map_x+1, map_y):  # Wall left side of tile
                                tile = 2, 2
                            else:  # No walls either side of tile
                                tile = 1, 1
                                
                    # No wall above tile     
                    else:

                        # Wall below tile
                        if wall(map_x, map_y+1):
                            
                            if wall(map_x+1, map_y) and wall(map_x-1, map_y):  # Wall both sides of tile
                                tile = 4, 0
                            elif wall(map_x+1, map_y) and not wall(map_x-1, map_y):  # Wall right side of tile
                                tile = 0, 0
                            elif wall(map_x-1, map_y) and not wall(map_x+1, map_y):  # Wall left side of tile
                                tile = 2, 0
                            else:  # No walls either side of tile
                                # No particular graphic for this, as map designers shouldn't have blocks that fit this case scenario
                                tile = 3, 0

                        # No wall below tile 
                        else:
                            
                            if wall(map_x+1, map_y) or wall(map_x-1, map_y):  # Wall either or both sides of tile
                                tile = 1, 0
                            else:  # Not a wall on either or both sides of the title
                                # No particular graphic for this, as map designers shouldn't have blocks that fit this case scenario
                                tile = 3, 0
                
                # If unit occupies cell, use default background sprite
                elif "sprite" in self.key[c]:
                    tile = default_pos
                
                # If not a wall tile or unit    
                else:
                    
                    # Error exception incase tile's property or requested property's value is not defined, or stringed values cannot be converted to an integer
                    try:

                        # Finds information dictionary for specific tile type, then the 'tile' key which holds the tile graphic position, split(' ,') converts position into array
                        tile = self.key[c]['tile'].split(',')
                        

                        # Array's values converted from strings to integers using int()
                        tile = int(tile[0]), int(tile[1])  
                        
                    except (ValueError, KeyError):

                        # Defaults to ground tile
                        tile = default_pos

                # Finds image by referencing index of the tile graphic pertaining to the co-ordinates in tile_image
                tile_image = tiles[tile[0]][tile[1]]

                # Draws the tile graphic on the map
                image.blit(tile_image, (map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT))
                
        return image, overlays