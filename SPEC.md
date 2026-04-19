# LunaLens — Technical Specification

## Overview

**Project Name:** LunaLens  
**Type:** AI-Powered Image Analysis Tool  
**Author:** Luna  
**Purpose:** Creative visual analysis, ASCII art generation, and poetic image insights  
**Target Users:** Luna (personal use), creative professionals, AI enthusiasts

---

## Architecture

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Language | Python 3.x | Core implementation |
| Image Processing | Pillow (PIL) | Image loading, manipulation |
| CLI Framework | Click | Command-line interface |
| UI Formatting | Rich | Terminal beautification |
| Testing | pytest | Unit testing |
| Vision AI | Hermes Vision Tool | Image analysis via `vision_analyze` |

### Directory Structure

```
lunalens/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── vision.py             # Vision analysis module
│   ├── ascii_generator.py    # ASCII art generation
│   ├── visual_insights.py    # Poetic descriptions
│   └── cli.py                # CLI entry point
├── tests/
│   └── test_lunalens.py      # Unit tests
├── data/
│   └── sample_images/        # Test images directory
├── notebooks/
│   └── exploration.ipynb     # Jupyter exploration
├── requirements.txt          # Dependencies
├── .gitignore                # Git ignore patterns
├── README.md                 # Project overview
└── SPEC.md                   # This specification
```

---

## Functionality Specification

### 1. Vision Module (`src/vision.py`)

**Purpose:** Analyze images using Hermes Vision Tool to extract descriptive information and features.

**Functions:**
- `analyze_image(image_path: str) -> str` — Returns detailed description of the image
- `extract_features(image_path: str) -> dict` — Extracts visual features (colors, objects, scene type)
- `get_image_stats(image_path: str) -> dict` — Returns basic image statistics (dimensions, format, mode)

**Implementation:**
- Load image using Pillow
- Pass image bytes to `vision_analyze` tool
- Parse and format the AI response
- Return structured or raw text results

### 2. ASCII Generator (`src/ascii_generator.py`)

**Purpose:** Convert images to ASCII art using character-based rendering.

**Functions:**
- `generate_ascii(image_path: str, width: int = 100, chars: str = None) -> str`
  - `image_path`: Path to input image
  - `width`: Output width in characters (default: 100)
  - `chars`: Custom character set for shading (optional)
  - Returns: ASCII art string

- `save_ascii(ascii_art: str, output_path: str) -> None` — Save ASCII to file

**Character Mapping:**
- Default charset: ` .:-=+*#%@` (light to dark)
- Custom charset support for artistic variation

**Processing Pipeline:**
1. Load image and convert to grayscale
2. Resize to target width maintaining aspect ratio
3. Map each pixel brightness to a character
4. Build string row by row

### 3. Visual Insights (`src/visual_insights.py`)

**Purpose:** Generate poetic, creative, and philosophical descriptions of images.

**Functions:**
- `generate_insight(image_path: str) -> str` — Returns poetic interpretation
- `generate_mood(image_path: str) -> str` — Returns emotional/mood description
- `generate_story(image_path: str) -> str` — Returns a short creative story about the image

**Implementation:**
- Uses `vision_analyze` to get base description
- Applies creative transformation and stylization
- Adds poetic language, metaphors, and personal touch
- Returns formatted Rich-formatted text

### 4. CLI Interface (`src/cli.py`)

**Purpose:** Command-line interface with Rich-formatted output.

**Commands:**

| Command | Description | Options |
|---------|-------------|---------|
| `analyze` | Analyze image content | `--path`, `--save` |
| `ascii` | Generate ASCII art | `--path`, `--width`, `--save` |
| `insights` | Generate poetic insights | `--path`, `--type` (insight/mood/story) |
| `batch` | Process multiple images | `--path` (directory), `--output` |

**Global Options:**
- `--verbose` — Enable verbose output
- `--output` — Save result to file

**Features:**
- Rich console output with colors and formatting
- Progress bars for batch operations
- Error handling with friendly messages
- Help text in Luna's personal style

---

## Data Flow

```
User Input (CLI)
      │
      ▼
┌─────────────┐
│  cli.py     │  ─── Command routing, Rich formatting
└─────────────┘
      │
      ▼
┌─────────────┐     ┌──────────────────┐
│ vision.py   │────▶│ vision_analyze   │  ─── Hermes AI
└─────────────┘     └──────────────────┘
      │
      ▼
┌─────────────┐
│ascii_gen.py │  ─── PIL processing
└─────────────┘
      │
      ▼
┌─────────────┐
│insights.py  │  ─── Creative transformation
└─────────────┘
```

---

## API Specification

### Vision Analysis

```python
def analyze_image(image_path: str) -> str:
    """
    Analyze an image using Hermes Vision.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Detailed text description of the image
    """
```

### ASCII Generation

```python
def generate_ascii(image_path: str, width: int = 100, 
                   chars: str = None, output_path: str = None) -> str:
    """
    Generate ASCII art from an image.
    
    Args:
        image_path: Path to input image
        width: Width of output in characters
        chars: Character set for shading (default: ' .:-=+*#%@')
        output_path: Optional path to save ASCII art
        
    Returns:
        ASCII art string
    """
```

### Visual Insights

```python
def generate_insight(image_path: str) -> str:
    """
    Generate poetic insight about an image.
    
    Args:
        image_path: Path to the image
        
    Returns:
        Poetic/creative description
    """
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LUNALENS_DEFAULT_WIDTH` | 100 | Default ASCII art width |
| `LUNALENS_CHARSET` | ` .:-=+*#%@` | Default ASCII character set |
| `LUNALENS_VERBOSE` | false | Enable verbose logging |

### CLI Defaults

- ASCII width: 100 characters
- Output format: Terminal (Rich formatting)
- Batch chunk size: 10 images

---

## Testing Strategy

### Unit Tests (`tests/test_lunalens.py`)

**Test Categories:**

1. **Vision Module Tests**
   - Test image analysis with valid image
   - Test feature extraction
   - Test error handling for invalid paths

2. **ASCII Generator Tests**
   - Test basic ASCII generation
   - Test custom width
   - Test custom character sets
   - Test output saving

3. **Visual Insights Tests**
   - Test insight generation
   - Test mood extraction
   - Test story generation

4. **CLI Tests**
   - Test analyze command
   - Test ascii command
   - Test insights command
   - Test batch processing
   - Test error cases

**Test Data:**
- Sample images in `data/sample_images/`
- Mock responses for Hermes Vision (if unavailable)

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| File not found | Friendly message + exit code 1 |
| Invalid image format | Suggest supported formats |
| Vision API failure | Graceful degradation + local fallback |
| Permission denied | Clear error message |

---

## Future Enhancements (v1.1+)

- [ ] Support for video frame analysis
- [ ] Batch ASCII art export to HTML
- [ ] Custom themes for ASCII art
- [ ] Integration with additional AI models
- [ ] Web interface / API

---

## Dependencies

```
Pillow>=10.0.0
rich>=13.0.0
click>=8.0.0
pytest>=7.0.0
```

---

*Spec version: 1.0*  
*Last updated: April 2026*
