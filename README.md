# Post Watermarker

Small Python script that automates the addition of a personal brand logo to blog post images.

---

## Features

- Converts an SVG logo to PNG automatically.
- Resizes the logo proportionally based on the image width.
- Applies rounded corners to the logo.
- Places the logo on the bottom right corner of each image.
- Batch processes all images in a folder.

---

## Requirements

- Python 3.8 or higher
- System library: **Cairo** (must be installed separately on macOS/Linux)

Python packages:

- Pillow
- CairoSVG

You can install the Python dependencies with:

```bash
pip install -r requirements.txt
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/asier-ortiz/post-watermarker.git
cd post-watermarker
```

2. (Optional) Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the Python requirements:

```bash
pip install -r requirements.txt
```

4. **macOS Users Only:**  
   Ensure you have the Cairo system library installed:

```bash
brew install cairo
```

If you still encounter issues, export the DYLD path:

```bash
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
```

You can automate this by running the `run.sh` script provided in the project.

---

## Usage

1. Place all your post images inside the `posts/` folder.
2. Place your `logo.svg` file in the project root.
3. Run the script manually:

```bash
python add_logo.py
```

Or use the provided script to automatically set environment variables (especially useful on macOS):

```bash
bash run.sh
```

Processed images will be saved in the `posts_with_logo/` folder.

---

## Project Structure

```
post-watermarker/
├── add_logo.py
├── run.sh
├── logo.svg
├── posts/             # Input images (without logo)
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── posts_with_logo/    # Output images (generated automatically)
├── README.md
└── requirements.txt
```

---

## Notes for macOS (Apple Silicon)

On macOS with M1/M2/M3 chips, you might encounter errors related to missing `cairo` libraries.
To fix this:

1. Make sure Cairo is installed via Homebrew:

```bash
brew install cairo
```

2. Export the dynamic library path before running the script:

```bash
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
```

Alternatively, you can add this line to your `~/.zshrc` to make it permanent:

```bash
echo 'export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH' >> ~/.zshrc
source ~/.zshrc
```

---

## License

This project is licensed under the MIT License.
