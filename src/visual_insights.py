"""
Visual Insights — Poetic and creative image descriptions 🌸

Transform simple image analysis into beautiful, poetic interpretations.
"""

import os
from typing import Optional, Dict, Any
from PIL import Image

from src.vision import get_image_stats, extract_visual_features


# Poetic templates for different moods
MOOD_TEMPLATES = {
    "mystical": [
        "Dans la lumière tamisée, je devine les secrets que cette image chuchote...",
        "Les ombres dansent sur la surface, racontant une histoire ancienne...",
        "Il y a quelque chose de_MAGIQUE dans ce moment capturé...",
    ],
    "warm": [
        "Une chaleur DOLCE se dégage de cette image, comme un souvenir précieux...",
        "Les couleurs s'embrassent doucement, créant une atmosphère de bien-être...",
        "On ressent cette lumière COMME un rayon de soleil sur la peau...",
    ],
    "melancholic": [
        "Une douce tristesse flotte dans l'air, BEAU dans sa fragilité...",
        "Les couleurs éteintes racontent une histoire de passages...",
        "Il y a quelque chose de POETIQUE dans cette solitude visuelle...",
    ],
    "energetic": [
        "L'énergie EXPLOSE dans chaque recoin de cette image !",
        "Une puissance VIVE pulse à travers les couleurs et les formes...",
        "Le mouvement est FIGÉ dans le temps, mais pas sa dynamique !",
    ],
    "serene": [
        "Un calme PARFAIT émane de cette composition...",
        "La simplicité de cette image respire la tranquillité...",
        "Un moment de PAIX visuelle, comme un lac sans vagues...",
    ],
}

STORY_STARTERS = [
    "Il était une fois, dans un coin de cette image...",
    "Cette scène cache un secret que seuls les yeux patients découvrent...",
    "Si cette image pouvait parler, elle dirait...",
    "Un jour, quelque chose dans cette photo a changé...",
    "Les couleurs racontent ce que les mots ne peuvent dire...",
]


def determine_mood_from_features(features: Dict[str, Any]) -> str:
    """
    Determine the mood category based on visual features.
    
    Args:
        features: Dictionary of visual features
        
    Returns:
        Mood category string
    """
    if "error" in features:
        return "mystical"
    
    hue = features.get("dominant_hue", "")
    brightness = features.get("brightness", "")
    
    if brightness in ["très sombre", "sombre"]:
        return "mystical"
    elif brightness in ["très clair", "clair"]:
        if hue in ["rouge", "orange"]:
            return "warm"
        return "serene"
    else:
        if hue in ["bleu", "vert"]:
            return "melancholic"
        return "warm"


def generate_insight(image_path: str) -> str:
    """
    Generate a poetic insight about an image.
    
    Args:
        image_path: Path to the image
        
    Returns:
        Poetic description string
    """
    if not os.path.exists(image_path):
        return "Cette image semble ne pas exister... peut-être est-elle quelque part dans mes rêves? 🌙"
    
    features = extract_visual_features(image_path)
    stats = get_image_stats(image_path)
    mood = determine_mood_from_features(features)
    
    import random
    
    # Build poetic response
    response = "🌸 *Voici ce que mes yeux de Lune perçoivent...*\n\n"
    
    # Add poetic mood line
    mood_line = random.choice(MOOD_TEMPLATES[mood])
    response += f"_{mood_line}_\n\n"
    
    # Add visual analysis
    response += "📷 *Analyse visuelle:*\n"
    
    if "error" not in features:
        response += f"   • Teinte dominante: {features.get('dominant_hue', 'mystérieuse')}\n"
        response += f"   • Luminosité: {features.get('brightness', 'énigmatique')}\n"
        response += f"   • Dimensions: {features.get('dimensions', 'infinies')}\n"
    
    if "error" not in stats:
        ratio = stats.get('aspect_ratio', 1.0)
        if ratio > 1.5:
            response += "   • Cette image aime s'étirer vers l'horizon...\n"
        elif ratio < 0.7:
            response += "   • Elle se dresse fièrement vers le ciel...\n"
        else:
            response += "   • Une forme équilibrée, presque parfaite...\n"
    
    response += "\n💫 *Mon ressenti:* Cette image a quelque chose de SPECIAL, tu sais? "
    response += "Elle me parle de..."
    
    # Add personalized endings
    endings = [
        "beaux souvenirs qui attendent d'être découverts",
        "moments suspendu dans le temps",
        "possibilités infinies de créatures visuelles",
        "la beauté simple qui nous entoure",
        "l'art de voir au-delà des apparences",
    ]
    response += random.choice(endings) + " ✨"
    
    return response


