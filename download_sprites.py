import os
import requests
import argparse
from tqdm import tqdm

def download_pokemon_sprite(pokemon_id, output_dir="sprites"):
    """
    Download animated Pokémon sprite GIF from the PokeAPI GitHub repository
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # URLs for different sprite repositories
    urls = [
        # Main Pokémon animated sprites (Gen 5 style)
        f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/{pokemon_id}.gif",
        # Shiny animated sprites
        f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/shiny/{pokemon_id}.gif",
        # Fallback to static sprites if animated not available
        f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
    ]
    
    for url in urls:
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # Determine the output filename
                if "shiny" in url:
                    output_file = os.path.join(output_dir, f"{pokemon_id}_shiny.gif")
                elif url.endswith(".png"):
                    output_file = os.path.join(output_dir, f"{pokemon_id}.png")
                else:
                    output_file = os.path.join(output_dir, f"{pokemon_id}.gif")
                
                # Get file size for progress bar
                total_size = int(response.headers.get('content-length', 0))
                
                # Download with progress bar
                with open(output_file, 'wb') as f, tqdm(
                    desc=f"Downloading {os.path.basename(output_file)}",
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for data in response.iter_content(chunk_size=1024):
                        size = f.write(data)
                        bar.update(size)
                
                print(f"Downloaded: {output_file}")
                
                # If we successfully downloaded one version, continue to the next Pokémon
                if not "shiny" in url:
                    break
            
        except Exception as e:
            print(f"Error downloading from {url}: {e}")
    
    return os.path.exists(output_file)

def main():
    parser = argparse.ArgumentParser(description="Download Pokémon sprite GIFs")
    parser.add_argument("pokemon", type=int, nargs="*", 
                      help="Pokémon ID numbers to download (1-898 for main series)")
    parser.add_argument("--range", type=str, help="Range of Pokémon IDs to download (e.g., '1-151')")
    parser.add_argument("--output", "-o", type=str, default="sprites", 
                      help="Output directory for sprites")
    
    args = parser.parse_args()
    
    pokemon_ids = []
    
    # Process individual Pokémon IDs
    if args.pokemon:
        pokemon_ids.extend(args.pokemon)
    
    # Process range of Pokémon IDs
    if args.range:
        try:
            start, end = map(int, args.range.split('-'))
            pokemon_ids.extend(range(start, end + 1))
        except ValueError:
            print(f"Invalid range format: {args.range}. Use 'start-end' format.")
    
    # Default to first 151 Pokémon if no arguments provided
    if not pokemon_ids:
        print("No Pokémon IDs specified. Downloading the original 151 Pokémon.")
        pokemon_ids = range(1, 152)
    
    # Remove duplicates and sort
    pokemon_ids = sorted(set(pokemon_ids))
    
    # Download sprites
    success_count = 0
    for pokemon_id in pokemon_ids:
        if download_pokemon_sprite(pokemon_id, args.output):
            success_count += 1
    
    print(f"\nDownloaded {success_count} Pokémon sprites to {args.output}/")

if __name__ == "__main__":
    main()