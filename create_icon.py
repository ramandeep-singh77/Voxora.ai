#!/usr/bin/env python3
"""
Create a simple icon for Voxora.AI
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple icon"""
    # Create a 256x256 image with transparent background
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a circle background
    circle_color = (0, 123, 255, 255)  # Blue
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin], fill=circle_color)
    
    # Try to draw the hand emoji or text
    try:
        # Try to use a font
        font_size = 120
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None
    
    # Draw the hand emoji or "V" for Voxora
    text = "🤟"
    if font:
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    else:
        # Fallback: draw "V" for Voxora
        text = "V"
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        draw.text((x, y), text, fill=(255, 255, 255, 255))
    
    # Save as ICO
    img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("✅ Icon created: icon.ico")

if __name__ == "__main__":
    try:
        create_icon()
    except Exception as e:
        print(f"⚠️  Could not create icon: {e}")
        print("   Continuing without icon...")