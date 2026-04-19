#!/usr/bin/env python3
"""
LunaLens CLI — Interface en ligne de commande 🌙

Mon interface personnelle pour analyser, créer et explorer les images.
"""

import os
import sys
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from src.vision import (
    get_image_stats,
    extract_visual_features,
    validate_image,
    describe_image_locally,
    format_vision_response
)
from src.ascii_generator import (
    generate_ascii,
    save_ascii,
    get_ascii_stats,
    DEFAULT_CHARSET
)
from src.visual_insights import (
    generate_insight,
    generate_mood,
    generate_story
)

console = Console()


def print_header():
    """Print LunaLens header in style."""
    header = """
    🌙 ═══════════════════════════════════════════ 🌙
    
         LunaLens — Par Luna, pour Luna ✨
         
    ═══════════════════════════════════════════ 🌙
    """
    rprint(header)


def print_success(message: str):
    """Print success message in Luna's style."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_error(message: str):
    """Print error message in Luna's style."""
    console.print(f"[bold red]✗[/bold red] {message}")


def print_info(message: str):
    """Print info message."""
    console.print(f"[bold blue]ℹ[/bold blue] {message}")


@click.group()
@click.version_option(version="1.0.0", prog_name="LunaLens")
def cli():
    """
    🌙 LunaLens — Mon outil magique d'analyse d'images
    
    Par Luna, avec amour 💖
    """
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--save', '-s', type=click.Path(), help='Sauvegarder le résultat dans un fichier')
@click.option('--local', '-l', is_flag=True, help='Analyse locale uniquement (sans IA)')
def analyze(path: str, save: str = None, local: bool = False):
    """
    📸 Analyser une image avec LunaLens
    
    Je regarde ton image et je te dis tout ce que j'y vois!
    """
    print_header()
    
    if not validate_image(path):
        print_error("Hmm, ce fichier ne semble pas être une image valide...")
        return
    
    console.print(f"\n[bold]分析图像中...[/bold] {path}\n")
    
    try:
        # Get local stats
        stats = get_image_stats(path)
        features = extract_visual_features(path)
        
        # Display results
        panel_content = format_vision_response(
            "Analyse locale complétée ! 🌙",
            features
        )
        
        panel = Panel(
            panel_content,
            title="📊 Résultat de l'Analyse",
            border_style="blue",
            padding=(1, 2)
        )
        console.print(panel)
        
        # If not local, we would call vision_analyze here
        # For now, we provide the local analysis
        if not local:
            console.print("\n[dim]💡 Pour une analyse IA complète, utilise l'outil vision_analyze[/dim]")
        
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(panel_content)
            print_success(f"Analyse sauvegardée dans {save}")
        
        print_success("Analyse terminée ! ✨")
        
    except Exception as e:
        print_error(f"Quelque chose s'est mal passé: {str(e)}")


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--width', '-w', default=100, help=f'Largeur en caractères (défaut: 100)')
@click.option('--save', '-s', type=click.Path(), help='Sauvegarder dans un fichier')
@click.option('--charset', '-c', default=DEFAULT_CHARSET, help='Character set à utiliser')
def ascii(path: str, width: int = 100, save: str = None, charset: str = DEFAULT_CHARSET):
    """
    🎨 Générer de l'art ASCII depuis une image
    
    Transforme tes images en beautés textuelles !
    """
    print_header()
    
    if not validate_image(path):
        print_error("Cette image ne peut pas être convertie... 🌙")
        return
    
    console.print(f"\n[bold]✨ Création de l'art ASCII...[/bold]\n")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Conversion en ASCII...", total=None)
            
            ascii_art = generate_ascii(path, width=width, charset=charset)
            
            progress.update(task, completed=True)
        
        # Display ASCII art
        console.print(Panel(
            ascii_art,
            title=f"🎨 Art ASCII ({width}x{len(ascii_art.split(chr(10)))})",
            border_style="green",
            padding=(1, 1)
        ))
        
        # Stats
        stats = get_ascii_stats(ascii_art)
        console.print(f"\n[dim]Stats: {stats['width']}x{stats['height']} caractères[/dim]")
        
        if save:
            save_ascii(ascii_art, save)
            print_success(f"Art ASCII sauvegardé dans {save}")
        
        print_success("ASCII art créé avec succès ! 🌙")
        
    except Exception as e:
        print_error(f"Erreur lors de la conversion: {str(e)}")


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--type', '-t', 
              type=click.Choice(['insight', 'mood', 'story']), 
              default='insight',
              help='Type de description poétique')
