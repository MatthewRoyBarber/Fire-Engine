from include import *

class Game:
    """Handles the set-up and the interaction of the program"""

    def __init__(self, level, sprite_cache, map_cache, tile_cache):
        
        self.screen = pygame.display.get_surface()
        self.pressed_key = None
        self.game_over = False
        self.sprites = SortedUpdates()  
        self.overlays = pygame.sprite.RenderUpdates()
        self.sprite_cache = sprite_cache
        self.map_cache = map_cache
        self.tile_cache = tile_cache
        self.use_level(level)
        self.sprite_cache = sprite_cache
        self.map_cache = map_cache
        self.tile_cache = tile_cache

    def use_level(self, level):
        """Sets the current level"""
        
        self.sprites = SortedUpdates()
        self.overlays = pygame.sprite.RenderUpdates()
        self.level = level
        for pos, tile in level.items.iteritems():
            if tile.get("player") in ('true', '1', 'yes', 'on'):
                sprite = self.player = Player(self.sprite_cache, pos)
            else:
                sprite = Sprite(pos, self.sprite_cache[tile["sprite"]])
            self.sprites.add(sprite)
        self.background, overlays = self.level.render()
        for (x, y), image in overlays.iteritems():
            overlay = pygame.sprite.Sprite(self.overlays)
            overlay.image = image
            overlay.rect = image.get_rect().move(x*MAP_TILE_WIDTH, y*MAP_TILE_HEIGHT-MAP_TILE_HEIGHT)
        
    def control(self):
        """Handle the controls of in-game units"""

        keys = pygame.key.get_pressed()

        def pressed(key):
            """Check if the specified key is pressed."""

            return self.pressed_key == key or keys[key]

        def walk(d):
            """Start walking (changing unit position and animation) in the specified direction"""

            x, y = self.player.pos
            self.player.direction = d
            if not self.level.is_blocking(x+DX[d], y+DY[d]):
                self.player.animation = self.player.walk_animation()
            
        # Reacts to each arrow key on the keyboard
        if pressed(pg.K_UP):
            walk(0)
        elif pressed(pg.K_DOWN):
            walk(2)
        elif pressed(pg.K_LEFT):
            walk(3)
        elif pressed(pg.K_RIGHT):
            walk(1)
        self.pressed_key = None

    def main(self):
        """Initializes the background and maintains the program loop that responds to user interaction"""

        clock = pygame.time.Clock()
        
        # Draws/loads (not display) the background tiles
        self.screen.blit(self.background, (0, 0))

        # Draws/loads (not display) the overlaying graphics
        self.overlays.draw(self.screen)

        # Updates(displays) the drawn graphics
        pygame.display.flip()

        # Main program loop
        while not self.game_over:

            # Clear all sprites on the screen and re-draw them in their new positions
            self.sprites.clear(self.screen, self.background)
            self.sprites.update()

            # If the player animation is complete (so referred to as None), act accordingly to any key presses.=
            if self.player.animation is None:
                self.control()
                self.player.update()

            dirty = self.sprites.draw(self.screen)
            self.overlays.draw(self.screen)
            pygame.display.update(dirty)

            # Wait for one tick
            clock.tick(30)

            # Runs through every program interaction (event) that has happened in this iteration (i.e. every 30th of a second)
            for event in pygame.event.get(): 
                if event.type == pg.QUIT:
                    self.game_over = True

        # Closes down the program
        pygame.quit()