import cv2
import numpy as np

def srgb_to_luminance(rgb):
    """Convert sRGB triplet to relative luminance (Y)."""
    rgb = np.array(rgb) / 255.0
    rgb = np.where(rgb <= 0.03928, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def apca_contrast(text_rgb, bg_rgb):
    """Approximate APCA perceptual contrast (Lc) between text and background."""
    Ytxt = srgb_to_luminance(text_rgb)
    Ybg = srgb_to_luminance(bg_rgb)
    polarity = "dark_on_light" if Ybg > Ytxt else "light_on_dark"
    contrast = 400 * (Ybg ** 0.56 - Ytxt ** 0.57)
    if polarity == "light_on_dark":
        contrast *= -1
    return contrast, polarity


def analyze_image_contrast(path):
    """
    Detect text-like regions using MSER, then estimate average contrast
    between those regions (text) and surrounding background.
    """
    img = cv2.imread(path)
    if img is None:
        return {"file": path, "error": "Cannot read image"}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- Detect likely text regions ---
    mser = cv2.MSER_create(delta=5, min_area=60, max_area=8000)
    regions, _ = mser.detectRegions(gray)

    mask = np.zeros_like(gray)
    for p in regions:
        hull = cv2.convexHull(p.reshape(-1, 1, 2))
        cv2.drawContours(mask, [hull], -1, 255, -1)

    text_pixels = img[mask == 255]
    bg_pixels = img[mask == 0]

    if len(text_pixels) < 10 or len(bg_pixels) < 10:
        return {"file": path, "Lc": 0.0, "status": "fail"}

    # --- Compute mean color of text and background ---
    text_rgb = text_pixels.mean(axis=0)[::-1]  # BGR → RGB
    bg_rgb = bg_pixels.mean(axis=0)[::-1]

    # --- Compute contrast ---
    Lc, polarity = apca_contrast(text_rgb, bg_rgb)
    Lc = round(float(Lc), 2)

    # --- Relaxed threshold for synthetic data ---
    status = "pass" if abs(Lc) >= 25 else "fail"

    return {
        "file": path,
        "Lc": Lc,
        "polarity": polarity,
        "status": status
    }
