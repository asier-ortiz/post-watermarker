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

# General settings
INPUT_FOLDER = "posts/"  # Folder where the images are located
OUTPUT_FOLDER = "posts_with_logo/"  # Output folder for images with logo
LOGO_SVG = "logo.svg"  # Logo file (must be in the project root)
LOGO_SIZE_RATIO = 0.1  # Logo width will be 10% of the image width
MARGIN = 20  # Margin in pixels from the edges
CORNER_RADIUS = 20  # Corner radius for the rounded logo

# Create the output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Convert the SVG logo to PNG (in memory)
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

        # Create a rounded mask for the logo
        mask = Image.new('L', logo_resized.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, logo_target_width, logo_target_height], radius=CORNER_RADIUS, fill=255)
        logo_rounded = ImageOps.fit(logo_resized, mask.size)
        logo_rounded.putalpha(mask)

        # Calculate position: bottom right corner
        position = (img_w - logo_target_width - MARGIN, img_h - logo_target_height - MARGIN)

        # Paste the rounded logo onto the image
        img.paste(logo_rounded, position, logo_rounded)

        # Save the final image
        output_path = os.path.join(OUTPUT_FOLDER, filename)
        img.save(output_path)

# Clean up the temporary logo file
os.remove(logo_png_path)

print("✅ All images have been processed!")
