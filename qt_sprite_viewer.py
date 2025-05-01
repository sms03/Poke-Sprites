import os
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QFileDialog, QMenuBar, QMenu, QStatusBar, 
                             QMessageBox)
from PySide6.QtGui import QPixmap, QImage, QAction, QDropEvent, QDragEnterEvent
from PySide6.QtCore import QTimer, QByteArray, Qt, QMimeData
from PIL import Image, ImageSequence
import io

class PokemonSpriteViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Pokémon Sprite Viewer (Qt)")
        self.resize(400, 400)
        self.setMinimumSize(300, 300)
        
        # Setup central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Image display label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #f0f0f0;")
        self.layout.addWidget(self.image_label)
        
        # Setup status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Drop a GIF or use File > Open")
        
        # Setup menu bar
        self.create_menus()
        
        # Animation setup
        self.frames = []
        self.frame_durations = []
        self.current_frame = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.current_sprite_path = None
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        
    def create_menus(self):
        # Create menu bar
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # Open action
        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Esc")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        # About action
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        """Handle drop events"""
        urls = event.mimeData().urls()
        if urls and len(urls) > 0:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith('.gif'):
                self.load_sprite(file_path)
            else:
                QMessageBox.warning(self, "Error", "Please drop a valid GIF file")
                
    def keyPressEvent(self, event):
        """Handle key press events"""
        # Number keys 1-5 for quick sprite loading
        key = event.key()
        if Qt.Key_1 <= key <= Qt.Key_5:
            num = key - Qt.Key_0
            self.load_numbered_sprite(num)
        else:
            super().keyPressEvent(event)
            
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
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Pokémon Sprite",
            "",
            "GIF Files (*.gif);;All Files (*.*)"
        )
        
        if file_path and os.path.exists(file_path):
            self.load_sprite(file_path)
            
    def load_sprite(self, gif_path):
        """Load a sprite from a GIF file"""
        try:
            # Stop any current animation
            if self.timer.isActive():
                self.timer.stop()
            
            # Load the GIF using PIL
            gif = Image.open(gif_path)
            self.frames = []
            self.frame_durations = []
            
            # Extract frames and their durations
            for frame in ImageSequence.Iterator(gif):
                # Convert to RGBA mode if needed
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                
                # Convert PIL Image to QPixmap
                buffer = io.BytesIO()
                frame.save(buffer, format='PNG')
                buffer.seek(0)
                
                img = QImage.fromData(QByteArray(buffer.read()), 'PNG')
                pixmap = QPixmap.fromImage(img)
                
                # Optional scaling for small sprites
                # if pixmap.width() < 100:
                #     pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2,
                #                           Qt.KeepAspectRatio, Qt.FastTransformation)
                
                self.frames.append(pixmap)
                
                # Get duration in milliseconds
                duration = frame.info.get('duration', 100)  # Default to 100ms
                self.frame_durations.append(duration)
            
            # Update status with filename
            self.current_sprite_path = gif_path
            self.status_bar.showMessage(f"Sprite: {os.path.basename(gif_path)} ({len(self.frames)} frames)")
            
            # Start animation
            self.current_frame = 0
            self.show_current_frame()
            self.start_animation()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load sprite: {str(e)}")
            
    def start_animation(self):
        """Start the animation timer"""
        if self.frames:
            self.timer.start(self.frame_durations[self.current_frame])
            
    def show_current_frame(self):
        """Display the current frame"""
        if self.frames and 0 <= self.current_frame < len(self.frames):
            self.image_label.setPixmap(self.frames[self.current_frame])
            
    def next_frame(self):
        """Advance to the next animation frame"""
        if not self.frames:
            return
            
        # Move to next frame
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        
        # Show the frame
        self.show_current_frame()
        
        # Update timer for the new frame's duration
        self.timer.setInterval(self.frame_durations[self.current_frame])
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Pokémon Sprite Viewer",
            "Pokémon Sprite Viewer\n\n"
            "A Qt-based application to view animated Pokémon sprites.\n\n"
            "- Use the File menu to open sprites\n"
            "- Drag and drop GIF files onto the window\n"
            "- Press 1-5 keys to quickly access sprites\n"
            "- Press Escape to exit\n\n"
            "Created with PySide6 and PIL"
        )

def main():
    app = QApplication(sys.argv)
    
    window = PokemonSpriteViewer()
    window.show()
    
    # Load initial sprite if provided as argument
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        window.load_sprite(sys.argv[1])
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()