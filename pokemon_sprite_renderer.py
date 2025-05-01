import os
import sys
import time
import pygame
from PIL import Image, ImageSequence

class PokemonSpriteRenderer:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pokémon Sprite Renderer")
        self.clock = pygame.time.Clock()
        self.background_color = (240, 240, 240)  # Light gray background
        
        # Font setup
        self.font = pygame.font.SysFont("Arial", 24)
        
        # Current sprite
        self.current_sprite = None
        self.frames = []
        self.current_frame = 0
        self.frame_duration = 0
        self.last_frame_time = 0
        
    def load_sprite(self, gif_path):
        """Load a GIF sprite and extract its frames"""
        if not os.path.exists(gif_path):
            print(f"Error: Sprite file not found: {gif_path}")
            return False
            
        try:
            gif = Image.open(gif_path)
            self.frames = []
            self.durations = []
            
            for frame in ImageSequence.Iterator(gif):
                # Convert to RGBA if needed
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                
                # Convert PIL Image to pygame surface
                frame_data = frame.tobytes()
                size = frame.size
                mode = frame.mode
                
                py_image = pygame.image.fromstring(frame_data, size, mode)
                self.frames.append(py_image)
                
                # Get frame duration in milliseconds
                duration = frame.info.get('duration', 100)  # Default to 100ms
                self.durations.append(duration)
            
            self.current_sprite = os.path.basename(gif_path)
            self.current_frame = 0
            self.last_frame_time = time.time()
            
            print(f"Loaded {len(self.frames)} frames from {gif_path}")
            return True
            
        except Exception as e:
            print(f"Error loading sprite: {e}")
            return False
            
    def update(self):
        """Update the animation state"""
        if not self.frames:
            return
            
        # Check if it's time to advance to the next frame
        current_time = time.time()
        if current_time - self.last_frame_time > self.durations[self.current_frame] / 1000:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_frame_time = current_time
            
    def draw(self):
        """Draw the current frame"""
        # Fill the background
        self.screen.fill(self.background_color)
        
        # Draw the current frame if available
        if self.frames:
            frame = self.frames[self.current_frame]
            
            # Center the sprite on screen
            x = (self.width - frame.get_width()) // 2
            y = (self.height - frame.get_height()) // 2
            
            self.screen.blit(frame, (x, y))
            
            # Draw sprite name
            if self.current_sprite:
                text = self.font.render(self.current_sprite, True, (0, 0, 0))
                text_rect = text.get_rect(center=(self.width // 2, self.height - 30))
                self.screen.blit(text, text_rect)
        else:
            # Draw instructions if no sprite is loaded
            text = self.font.render("Drop a Pokémon GIF sprite to view", True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()
        
    def run(self, initial_sprite=None):
        """Main application loop"""
        # Optionally load an initial sprite
        if initial_sprite and os.path.exists(initial_sprite):
            self.load_sprite(initial_sprite)
            
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.DROPFILE:
                    # Handle file drop
                    self.load_sprite(event.file)
                elif event.type == pygame.KEYDOWN:
                    # Quit on Escape
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # Load a different sprite with number keys
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                        sprite_num = event.key - pygame.K_0
                        for file in os.listdir("sprites"):
                            if file.startswith(f"{sprite_num}_") and file.endswith(".gif"):
                                self.load_sprite(os.path.join("sprites", file))
                                break
            
            self.update()
            self.draw()
            self.clock.tick(60)  # Limit to 60 FPS
            
        pygame.quit()
        sys.exit()


def main():
    """Entry point of the application"""
    # Get the path to the sprite from command line arguments
    initial_sprite = None
    if len(sys.argv) > 1:
        initial_sprite = sys.argv[1]
    
    # Create and run the renderer
    renderer = PokemonSpriteRenderer()
    renderer.run(initial_sprite)

if __name__ == "__main__":
    main()