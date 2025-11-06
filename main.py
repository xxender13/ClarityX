import argparse
from clarityx.utils import banner

from clarityx.contrast import analyze_image_contrast
from clarityx.clarity import clarity_score


import argparse
from clarityx.report import process_folder



def main():
    parser = argparse.ArgumentParser(description="ClarityX – Automated Visual Accessibility Tool")
    parser.add_argument("--input", type=str, required=True, help="Path to image or folder")
    args = parser.parse_args()

    print(banner())
    print(f"Initializing ClarityX on: {args.input}")
    print(">>> Scanning images...")
    print(">>> Running clarity and contrast modules (placeholder)...")
    print(">>> Done ✅")
    parser = argparse.ArgumentParser(description="ClarityX – Visual Accessibility Evaluator")
    parser.add_argument("--input", type=str, required=True, help="Path to image or folder")
    args = parser.parse_args()

    process_folder(args.input)

if __name__ == "__main__":
    main()