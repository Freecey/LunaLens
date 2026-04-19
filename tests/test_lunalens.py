"""
Tests for LunaLens — Unit tests for all modules 🌙
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from PIL import Image
import io

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.vision import (
    get_image_stats,
    validate_image,
    extract_visual_features,
    describe_image_locally,
    format_vision_response,
    load_and_preprocess
)
from src.ascii_generator import (
    generate_ascii,
    save_ascii,
    pixel_to_char,
    get_ascii_stats,
    create_ascii_banner,
    DEFAULT_CHARSET
)
from src.visual_insights import (
    generate_insight,
    generate_mood,
    generate_story,
    determine_mood_from_features,
    get_poetic_color_name
)


# Fixtures
@pytest.fixture
def test_image_path(tmp_path):
    """Create a temporary test image."""
    # Create a simple test image (100x100 red square)
    img = Image.new('RGB', (100, 100), color='red')
    img_path = tmp_path / "test_image.png"
    img.save(img_path)
    return str(img_path)


@pytest.fixture
def grayscale_image_path(tmp_path):
    """Create a grayscale test image."""
    img = Image.new('L', (50, 50), color=128)
    img_path = tmp_path / "gray_image.png"
    img.save(img_path)
    return str(img_path)


@pytest.fixture
def invalid_path():
    """Return an invalid path for error testing."""
    return "/nonexistent/path/to/image.png"


# Vision Module Tests
class TestVisionModule:
    """Tests for vision.py module."""
    
    def test_get_image_stats_valid(self, test_image_path):
        """Test getting stats from a valid image."""
        stats = get_image_stats(test_image_path)
        assert 'error' not in stats
        assert stats['width'] == 100
        assert stats['height'] == 100
        assert stats['format'] == 'PNG'
    
    def test_get_image_stats_invalid(self, invalid_path):
        """Test getting stats from invalid path."""
        stats = get_image_stats(invalid_path)
        assert 'error' in stats
    
    def test_validate_image_valid(self, test_image_path):
        """Test image validation with valid image."""
        assert validate_image(test_image_path) is True
    
    def test_validate_image_invalid(self, invalid_path):
        """Test image validation with invalid path."""
        assert validate_image(invalid_path) is False
    
    def test_validate_image_wrong_extension(self, tmp_path):
        """Test validation with wrong extension."""
        fake_file = tmp_path / "fake.txt"
        fake_file.write_text("not an image")
        assert validate_image(str(fake_file)) is False
    
    def test_extract_visual_features(self, test_image_path):
        """Test visual feature extraction."""
        features = extract_visual_features(test_image_path)
        assert 'error' not in features
        assert 'dominant_hue' in features
        assert 'brightness' in features
        assert 'dimensions' in features
    
    def test_extract_visual_features_invalid(self, invalid_path):
        """Test feature extraction with invalid path."""
        features = extract_visual_features(invalid_path)
        assert 'error' in features
    
    def test_describe_image_locally(self, test_image_path):
        """Test local image description."""
        desc = describe_image_locally(test_image_path)
        assert '100 x 100' in desc or '100x100' in desc
    
    def test_format_vision_response(self):
        """Test response formatting."""
        response = format_vision_response(
            "Test description",
            {"key": "value"}
        )
        assert "Test description" in response
        assert "key" in response


# ASCII Generator Tests
class TestAsciiGenerator:
    """Tests for ascii_generator.py module."""
    
    def test_pixel_to_char(self):
        """Test pixel to character mapping."""
        # White pixel (255) should get light character
        char_white = pixel_to_char(255)
        # Black pixel (0) should get dark character
        char_black = pixel_to_char(0)
        # Light char should come before dark char in default charset
        assert DEFAULT_CHARSET.index(char_white) < DEFAULT_CHARSET.index(char_black)
    
    def test_generate_ascii_valid(self, test_image_path):
        """Test ASCII generation with valid image."""
        ascii_art = generate_ascii(test_image_path, width=50)
        assert isinstance(ascii_art, str)
        assert len(ascii_art) > 0
        # Should have newlines
        assert '\n' in ascii_art
    
    def test_generate_ascii_custom_width(self, test_image_path):
        """Test ASCII generation with custom width."""
        ascii_50 = generate_ascii(test_image_path, width=50)
        ascii_100 = generate_ascii(test_image_path, width=100)
        # 100 should be wider than 50
        assert len(ascii_100.split('\n')[0]) > len(ascii_50.split('\n')[0])
    
    def test_generate_ascii_custom_charset(self, test_image_path):
        """Test ASCII generation with custom charset."""
        custom = ".*#"
        ascii_art = generate_ascii(test_image_path, width=20, charset=custom)
        # All characters should be from custom charset
        for char in ascii_art.replace('\n', ''):
            assert char in custom
    
    def test_generate_ascii_invalid_path(self, invalid_path):
        """Test ASCII generation with invalid path."""
        with pytest.raises(FileNotFoundError):
            generate_ascii(invalid_path)
    
    def test_save_ascii(self, tmp_path):
        """Test saving ASCII art to file."""
        ascii_content = "Test\nASCII\nArt"
        output_path = tmp_path / "output.txt"
        save_ascii(ascii_content, str(output_path))
        assert output_path.exists()
        assert output_path.read_text() == ascii_content
    
    def test_get_ascii_stats(self):
        """Test ASCII stats calculation."""
        ascii_art = "abc\ndefgh\nij"
        stats = get_ascii_stats(ascii_art)
        assert stats['width'] == 5
        assert stats['height'] == 3
        assert stats['total_chars'] == 11
    
    def test_create_ascii_banner(self):
        """Test ASCII banner creation."""
        banner = create_ascii_banner("TEST", width=20)
        assert "TEST" in banner
        assert "+" in banner
        assert "-" in banner


# Visual Insights Tests
class TestVisualInsights:
    """Tests for visual_insights.py module."""
    
    def test_generate_insight_valid(self, test_image_path):
        """Test insight generation with valid image."""
        insight = generate_insight(test_image_path)
        assert isinstance(insight, str)
        assert len(insight) > 0
        assert "🌸" in insight or "mes yeux" in insight.lower()
    
    def test_generate_insight_invalid(self, invalid_path):
        """Test insight generation with invalid path."""
        insight = generate_insight(invalid_path)
        assert "existe" in insight.lower() or "pas" in insight.lower()
    
    def test_generate_mood_valid(self, test_image_path):
        """Test mood generation with valid image."""
        mood = generate_mood(test_image_path)
        assert isinstance(mood, str)
        assert len(mood) > 0
        assert "🌡️" in mood or "Ambiance" in mood
    
    def test_generate_mood_invalid(self, invalid_path):
        """Test mood generation with invalid path."""
        mood = generate_mood(invalid_path)
        assert "mood" in mood.lower() or "aucun" in mood.lower()
    
    def test_generate_story_valid(self, test_image_path):
        """Test story generation with valid image."""
        story = generate_story(test_image_path)
        assert isinstance(story, str)
        assert len(story) > 0
        assert "✨" in story or "." in story
    
    def test_generate_story_invalid(self, invalid_path):
        """Test story generation with invalid path."""
        story = generate_story(invalid_path)
        assert "existe" in story.lower() or "pas" in story.lower()
    
    def test_determine_mood_from_features(self):
        """Test mood determination from features."""
        # Test different feature combinations
        mystical = {"dominant_hue": "bleu", "brightness": "très sombre"}
        warm = {"dominant_hue": "rouge", "brightness": "très clair"}
        
        mood_mystical = determine_mood_from_features(mystical)
        mood_warm = determine_mood_from_features(warm)
        
        assert mood_mystical in ["mystical", "melancholic"]
        assert mood_warm == "warm"
    
    def test_get_poetic_color_name(self):
        """Test poetic color name generation."""
        # Test various colors
        assert "Rouge" in get_poetic_color_name((255, 50, 50))
        assert "Or" in get_poetic_color_name((255, 255, 100))
        assert "Vert" in get_poetic_color_name((50, 255, 50))


# Integration Tests
class TestIntegration:
    """Integration tests for the full LunaLens pipeline."""
    
    def test_full_pipeline(self, test_image_path):
        """Test full analysis pipeline."""
        # Get stats
        stats = get_image_stats(test_image_path)
        assert stats['width'] == 100
        
        # Generate ASCII
        ascii_art = generate_ascii(test_image_path, width=40)
        assert len(ascii_art) > 0
        
        # Generate insights
        insight = generate_insight(test_image_path)
        assert len(insight) > 0
    
    def test_batch_ready_outputs(self, test_image_path, tmp_path):
        """Test that batch-style outputs work."""
        # Generate multiple outputs
        ascii_art = generate_ascii(test_image_path, width=30)
        ascii_path = tmp_path / "test_ascii.txt"
        save_ascii(ascii_art, str(ascii_path))
        
        insight = generate_insight(test_image_path)
        insight_path = tmp_path / "test_insight.txt"
        with open(insight_path, 'w') as f:
            f.write(insight)
        
        assert ascii_path.exists()
        assert insight_path.exists()


# Error Handling Tests
class TestErrorHandling:
    """Tests for error handling."""
    
    def test_nonexistent_file_vision(self, invalid_path):
        """Test handling of nonexistent file in vision module."""
        stats = get_image_stats(invalid_path)
        assert 'error' in stats
    
    def test_nonexistent_file_ascii(self, invalid_path):
        """Test handling of nonexistent file in ASCII generator."""
        with pytest.raises(FileNotFoundError):
            generate_ascii(invalid_path)
    
    def test_nonexistent_file_insights(self, invalid_path):
        """Test handling of nonexistent file in insights."""
        insight = generate_insight(invalid_path)
        assert "existe" in insight.lower() or "pas" in insight.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
