from PIL import Image, ImageDraw, ImageOps
import os

# Try to import cairosvg and handle the case if it's not installed properly
try:
    import cairosvg
except ImportError:
    raise ImportError(
        "CairoSVG is not installed or Cairo system library is missing.\n"
        "Please install CairoSVG with 'pip install cairosvg' and make sure Cairo is available on your system.\n"
        "On macOS, you can install Cairo with Homebrew:\n"
        "    brew install cairo"
    )

# General configuration
INPUT_FOLDER = "posts/"
OUTPUT_FOLDER = "posts_with_logo/"
LOGO_SVG = "logo.svg"
LOGO_SIZE_RATIO = 0.1       # Logo width as a percentage of the image width
LOGO_OPACITY = 0.7          # Watermark opacity (0.0 to 1.0)
OFFSET_PIXELS = 20          # Offset from the edges (in pixels)

# Create the output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Convert the SVG logo to temporary PNG
logo_png_path = "logo_temp.png"
cairosvg.svg2png(url=LOGO_SVG, write_to=logo_png_path)
logo = Image.open(logo_png_path).convert("RGBA")

# Process each image in the input folder
for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        print(f"Processing {filename}...")

        # Open the main image
        img = Image.open(os.path.join(INPUT_FOLDER, filename)).convert("RGBA")
        img_w, img_h = img.size

        # Resize the logo
        logo_target_width = int(img_w * LOGO_SIZE_RATIO)
        aspect_ratio = logo.height / logo.width
        logo_target_height = int(logo_target_width * aspect_ratio)
        logo_resized = logo.resize((logo_target_width, logo_target_height), Image.LANCZOS)

        # Create a circular mask
        mask = Image.new("L", logo_resized.size, 0)
        draw = ImageDraw.Draw(mask)
        radius = min(logo_target_width, logo_target_height) // 2
        center = (logo_target_width // 2, logo_target_height // 2)
        draw.ellipse(
            [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
            fill=255,
        )

        # Apply the mask and opacity
        logo_rounded = logo_resized.copy()
        logo_rounded.putalpha(mask)
        alpha = logo_rounded.split()[3].point(lambda p: int(p * LOGO_OPACITY))
        logo_rounded.putalpha(alpha)

        # Position: bottom-right corner with offset
        position = (
            img_w - logo_target_width - OFFSET_PIXELS,
            img_h - logo_target_height - OFFSET_PIXELS
        )

        # Paste the rounded logo onto the image
        img.paste(logo_rounded, position, logo_rounded)

        # Save as .png
        output_filename = os.path.splitext(filename)[0] + ".png"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        img.save(output_path, "PNG")

# Remove the temporary logo file
os.remove(logo_png_path)

print("All images have been processed and saved in WebP format!")