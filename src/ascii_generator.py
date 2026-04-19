"""
ASCII Generator — Transform images into ASCII art 🎨

Using PIL to convert images into beautiful character-based artwork.
"""

import os
from pathlib import Path
from typing import Optional, List, Tuple
from PIL import Image, ImageOps


# Default character set from light to dark
DEFAULT_CHARSET = ' .:-=+*#%@'
COMPACT_CHARSET = ' .:#@'
DETAILED_CHARSET = " .',-':;=+*#%@"


def load_and_preprocess(image_path: str, target_width: int) -> Image.Image:
    """
    Load an image and preprocess it for ASCII conversion.
    
    Args:
        image_path: Path to the input image
        target_width: Desired width in characters
        
    Returns:
        Grayscale PIL Image resized for ASCII output
    """
    img = Image.open(image_path)
    
    # Convert to grayscale
    img = ImageOps.grayscale(img)
    
    # Calculate new height to maintain aspect ratio
    # Assuming characters are taller than wide (typically 2:1 ratio)
    aspect_ratio = img.height / img.width
    target_height = int(target_width * aspect_ratio * 0.5)
    
    # Resize
    img = img.resize((target_width, target_height))
    
    return img


def pixel_to_char(pixel_value: int, charset: str = DEFAULT_CHARSET) -> str:
    """
    Map a pixel grayscale value (0-255) to an ASCII character.
    
    Args:
        pixel_value: Grayscale value (0 = black, 255 = white)
        charset: Character set to use
        
    Returns:
        ASCII character
    """
    # Invert because in ASCII art, low values = dark chars
    # But our charset goes light to dark, so we invert
    index = int((255 - pixel_value) / 255 * (len(charset) - 1))
    return charset[max(0, min(len(charset) - 1, index))]


def generate_ascii(image_path: str, 
                   width: int = 100, 
                   charset: str = None,
                   output_path: Optional[str] = None) -> str:
    """
    Generate ASCII art from an image.
    
    Args:
        image_path: Path to the input image
        width: Width of output in characters (default: 100)
        charset: Character set to use (default: ' .:-=+*#%@')
        output_path: Optional path to save the ASCII art
        
    Returns:
        ASCII art string
    """
    if charset is None:
        charset = DEFAULT_CHARSET
    
    # Validate image
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"L'image n'existe pas: {image_path}")
    
    # Load and preprocess
    img = load_and_preprocess(image_path, width)
    
    # Generate ASCII
    ascii_lines = []
    for y in range(img.height):
        line = ""
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            char = pixel_to_char(pixel, charset)
            line += char
        ascii_lines.append(line)
    
    ascii_art = "\n".join(ascii_lines)
    
    # Save if output path provided
    if output_path:
        save_ascii(ascii_art, output_path)
    
    return ascii_art


def save_ascii(ascii_art: str, output_path: str) -> None:
    """
    Save ASCII art to a text file.
    
    Args:
        ascii_art: ASCII art string
        output_path: Path to save to
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ascii_art)


def generate_colored_ascii(image_path: str,
                           width: int = 80,
                           output_path: Optional[str] = None) -> Tuple[str, List[Tuple[int, int, int]]]:
    """
    Generate ASCII art with color information for each character.
    
    Args:
        image_path: Path to input image
        width: Width in characters
        output_path: Optional path to save
        
    Returns:
        Tuple of (ASCII string, list of average colors per row)
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"L'image n'existe pas: {image_path}")
    
    img = Image.open(image_path)
    
    # Calculate dimensions
    aspect_ratio = img.height / img.width
    target_height = int(width * aspect_ratio * 0.5)
    
    # Resize
    img = img.resize((width, target_height))
    
    # Generate ASCII with color preservation
    ascii_lines = []
    row_colors = []
    
    for y in range(img.height):
        line = ""
        row_colors_list = []
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            if isinstance(pixel, int):
                # Grayscale
                gray = pixel
                row_colors_list.append((gray, gray, gray))
            else:
                # RGB
                row_colors_list.append(pixel[:3])
            
            # Get character for grayscale value
            if isinstance(pixel, int):
                char = pixel_to_char(pixel, DEFAULT_CHARSET)
            else:
                # Use average for color images
                gray = sum(pixel[:3]) // 3
                char = pixel_to_char(gray, DEFAULT_CHARSET)
            line += char
        
        ascii_lines.append(line)
        row_colors.append(row_colors_list[0] if row_colors_list else (128, 128, 128))
    
    ascii_art = "\n".join(ascii_lines)
    
    if output_path:
        save_ascii(ascii_art, output_path)
    
    return ascii_art, row_colors


def get_ascii_stats(ascii_art: str) -> dict:
    """
    Get statistics about generated ASCII art.
    
    Args:
        ascii_art: ASCII art string
        
    Returns:
        Dictionary with statistics
    """
    lines = ascii_art.split('\n')
    return {
        "width": max(len(line) for line in lines) if lines else 0,
        "height": len(lines),
        "total_chars": sum(len(line) for line in lines),
        "unique_chars": len(set(''.join(lines))),
    }


def create_ascii_banner(text: str, width: int = 80) -> str:
    """
    Create a simple ASCII banner from text.
    
    Args:
        text: Text to convert to banner
        width: Width of banner
        
    Returns:
        ASCII banner string
    """
    border = "+" + "-" * (width - 2) + "+"
    padding = (width - len(text) - 2) // 2
    text_line = "|" + " " * padding + text + " " * (width - padding - len(text) - 2) + "|"
    
    return f"\n{border}\n{text_line}\n{border}\n"
