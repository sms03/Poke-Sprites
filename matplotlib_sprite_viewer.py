import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image, ImageSequence

class MatplotlibSpriteViewer:
    def __init__(self, gif_path=None):
        # Setup figure and axis
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.fig.canvas.manager.set_window_title("Pokémon Sprite Viewer (Matplotlib)")
        
        # Remove axes ticks and frame
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_frame_on(False)
        
        # Animation variables
        self.frames = []
        self.durations = []
        self.current_frame = 0
        self.animation = None
        
        # Load initial sprite if provided
        if gif_path and os.path.exists(gif_path):
            self.load_sprite(gif_path)
        else:
            self.display_welcome()
            
        # Key bindings for keyboard shortcuts
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        
    def display_welcome(self):
        """Display welcome message when no sprite is loaded"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Press 'o' to open a sprite\nor 1-5 to load sprites by number", 
                    horizontalalignment='center', verticalalignment='center',
                    fontsize=12, color='black', transform=self.ax.transAxes)
        self.ax.set_title("Pokémon Sprite Viewer")
        plt.tight_layout()
        self.fig.canvas.draw_idle()
        
    def on_key_press(self, event):
        """Handle key press events"""
        if event.key == 'escape':
            plt.close(self.fig)
        elif event.key == 'o':
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import tkinter as tk
            from tkinter import filedialog
            
            # Create a temporary Tkinter root to use the file dialog
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            
            file_path = filedialog.askopenfilename(
                title="Select Pokémon Sprite",
                filetypes=[("GIF Files", "*.gif"), ("All Files", "*.*")]
            )
            
            root.destroy()
            
            if file_path and os.path.exists(file_path):
                self.load_sprite(file_path)
        elif event.key in ['1', '2', '3', '4', '5']:
            self.load_numbered_sprite(int(event.key))
    
    def load_numbered_sprite(self, num):
        """Load a sprite that starts with the given number"""
        sprites_dir = "sprites"
        if os.path.exists(sprites_dir):
            for file in os.listdir(sprites_dir):
                if file.startswith(f"{num}") and file.endswith(".gif"):
                    self.load_sprite(os.path.join(sprites_dir, file))
                    break
    
    def load_sprite(self, gif_path):
        """Load a sprite from a GIF file"""
        try:
            # Stop any current animation
            if self.animation:
                self.animation.event_source.stop()
                
            # Open and process the GIF
            gif = Image.open(gif_path)
            self.frames = []
            self.durations = []
            
            # Extract frames and durations
            for frame in ImageSequence.Iterator(gif):
                # Convert frame to RGB if needed
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                
                # Convert to array for matplotlib
                frame_array = np.array(frame)
                self.frames.append(frame_array)
                
                # Get duration in milliseconds, convert to seconds for FuncAnimation
                duration = frame.info.get('duration', 100) / 1000  # Default to 100ms
                self.durations.append(duration)
            
            # Set the window title to include the sprite name
            self.fig.canvas.manager.set_window_title(f"Pokémon Sprite: {os.path.basename(gif_path)}")
            
            # Reset animation
            self.current_frame = 0
            
            # Update display immediately with first frame
            self.ax.clear()
            self.img_obj = self.ax.imshow(self.frames[0])
            self.ax.set_title(os.path.basename(gif_path))
            plt.tight_layout()
            
            # Calculate the interval (use the first frame's duration)
            interval_ms = self.durations[0] * 1000  # Convert to milliseconds
            
            # Start animation
            self.animation = FuncAnimation(
                self.fig, self.update_frame, 
                frames=len(self.frames),
                interval=interval_ms, 
                blit=True,
                repeat=True
            )
            
            # Show the figure
            self.fig.canvas.draw_idle()
            
        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Error loading sprite:\n{str(e)}", 
                        horizontalalignment='center', verticalalignment='center',
                        fontsize=10, color='red', transform=self.ax.transAxes)
            plt.tight_layout()
            self.fig.canvas.draw_idle()
    
    def update_frame(self, frame_idx):
        """Update the animation to the specified frame"""
        # Use current_frame and increment for proper timing
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        
        # Update the image data
        self.img_obj.set_array(self.frames[self.current_frame])
        
        # Update the interval for the next frame
        if self.animation:
            interval_ms = self.durations[self.current_frame] * 1000
            self.animation.event_source.interval = interval_ms
            
        return [self.img_obj]

def main():
    # Get the path to the sprite from command line arguments
    initial_sprite = None
    if len(sys.argv) > 1:
        initial_sprite = sys.argv[1]
    
    # Create and run the viewer
    viewer = MatplotlibSpriteViewer(initial_sprite)
    
    # Display instructions
    print("Pokémon Sprite Viewer (Matplotlib)")
    print("Commands:")
    print("  o      - Open sprite file")
    print("  1-5    - Load sprite starting with that number")
    print("  Escape - Exit viewer")
    
    # Show the plot (this will block until window is closed)
    plt.show()

if __name__ == "__main__":
    main()