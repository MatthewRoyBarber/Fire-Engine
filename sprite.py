from include import *

class SortedUpdates(pygame.sprite.RenderUpdates):
    """SortedUpdates inherits from PyGame's RenderUpdates class which holds a group of sprites and has useful methods for managing sprites"""

    def sprites(self):
        """Lists every sprite in the group sorted by their visual depth"""
        
        # Second parameter in sorted() allows for an anonymous function that dictates the attribute of each iterable to be sorted

        return sorted(self.spritedict.keys(), key=lambda sprite: sprite.depth)

class Sprite(pygame.sprite.Sprite):
    """Sprite class inherits from PyGame's Sprite class, which contains a lot of useful methods for using sprites"""
    
    def __init__(self, pos, frames=None):
        
        print("wee a sprite")

        # super() inherits the initialization of PyGame's Sprite class, necessary to use as __init__ is a private method
        super(Sprite, self).__init__()
        
        if frames:
            self.frames = frames

        # Starts the image with the first frame of the tileset
        self.image = frames[0][0]

        # Gets a PyGame co-ordinates holding object of the image, containing useful methods
        self.rect = self.image.get_rect()

        # Controls animation of the sprite 
        self.animation = self.stand_animation()

        # Contains co-ordinates of the sprite on the map- assigns the pos attribute as a Python property to allow for easy interaction with the (Tuple) value
        self.pos = pos  

    def _get_pos(self):
        """Finds the current position of the sprite on the map"""
        
        return (self.rect.midbottom[0]-(MAP_TILE_WIDTH/2))/MAP_TILE_WIDTH, (self.rect.midbottom[1]-(MAP_TILE_HEIGHT))/MAP_TILE_HEIGHT

    def _set_pos(self, pos):
        """Set the position and depth of the sprite on the map"""
        
        self.rect.midbottom = pos[0]*MAP_TILE_WIDTH+(MAP_TILE_WIDTH/2), pos[1]*MAP_TILE_HEIGHT+(MAP_TILE_HEIGHT)
        self.depth = self.rect.midbottom[1]

    # property() makes a property, the first argument defining the reading method to use, the second argument defining the writing method to use
    pos = property(_get_pos, _set_pos)

    def move(self, dx, dy):
        """Changes the position of the sprite on-screen"""
        
        self.rect.move_ip(dx, dy) 
        self.depth = self.rect.midbottom[1]

    def stand_animation(self):
        """Sets the animation of the image when not moving"""
        print("Bob")
        
        # Infinite loop as sprites have animations that loop for the duration of the play session
        while True:
            
            # "yield None" essentially pauses the iteration until it is next called upon (after one program tick)
            for frame in self.frames[0]:
                self.image = frame
                yield None
                yield None

    def update(self, *args):
        """Goes through animation frames"""
        
        # Python's inbuilt next method goes through an iteration
        self.animation.next()

class Player(Sprite):
    """Player class inherits from the Sprite class, having the properties of in-game sprites but also contains necessary features unique to playable units"""

    def __init__(self, sprite_cache, pos=(1, 1)):
        
        self.frames = sprite_cache["player.png"]
        
        # super() inherits the initialization of PyGame's Sprite class, necessary to use as __init__ is a private method
        Sprite.__init__(self, pos, self.frames)
        
        # Overwrites the attribute's initialization with
        self.animation = None
        
        # Contains the first-level array index, or column, of the initial player sprite in the player tileset- each column pertains to a direction of movement
        self.direction = 2
        
        #  Contains the current image of the sprite, initially the first image (index 0) of the direction column
        self.image = self.frames[self.direction][0]  

    def walk_animation(self):
        """Handles the player animation for each direction of movement"""

        # Iterates over each second-level array element, or row, of the chosen direction column
        # "yield None" essentially pauses the iteration until it is next called upon (after one program tick)
        for frame in range(4):  
            self.image = self.frames[self.direction][frame]
            yield None
            self.move(4*DX[self.direction], 4*DY[self.direction])
            yield None
            self.move(4*DX[self.direction], 4*DY[self.direction])

    def update(self, *args):
        """Goes through the animation frames"""
        
        if self.animation is None:
            self.image = self.frames[self.direction][0]
        else:
            try:
                self.animation.next()
            except StopIteration:
                self.animation = None