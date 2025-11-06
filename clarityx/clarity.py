import cv2
import numpy as np

def laplacian_variance(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def edge_density(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 160)
    return np.sum(edges > 0) / edges.size

def noise_estimate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3,3), 0)
    noise = np.std(blurred.astype(np.float32) - gray.astype(np.float32))
    return noise / 255.0

def clarity_score(path):
    image = cv2.imread(path)
    if image is None:
        return {"file": path, "error": "Cannot read image"}

    lap_var = laplacian_variance(image)
    edge_ratio = edge_density(image)
    noise = noise_estimate(image)

    # --- Dynamic normalization tuned for text images ---
    sharpness = np.clip(lap_var / 150.0, 0, 1)          # more generous scale
    structure = np.clip(edge_ratio * 25, 0, 1)          # edges weigh more
    noise_penalty = max(1.0 - (noise * 8), 0.4)         # lighter penalty

    clarity = 100 * sharpness * structure * noise_penalty
    clarity = round(float(clarity), 2)
    status = "pass" if clarity >= 30 else "fail"

    return {
        "file": path,
        "lap_var": round(lap_var, 2),
        "edge_density": round(edge_ratio, 3),
        "noise": round(noise, 3),
        "clarity_score": clarity,
        "status": status
    }
