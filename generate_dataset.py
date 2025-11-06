import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random

BASE_DIR = "dataset/raw/synthetic"
os.makedirs(BASE_DIR, exist_ok=True)

texts = [
    "ClarityX", "Accessibility", "Contrast", "Legibility", "Perception",
    "Readability", "AI Vision", "Dynamic Range", "Text Visibility"
]
fonts = [
    "arial.ttf", "times.ttf", "calibri.ttf", "tahoma.ttf", "cour.ttf"
]
backgrounds = [
    (255, 255, 255), (0, 0, 0), (120, 120, 120),
    (30, 30, 30), (200, 200, 240), (230, 230, 230), (15, 15, 15)
]

# total samples
NUM_IMAGES = 500

for i in range(NUM_IMAGES):
    bg = random.choice(backgrounds)
    img = Image.new("RGB", (512, 256), color=bg)
    draw = ImageDraw.Draw(img)

    # random font and text size
    size = random.randint(18, 90)
    try:
        font = ImageFont.truetype(random.choice(fonts), size)
    except IOError:
        font = ImageFont.load_default()

    text = random.choice(texts)
    color_shift = random.randint(-60, 60)
    text_color = (
        max(0, min(255, bg[0] + color_shift)),
        max(0, min(255, bg[1] + color_shift)),
        max(0, min(255, bg[2] + color_shift)),
    )

    # place text
    draw.text((random.randint(20, 120), random.randint(60, 160)),
              text, fill=text_color, font=font)

    # convert to OpenCV
    img_cv = np.array(img)

    # optional blur
    if random.random() < 0.4:
        sigma = random.uniform(0.5, 3.0)
        img_cv = cv2.GaussianBlur(img_cv, (5, 5), sigma)

    # optional noise
    if random.random() < 0.3:
        noise = np.random.normal(0, 25, img_cv.shape).astype(np.int16)
        img_cv = np.clip(img_cv + noise, 0, 255).astype(np.uint8)

    # optional compression artifact (simulate low quality)
    if random.random() < 0.3:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), random.randint(20, 70)]
        _, encimg = cv2.imencode(".jpg", img_cv, encode_param)
        img_cv = cv2.imdecode(encimg, 1)

    cv2.imwrite(f"{BASE_DIR}/sample_{i:03d}.jpg", img_cv)

print(f"✅ Generated {NUM_IMAGES} synthetic images at {BASE_DIR}")
