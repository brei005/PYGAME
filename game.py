import pygame
import sys
import random
import noise

# Pygame initialization
pygame.init()

# Screen configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minecraft-Style Ecosystem Simulator")

# Colors
COLORS = {
    'GRASS': (34, 139, 34),
    'DIRT': (139, 69, 19),
    'STONE': (128, 128, 128),
    'WATER': (64, 164, 223),
    'SKY': (135, 206, 235),
    'WOOD': (139, 69, 19),
    'LEAVES': (34, 139, 34),
    'RED': (255, 0, 0),
    'WHITE': (255, 255, 255)
}

# Game settings
TILE_SIZE = 64
RENDER_DISTANCE = 16
WORLD_SIZE = 256
CHUNK_SIZE = 16

# Player settings
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.inventory = {}
        self.selected_block = None
        self.breaking_progress = 0
        self.breaking_time = 60  # Frames to break a block

# World generation
class WorldGenerator:
    def __init__(self, seed=None):
        self.seed = seed or random.randint(0, 1000000)
        self.world = {}
    
    def generate_chunk(self, chunk_x, chunk_y):
        chunk = {}
        for local_x in range(CHUNK_SIZE):
            for local_y in range(CHUNK_SIZE):
                # Use Perlin noise for terrain generation
                world_x = chunk_x * CHUNK_SIZE + local_x
                world_y = chunk_y * CHUNK_SIZE + local_y
                
                # Height map
                height = int(noise.pnoise2(
                    world_x / 100, 
                    world_y / 100, 
                    octaves=4, 
                    persistence=0.5, 
                    lacunarity=2.0, 
                    repeatx=WORLD_SIZE, 
                    repeaty=WORLD_SIZE, 
                    base=self.seed
                ) * 20 + 64)
                
                # Biome and block type determination
                if height < 55:
                    chunk[(local_x, local_y)] = 'WATER'
                elif height < 60:
                    chunk[(local_x, local_y)] = 'SAND'
                elif height < 65:
                    chunk[(local_x, local_y)] = 'GRASS'
                else:
                    chunk[(local_x, local_y)] = 'STONE'
                
                # Add trees and vegetation
                if random.random() < 0.01 and chunk[(local_x, local_y)] == 'GRASS':
                    chunk[(local_x, local_y, 'TREE')] = True
        
        return chunk

    def get_chunk(self, chunk_x, chunk_y):
        chunk_key = (chunk_x, chunk_y)
        if chunk_key not in self.world:
            self.world[chunk_key] = self.generate_chunk(chunk_x, chunk_y)
        return self.world[chunk_key]

# Renderer
class Renderer:
    @staticmethod
    def draw_block(screen, block_type, x, y):
        color = COLORS.get(block_type, COLORS['GRASS'])
        pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
        
        # Add block outlines
        pygame.draw.rect(screen, (0,0,0), (x, y, TILE_SIZE, TILE_SIZE), 1)

# Game class
class MinecraftLikeGame:
    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.world_generator = WorldGenerator()
        self.player = Player(WORLD_SIZE // 2, WORLD_SIZE // 2)
        self.camera_x = 0
        self.camera_y = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Mouse interactions
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click - break block
                    self.break_block()
                elif event.button == 3:  # Right click - place block
                    self.place_block()
            
            # Keyboard movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.y -= 1
            if keys[pygame.K_s]:
                self.player.y += 1
            if keys[pygame.K_a]:
                self.player.x -= 1
            if keys[pygame.K_d]:
                self.player.x += 1
        
        return True
    
    def break_block(self):
        # Implement block breaking logic
        pass
    
    def place_block(self):
        # Implement block placement logic
        pass
    
    def render_world(self):
        self.screen.fill(COLORS['SKY'])
        
        # Calculate visible chunks
        start_chunk_x = max(0, (self.player.x - RENDER_DISTANCE) // CHUNK_SIZE)
        start_chunk_y = max(0, (self.player.y - RENDER_DISTANCE) // CHUNK_SIZE)
        end_chunk_x = min(WORLD_SIZE // CHUNK_SIZE, (self.player.x + RENDER_DISTANCE) // CHUNK_SIZE)
        end_chunk_y = min(WORLD_SIZE // CHUNK_SIZE, (self.player.y + RENDER_DISTANCE) // CHUNK_SIZE)
        
        # Render chunks
        for chunk_x in range(int(start_chunk_x), int(end_chunk_x) + 1):
            for chunk_y in range(int(start_chunk_y), int(end_chunk_y) + 1):
                chunk = self.world_generator.get_chunk(chunk_x, chunk_y)
                
                for (local_x, local_y), block_type in chunk.items():
                    if isinstance(local_x, int):  # Filter out tree markers
                        screen_x = (local_x - self.player.x + RENDER_DISTANCE) * TILE_SIZE
                        screen_y = (local_y - self.player.y + RENDER_DISTANCE) * TILE_SIZE
                        Renderer.draw_block(self.screen, block_type, screen_x, screen_y)
        
        # Render player
        player_screen_x = SCREEN_WIDTH // 2
        player_screen_y = SCREEN_HEIGHT // 2
        pygame.draw.rect(self.screen, COLORS['WHITE'], 
                         (player_screen_x, player_screen_y, TILE_SIZE, TILE_SIZE))
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            self.render_world()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Main game execution
if __name__ == "__main__":
    game = MinecraftLikeGame()
    game.run()