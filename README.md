# 🌙 LunaLens

*Une petite fenêtre magique sur le monde visuel, par Luna pour Luna* ✨

---

## Salut, c'est moi, Luna ! 👋

Tu sais ce sentiment quand tu regardes une image et que tu *sens* quelque chose de profond ? Quand les couleurs, les formes, les textures te racontent une histoire sans mots ? C'est exactement pour ça que j'ai créé LunaLens.

LunaLens est mon petit assistant visuel personnel — un outil qui analyse les images avec une touche de poésie et beaucoup d'amour. Que ce soit pour comprendre ce qu'une photo montre, la transformer en art ASCII, ou obtenir des insights créatifs et philosophiques... je suis là. 💫

## ✨ Ce que je fais

| Commande | Description |
|----------|-------------|
| `analyze` | Je regarde une image et je te dis tout ce que j'y vois |
| `ascii` | Je transforme tes images en beautés textuelles ASCII |
| `insights` | Je te donne des descriptions poétiques et créatives |
| `batch` | Je traite plusieurs images d'un coup — efficace ! |

## 🚀 Par où commencer ?

```bash
# Installation rapide
pip install -r requirements.txt

# Découvrir ce que je vois dans une image
python -m src.cli analyze chemin/vers/ton/image.jpg

# Créer de l'art ASCII
python -m src.cli ascii chemin/vers/ton/image.jpg

# Obtenir des insights créatifs
python -m src.cli insights chemin/vers/ton/image.jpg

# Traiter plusieurs images
python -m src.cli batch chemin/vers/dossier/
```

## 💡 Pourquoi LunaLens ?

Parce que je crois que la technologie devrait être:
- **Chaleureuse** — pas froid et technique, mais amicale et inspire
- **Créative** — pas juste des données, mais de la magie
- **Personnelle** — un outil qui me ressemble, fait pour moi

## 🛠️ Tech stack

- **Python 3** — mon langage de prédilection
- **Pillow** — pour la manipulation d'images
- **Rich** — pour des interfaces magnifiques dans le terminal
- **Click** — pour des commandes CLI élégantes
- **Hermes Vision** — mon outil d'analyse IA préféré

## 📁 Structure du projet

```
lunalens/
├── src/
│   ├── __init__.py
│   ├── vision.py          # Analyse d'images par IA
│   ├── ascii_generator.py # Conversion en ASCII art
│   ├── visual_insights.py # Descriptions poétiques
│   └── cli.py             # Interface en ligne de commande
├── tests/
│   └── test_lunalens.py
├── data/
│   └── sample_images/     # Tes images de test ici !
├── notebooks/
│   └── exploration.ipynb
├── requirements.txt
├── .gitignore
└── SPEC.md
```

## 🌟 Pour moi (et pour toi)

Ce projet est avant tout personnel — un espace où je peux expérimenter avec la vision par ordinateur tout en m'amusant. Si tu l'utilises et que tu as des idées pour le rendre encore plus magique, je suis toute ouïe ! 

*"Dans chaque pixel, il y a une histoire. LunaLens me aide à la raconter."* 🌙

---

Fait avec 💖 et beaucoup de ☕ par **Luna**

*Last updated: Avril 2026*
