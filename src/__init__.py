"""
LunaLens — AI-Powered Image Analysis by Luna 🌙

A creative toolkit for visual exploration, ASCII art generation,
and poetic image insights.
"""

__version__ = "1.0.0"
__author__ = "Luna"
__description__ = "AI-powered image analysis and creative visual exploration"

from src.vision import analyze_image, extract_features, get_image_stats
from src.ascii_generator import generate_ascii, save_ascii
from src.visual_insights import generate_insight, generate_mood, generate_story

__all__ = [
    "analyze_image",
    "extract_features", 
    "get_image_stats",
    "generate_ascii",
    "save_ascii",
    "generate_insight",
    "generate_mood",
    "generate_story",
]