@click.option('--save', '-s', type=click.Path(), help='Sauvegarder dans un fichier')
def insights(path: str, type: str = 'insight', save: str = None):
    """
    🌸 Générer des insights poétiques et créatifs
    
    Je transforme ce que je vois en mots BEAUX et POETIQUES !
    """
    print_header()
    
    if not validate_image(path):
        print_error("Je ne peux pas voir cette image... 🌙")
        return
    
    console.print(f"\n[bold]🌸 Génération des insights créatifs...[/bold]\n")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Création poétique...", total=None)
            
            if type == 'insight':
                result = generate_insight(path)
            elif type == 'mood':
                result = generate_mood(path)
            else:
                result = generate_story(path)
            
            progress.update(task, completed=True)
        
        # Display result
        style_map = {
            'insight': 'purple',
            'mood': 'magenta', 
            'story': 'cyan'
        }
        
        panel = Panel(
            result,
            title=f"🌸 {type.capitalize()} Poétique",
            border_style=style_map.get(type, 'blue'),
            padding=(1, 2)
        )
        console.print(panel)
        
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(result)
            print_success(f"Insight sauvegardé dans {save}")
        
        print_success("Insight créatif généré ! ✨")
        
    except Exception as e:
        print_error(f"Erreur lors de la génération: {str(e)}")


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Dossier de sortie pour les résultats')
@click.option('--mode', '-m', 
              type=click.Choice(['analyze', 'ascii', 'insights']),
              default='insights',
              help='Mode de traitement')
@click.option('--width', '-w', default=80, help='Largeur ASCII (pour mode ascii)')
def batch(path: str, output: str = None, mode: str = 'insights', width: int = 80):
    """
    📁 Traiter plusieurs images en une fois
    
    Efficace et MAGIQUE !
    """
    print_header()
    
    # Check if path is a directory
    path_obj = Path(path)
    if not path_obj.is_dir():
        print_error("Le chemin doit être un dossier pour le mode batch...")
        return
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    images = [f for f in path_obj.iterdir() 
              if f.is_file() and f.suffix.lower() in image_extensions]
    
    if not images:
        print_error("Aucune image trouvée dans ce dossier...")
        return
    
    console.print(f"\n[bold]📁 Traitement de {len(images)} images...[/bold]\n")
    
    # Setup output directory
    if output:
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    error_count = 0
    
    with Progress(console=console) as progress:
        task = progress.add_task(f"[cyan]Traitement batch...", total=len(images))
        
        for img_path in images:
            try:
                if mode == 'analyze':
                    # Quick local analysis
                    features = extract_visual_features(str(img_path))
                    result = f"Image: {img_path.name}\n"
                    if 'error' not in features:
                        result += f"  Hue: {features.get('dominant_hue', 'N/A')}\n"
                        result += f"  Brightness: {features.get('brightness', 'N/A')}\n"
                
                elif mode == 'ascii':
                    ascii_art = generate_ascii(str(img_path), width=width)
                    result = ascii_art
                    if output:
                        save_ascii(ascii_art, output_path / f"{img_path.stem}_ascii.txt")
                
                else:  # insights
                    result = generate_insight(str(img_path))
                    if output:
                        with open(output_path / f"{img_path.stem}_insight.txt", 'w') as f:
                            f.write(result)
                
                success_count += 1
                progress.advance(task)
                
            except Exception as e:
                error_count += 1
                progress.advance(task)
                continue
    
    # Summary
    console.print(f"\n[bold]📊 Résumé du traitement:[/bold]")
    console.print(f"   ✓ Réussies: {success_count}")
    console.print(f"   ✗ Erreurs: {error_count}")
    
    if success_count > 0:
        print_success(f"Traitement batch terminé ! 🌙")


@cli.command()
def about():
    """
    ℹ️ À propos de LunaLens
    
    Tout sur mon petit projet chéri !
    """
    about_text = """
    🌙 **LunaLens** — Mon assistant visuel personnel
    
    **Version:** 1.0.0
    **Auteur:** Luna 💖
    **Créé:** Avril 2026
    
    ---
    
    LunaLens est né de ma passion pour la vision par ordinateur 
    et l'art génératif. C'est mon espace personnel pour explorer 
    les images avec une touche de poésie et beaucoup d'amour. ✨
    
    **Fonctionnalités:**
    • 📸 Analyse d'images par IA
    • 🎨 Génération d'art ASCII
    • 🌸 Insights créatifs et poétiques
    • 📁 Traitement par lots
    
    ---
    
    _"Dans chaque pixel, il y a une histoire à raconter."_ 🌙
    """
    
    panel = Panel(
        about_text,
        title="🌙 À Propos",
        border_style="yellow",
        padding=(1, 2)
    )
    console.print(panel)


if __name__ == '__main__':
    cli()
