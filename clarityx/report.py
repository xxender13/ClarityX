import os
import csv
from clarityx.contrast import analyze_image_contrast
from clarityx.clarity import clarity_score

def process_folder(folder_path, output_csv="clarityx_results.csv"):
    """Run clarity and contrast analysis on all images in a folder."""
    results = []
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".png", ".jpeg"))]

    for i, img_file in enumerate(image_files, 1):
        full_path = os.path.join(folder_path, img_file)
        print(f"[{i}/{len(image_files)}] Processing {img_file}...")

        contrast_result = analyze_image_contrast(full_path)
        clarity_result = clarity_score(full_path)

        results.append({
            "file": img_file,
            "contrast_Lc": contrast_result.get("Lc"),
            "contrast_status": contrast_result.get("status"),
            "clarity_score": clarity_result.get("clarity_score"),
            "clarity_status": clarity_result.get("status"),
            "overall_status": "fail" if (
                contrast_result.get("status") == "fail" or clarity_result.get("status") == "fail"
            ) else "pass"
        })

    # Save to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Results saved to {output_csv}")
    return results
