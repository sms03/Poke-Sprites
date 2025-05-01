import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageSequence

class TkPokemonSpriteViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Pokémon Sprite Viewer (Tkinter)")
        self.geometry("400x400")
        self.minsize(300, 300)
        
        # Set up the main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Image display label
        self.image_label = tk.Label(self.main_frame, bg='#f0f0f0')
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = tk.Label(self, text="Use File > Open to load a sprite", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create menu
        self.menu_bar = tk.Menu(self)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        
        self.config(menu=self.menu_bar)
        
        # Animation variables
        self.is_animating = False
        self.frames = []
        self.frame_durations = []
        self.current_frame = 0
        self.current_sprite_path = None
        
        # Bind keyboard shortcuts
        self.bind("<Escape>", lambda e: self.quit())
        for i in range(1, 6):
            self.bind(str(i), lambda e, num=i: self.load_numbered_sprite(num))
            
    def load_numbered_sprite(self, num):
        """Load a sprite that starts with the given number"""
        sprites_dir = "sprites"
        if os.path.exists(sprites_dir):
            for file in os.listdir(sprites_dir):
                if file.startswith(f"{num}") and file.endswith(".gif"):
                    self.load_sprite(os.path.join(sprites_dir, file))
                    break
            
    def open_file(self):
        """Open file dialog to select a GIF"""
        file_path = filedialog.askopenfilename(
            title="Select Pokémon Sprite",
            filetypes=[("GIF Files", "*.gif"), ("All Files", "*.*")]
        )
        
        if file_path and os.path.exists(file_path):
            self.load_sprite(file_path)
    
    def load_sprite(self, gif_path):
        """Load a sprite from a GIF file"""
        try:
            # Stop any current animation
            if self.is_animating:
                self.is_animating = False
                self.after_cancel(self.animation_id)
            
            # Load the GIF
            self.gif = Image.open(gif_path)
            self.frames = []
            self.frame_durations = []
            
            # Extract frames and their durations
            for frame in ImageSequence.Iterator(self.gif):
                # Convert to RGBA mode if needed
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                
                # Resize if needed (uncomment if you want to scale up small sprites)
                # scale = 2  # Scale factor
                # frame = frame.resize((frame.width * scale, frame.height * scale), Image.NEAREST)
                
                # Convert to PhotoImage for Tkinter
                photoframe = ImageTk.PhotoImage(frame)
                self.frames.append(photoframe)
                
                # Get duration in milliseconds
                duration = frame.info.get('duration', 100)  # Default to 100ms
                self.frame_durations.append(duration)
            
            # Update status with filename
            self.current_sprite_path = gif_path
            self.status_bar.config(text=f"Sprite: {os.path.basename(gif_path)} ({len(self.frames)} frames)")
            
            # Start animation
            self.current_frame = 0
            self.is_animating = True
            self.animate()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sprite: {e}")
    
    def animate(self):
        """Display animation frames with correct timing"""
        if not self.is_animating:
            return
            
        # Display current frame
        if self.frames:
            frame = self.frames[self.current_frame]
            self.image_label.config(image=frame)
            
            # Get duration for current frame
            duration = self.frame_durations[self.current_frame]
            
            # Advance to next frame
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            
            # Schedule next frame
            self.animation_id = self.after(duration, self.animate)
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About Pokémon Sprite Viewer",
            "Pokémon Sprite Viewer\n\n"
            "A simple application to view animated Pokémon sprites.\n\n"
            "- Use the File menu to open sprites\n"
            "- Press 1-5 keys to quickly access sprites\n"
            "- Press Escape to exit\n\n"
            "Created with Tkinter and PIL"
        )
        
def main():
    app = TkPokemonSpriteViewer()
    
    # Load initial sprite if provided as argument
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        app.load_sprite(sys.argv[1])
    
    app.mainloop()

if __name__ == "__main__":
    main()