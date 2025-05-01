import os
import sys
import pygame
from PIL import Image, ImageSequence

def load_gif_frames(gif_path):
    """Load all frames from a GIF file and convert them to Pygame surfaces"""
    if not os.path.exists(gif_path):
        print(f"Error: File not found: {gif_path}")
        return None, None
        
    try:
        gif = Image.open(gif_path)
        frames = []
        durations = []
        
        for frame in ImageSequence.Iterator(gif):
            # Convert to RGBA if needed
            if frame.mode != 'RGBA':
                frame = frame.convert('RGBA')
            
            # Convert PIL Image to pygame surface
            frame_data = frame.tobytes()
            size = frame.size
            mode = frame.mode
            
            py_image = pygame.image.fromstring(frame_data, size, mode)
            frames.append(py_image)
            
            # Get frame duration in milliseconds
            duration = frame.info.get('duration', 100)  # Default to 100ms
            durations.append(duration / 1000.0)  # Convert to seconds
        
        return frames, durations
        
    except Exception as e:
        print(f"Error loading GIF: {e}")
        return None, None

def main():
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python simple_gif_viewer.py <path_to_gif>")
        return
    
    gif_path = sys.argv[1]
    
    # Initialize Pygame
    pygame.init()
    
    # Load the GIF frames
    frames, durations = load_gif_frames(gif_path)
    if not frames:
        return
    
    # Set up the display
    first_frame = frames[0]
    screen = pygame.display.set_mode((first_frame.get_width(), first_frame.get_height()))
    pygame.display.set_caption(f"GIF Viewer - {os.path.basename(gif_path)}")
    
    # Animation state
    current_frame = 0
    frame_timer = 0
    clock = pygame.time.Clock()
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update animation
        dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
        frame_timer += dt
        
        if frame_timer >= durations[current_frame]:
            frame_timer = 0
            current_frame = (current_frame + 1) % len(frames)
        
        # Draw the current frame
        screen.fill((0, 0, 0))
        screen.blit(frames[current_frame], (0, 0))
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()