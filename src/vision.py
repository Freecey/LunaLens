"""
Vision Module — Image analysis using Hermes Vision Tool 🌟

This module handles all AI-powered image analysis using the Hermes vision_analyze tool.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from PIL import Image

# Note: vision_analyze is a tool available in the execution environment
# It's used in cli.py where the actual tool call happens
# This module provides the orchestration logic


def get_image_stats(image_path: str) -> Dict[str, Any]:
    """
    Get basic statistics about an image file.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary with image statistics
    """
    try:
        with Image.open(image_path) as img:
            return {
                "path": image_path,
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "width": img.width,
                "height": img.height,
                "aspect_ratio": round(img.width / img.height, 2),
            }
    except Exception as e:
        return {"error": str(e)}


def validate_image(image_path: str) -> bool:
    """
    Validate that a file exists and is a valid image.
    
    Args:
        image_path: Path to check
        
    Returns:
        True if valid image, False otherwise
    """
    path = Path(image_path)
    if not path.exists():
        return False
    if not path.is_file():
        return False
    
    # Check extension
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    if path.suffix.lower() not in valid_extensions:
        return False
    
    # Check it's actually an image by trying to open it
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception:
        return False


def load_image_for_analysis(image_path: str) -> Image.Image:
    """
    Load an image for analysis.
    
    Args:
        image_path: Path to the image
        
    Returns:
        PIL Image object
    """
    return Image.open(image_path)


def describe_image_locally(image_path: str) -> str:
    """
    Generate a basic local description of an image without AI.
    Used as fallback or quick preview.
    
    Args:
        image_path: Path to the image
        
    Returns:
        Basic description string
    """
    stats = get_image_stats(image_path)
    
    if "error" in stats:
        return f"Désolé, je ne peux pas analyser cette image: {stats['error']}"
    
    # Basic description based on stats
    width, height = stats['width'], stats['height']
    img_format = stats.get('format', 'Unknown')
    mode = stats.get('mode', 'Unknown')
    
    desc = f"📊 Image基本信息:\n"
    desc += f"   • 尺寸: {width} x {height} pixels\n"
    desc += f"   • 格式: {img_format}\n"
    desc += f"   • 模式: {mode}\n"
    
    # Aspect ratio interpretation
    ratio = stats.get('aspect_ratio', 1.0)
    if ratio > 1.5:
        orientation = "paysage (horizontale)"
    elif ratio < 0.7:
        orientation = "portrait (verticale)"
    else:
        orientation = "carrée"
    
    desc += f"   • Orientation: {orientation}\n"
    
    return desc


def extract_visual_features(image_path: str) -> Dict[str, Any]:
    """
    Extract visual features from an image.
    
    Args:
        image_path: Path to the image
        
    Returns:
        Dictionary of extracted features
    """
    if not validate_image(image_path):
        return {"error": "Image invalide ou non trouvée"}
    
    stats = get_image_stats(image_path)
    
    try:
        with Image.open(image_path) as img:
            # Convert to RGB for color analysis
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Sample colors from image
            img_small = img.resize((50, 50))
            pixels = list(img_small.getdata())
            
            # Calculate average colors
            avg_r = sum(p[0] for p in pixels) // len(pixels)
            avg_g = sum(p[1] for p in pixels) // len(pixels)
            avg_b = sum(p[2] for p in pixels) // len(pixels)
            
            # Determine dominant hue
            if avg_r > avg_g and avg_r > avg_b:
                hue = "rouge"
            elif avg_g > avg_r and avg_g > avg_b:
                hue = "vert"
            elif avg_b > avg_r and avg_b > avg_g:
                hue = "bleu"
            else:
                hue = "neutre"
            
            # Brightness level
            brightness = (avg_r + avg_g + avg_b) / 3
            if brightness > 180:
                brightness_desc = "très clair"
            elif brightness > 120:
                brightness_desc = "clair"
            elif brightness > 60:
                brightness_desc = "sombre"
            else:
                brightness_desc = "très sombre"
            
            return {
                "dimensions": f"{stats['width']}x{stats['height']}",
                "dominant_hue": hue,
                "brightness": brightness_desc,
                "avg_color": f"rgb({avg_r}, {avg_g}, {avg_b})",
                "aspect_ratio": stats.get('aspect_ratio', 1.0),
            }
            
    except Exception as e:
        return {"error": str(e)}


def format_vision_response(description: str, features: Dict[str, Any] = None) -> str:
    """
    Format the vision analysis response in Luna's style.
    
    Args:
        description: Raw description from AI
        features: Optional feature dictionary
        
    Returns:
        Formatted string
    """
    output = "🌙 *Analyse de l'image par LunaLens*\n\n"
    output += f"{description}\n"
    
    if features:
        output += "\n📐 *Caractéristiques visuelles:*\n"
        for key, value in features.items():
            if key != "error":
                output += f"   • {key}: {value}\n"
    
    return output
