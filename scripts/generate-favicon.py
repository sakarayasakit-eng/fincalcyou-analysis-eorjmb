from PIL import Image, ImageDraw, ImageFont

ACCENT = "#0e7a4a"  # matches --accent in index.html light theme
SIZE = 256
RADIUS = 56

img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=RADIUS, fill=ACCENT)

font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 168)
text = "f"
bbox = draw.textbbox((0, 0), text, font=font)
w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
draw.text(
    ((SIZE - w) / 2 - bbox[0], (SIZE - h) / 2 - bbox[1]),
    text,
    font=font,
    fill="white",
)

img.save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
img.resize((180, 180), Image.LANCZOS).save("apple-touch-icon.png")
img.resize((32, 32), Image.LANCZOS).save("favicon-32x32.png")
img.resize((16, 16), Image.LANCZOS).save("favicon-16x16.png")
print("Favicon assets generated.")
