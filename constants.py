# Dimensions of the map tiles in pixels
MAP_TILE_WIDTH, MAP_TILE_HEIGHT = 32, 32
RES = MAP_TILE_WIDTH, MAP_TILE_HEIGHT

# DX and DY contains the offset values for North, East, South and West respectively
# DX represents the direction in the horizontal, or each row of the map
# DY represents the direction in the vertical, or each column of the map
# Each value acts as multiplier for calculating the direction of movement of moving sprites
DX = [0, 1, 0, -1]
DY = [-1, 0, 1, 0]