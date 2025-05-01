<div align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/6.gif" width="120" height="120">
  <h1>🔥 Pokémon Sprite Renderer 🔥</h1>
  <p><em>Gotta Render 'Em All!</em></p>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/pokemon-animated-red.svg" alt="Pokemon: Animated">
</p>

---

## ✨ Features

- 📥 Download animated Pokémon sprites from PokéAPI
- 🖼️ View animated GIF sprites with proper timing
- 🛠️ Multiple renderer implementations (Pygame, Tkinter, Matplotlib)
- 🖱️ Simple drag-and-drop interface (in some implementations)
- ⌨️ Keyboard shortcuts for quick sprite selection
- 🔄 Proper animation timing from the original GIFs

---

<div align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/25.gif" width="80">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/1.gif" width="80">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/4.gif" width="80">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/7.gif" width="80">
</div>

## 🔥 Charizard Spotlight 🔥

Charizard, the iconic Fire/Flying-type Pokémon (#6 in the Pokédex), is a fan favorite and the star of this renderer! With its majestic wings and flaming tail, Charizard represents the power and beauty of Pokémon animation.

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/6.gif" width="100"><br><b>Normal</b></td>
      <td align="center"><img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/shiny/6.gif" width="100"><br><b>Shiny</b></td>
    </tr>
  </table>
</div>

View Charizard in all its animated glory with:
```bash
python pokemon_sprite_renderer.py sprites/6.gif
```

## 🚀 Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/poke-sprites.git
   cd poke-sprites
   ```

2. Set up a virtual environment (recommended):
   ```
   python -m venv poke
   ```

3. Activate the virtual environment:
   - Windows: `poke\Scripts\activate`
   - macOS/Linux: `source poke/bin/activate`

4. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## 📋 Usage

### 📥 Downloading Sprites

Use the `download_sprites.py` script to download Pokémon sprites:

```bash
# Download the first 25 Pokémon
python download_sprites.py --range 1-25

# Download specific Pokémon by ID
python download_sprites.py 1 4 7 25

# Download sprites to a custom directory
python download_sprites.py --range 1-151 --output mypokemon

# Download Charizard (of course!)
python download_sprites.py 6
```

### 👁️ Viewing Sprites

The project includes multiple implementations for viewing sprites:

#### 🎮 Pygame Implementation (Main)

```bash
python pokemon_sprite_renderer.py sprites/1.gif
```

<details>
<summary>Controls</summary>

- Drag and drop GIF files to view them
- Press Escape to exit
- Press 1-5 to quickly load sprites starting with those numbers
</details>

#### 🔄 Simple GIF Viewer

A minimal implementation using Pygame:

```bash
python simple_gif_viewer.py sprites/25.gif
```

<details>
<summary>Controls</summary>

- Press Escape to exit
</details>

#### 🪟 Tkinter Implementation

A viewer using the built-in Tkinter library:

```bash
python tkinter_sprite_viewer.py sprites/4.gif
```

<details>
<summary>Controls</summary>

- Use File > Open to load a sprite
- Press 1-5 to quickly load sprites starting with those numbers
- Press Escape to exit
</details>

#### 📊 Matplotlib Implementation

A viewer using the Matplotlib library:

```bash
python matplotlib_sprite_viewer.py sprites/25.gif
```

<details>
<summary>Controls</summary>

- Press 'o' to open a sprite file
- Press 1-5 to quickly load sprites starting with those numbers
- Press Escape to exit
</details>

#### 💎 Qt Implementation (Optional)

A viewer using PySide6 (Qt). Requires additional installation:

```bash
pip install PySide6
python qt_sprite_viewer.py sprites/6.gif
```

<details>
<summary>Controls</summary>

- Drag and drop GIF files to view them
- Use File > Open to load a sprite
- Press 1-5 to quickly load sprites starting with those numbers
- Press Escape to exit
</details>

## 🛠️ Implementation Details

### Main Components

<table>
  <tr>
    <th>Component</th>
    <th>Description</th>
    <th>Pokemon Type</th>
  </tr>
  <tr>
    <td><b>download_sprites.py</b></td>
    <td>Downloads animated Pokémon sprites from the PokéAPI GitHub repository</td>
    <td>⬇️ Normal</td>
  </tr>
  <tr>
    <td><b>pokemon_sprite_renderer.py</b></td>
    <td>The main Pygame-based implementation for viewing animated sprites</td>
    <td>🔥 Fire</td>
  </tr>
  <tr>
    <td><b>simple_gif_viewer.py</b></td>
    <td>A simplified version of the Pygame renderer</td>
    <td>💧 Water</td>
  </tr>
  <tr>
    <td><b>tkinter_sprite_viewer.py</b></td>
    <td>An implementation using Tkinter, which is included in the Python standard library</td>
    <td>🌿 Grass</td>
  </tr>
  <tr>
    <td><b>matplotlib_sprite_viewer.py</b></td>
    <td>An implementation using Matplotlib for rendering</td>
    <td>⚡ Electric</td>
  </tr>
  <tr>
    <td><b>qt_sprite_viewer.py</b></td>
    <td>An implementation using PySide6 (Qt) for a modern UI experience</td>
    <td>✨ Psychic</td>
  </tr>
</table>

### Dependencies

- **Pygame**: For rendering graphics and handling input in the main implementation
- **Pillow (PIL)**: For processing GIF images
- **Requests**: For downloading sprites from the internet
- **tqdm**: For progress bars during downloads
- **Matplotlib & NumPy**: For the Matplotlib implementation
- **PySide6** (Optional): For the Qt implementation

## ✨ Customization

### Scaling Sprites

Most implementations include commented code for scaling sprites if they're too small. To enable scaling, uncomment the relevant sections in the viewer of your choice.

### Adding Custom Sprites

You can add custom sprites to the `sprites/` directory and view them with any of the renderers. The viewers support any properly formatted GIF file.

## ❓ Troubleshooting

### Common Issues

1. **GIF animation appears choppy**  
   This can happen with GIFs that have inconsistent frame durations. Each implementation handles timing slightly differently.

2. **Error: No module named 'PySide6'**  
   The Qt implementation is optional. Either install PySide6 with `pip install PySide6` or use one of the other viewers.

3. **Sprite files not found**  
   Make sure to download sprites first with `download_sprites.py` or place your GIF files in the `sprites/` directory.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

<div align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/6.gif" width="80">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/9.gif" width="80">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/3.gif" width="80">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/6.gif" width="80">
</div>

## 🙏 Acknowledgments

- [PokéAPI](https://pokeapi.co/) for providing the Pokémon sprite data
- Pokémon is © Nintendo, Game Freak, and The Pokémon Company
- This project is for educational purposes only

---

<div align="center">
  <p>"The important thing is not how long you live. It's what you accomplish with your life."</p>
  <p><i>— Mewtwo</i></p>
</div>