def generate_mood(image_path: str) -> str:
    """
    Generate an emotional mood description of an image.
    
    Args:
        image_path: Path to the image
        
    Returns:
        Mood description string
    """
    if not os.path.exists(image_path):
        return "Aucun mood à détecter... l'image m'échappe 🌑"
    
    features = extract_visual_features(image_path)
    mood = determine_mood_from_features(features)
    
    import random
    
    mood_descriptions = {
        "mystical": {
            "emoji": "🔮",
            "title": "Ambiance Mystique",
            "description": "Tu es entré dans un espace où la réalité et l'imagination se confondent...",
            "colors": ["violet profond", "bleu nuit", "argent"],
        },
        "warm": {
            "emoji": "🌻",
            "title": "ChaleurAccueillante",
            "description": "Une atmosphère douce et réconfortante t'enveloppe...",
            "colors": ["jaune doré", "orange doux", "rose pâle"],
        },
        "melancholic": {
            "emoji": "🌧️",
            "title": "Tristesse Belle",
            "description": "Il y a de la beauté dans cette mélancolie, COMME une chanson douce-amère...",
            "colors": ["bleu gris", "vert triste", "violet éteint"],
        },
        "energetic": {
            "emoji": "⚡",
            "title": "Énergie Explosive",
            "description": "La puissance crépite dans cette image! On ne peut pas rester indifférent...",
            "colors": ["rouge vif", "jaune éclatant", "orange brûlant"],
        },
        "serene": {
            "emoji": "🧘",
            "title": "Calme Parfait",
            "description": "Respire... tu es maintenant dans un espace de paix visuelle...",
            "colors": ["bleu ciel", "vert menthe", "blanc pur"],
        },
    }
    
    info = mood_descriptions[mood]
    
    output = f"{info['emoji']} **{info['title']}**\n\n"
    output += f"_{info['description']}_\n\n"
    output += "🎨 Couleurs dominantes: " + ", ".join(info['colors']) + "\n"
    
    if "error" not in features:
        output += f"🌡️ Température perçue: "
        if mood in ["warm", "energetic"]:
            output += "Chaude\n"
        elif mood in ["mystical", "melancholic"]:
            output += "Fraiche\n"
        else:
            output += "Neutre\n"
    
    return output


def generate_story(image_path: str) -> str:
    """
    Generate a short creative story about an image.
    
    Args:
        image_path: Path to the image
        
    Returns:
        Short creative story string
    """
    if not os.path.exists(image_path):
        return "Je ne peux pas inventer d'histoire pour une image qui n'existe pas... 🌙"
    
    import random
    
    stats = get_image_stats(image_path)
    features = extract_visual_features(image_path)
    
    starter = random.choice(STORY_STARTERS)
    
    # Build story based on image properties
    story = f"✨ *{starter}*\n\n"
    
    if "error" not in stats:
        dimensions = f"{stats.get('width', '?')}x{stats.get('height', '?')}"
        story += f"_Une image de {dimensions} pixels, comme un petit univers fractal..._\n\n"
    
    # Generate story content
    story_lines = [
        "Les premières lueurs de l'aube ont effleuré ce moment,\n",
        "Les ombres s'allongeèrent lentement,\n",
        "Quelque part, un souvenir se cache dans ces pixels,\n",
        "Le temps semble suspendu entre ces couleurs,\n",
        "Chaque détail raconte une parcelle d'éternité,\n",
    ]
    
    # Select 3 random story lines
    selected = random.sample(story_lines, 3)
    for line in selected:
        story += f"  {line.strip()}\n"
    
    story += "\n🌙 *Et toi, qu'imagines-tu en regardant cette image?*"
    
    return story


def get_poetic_color_name(rgb: tuple) -> str:
    """
    Convert RGB color to a poetic French color name.
    
    Args:
        rgb: Tuple of (R, G, B) values
        
    Returns:
        Poetic color name in French
    """
    r, g, b = rgb
    
    # Simple color mapping
    if r > 200 and g < 100 and b < 100:
        return "Rouge passion"
    elif r > 200 and g > 200 and b < 100:
        return "Or solaire"
    elif r < 100 and g > 200 and b < 100:
        return "Vert espoir"
    elif r < 100 and g > 150 and b > 200:
        return "Cyan rêveur"
    elif r > 150 and g < 100 and b > 200:
        return "Violet mystique"
    elif r > 200 and g > 200 and b > 200:
        return "Blanc innocence"
    elif r < 50 and g < 50 and b < 50:
        return "Noir profond"
    elif r > 150 and g > 100 and b < 100:
        return "Corail chaleureux"
    elif r > 200 and g > 150 and b > 100:
        return "Pêche doux"
    else:
        return "Couleur indéchiffrable"
