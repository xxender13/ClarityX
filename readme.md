# 🧠 ClarityX  
### Visual Intelligence System for Image Clarity & Contrast Analysis  

ClarityX is an AI-driven visual quality analysis system that evaluates the **clarity, contrast, and readability** of images in real time.  
It’s designed to detect low-quality visual inputs — blurred, low-contrast, or poorly lit — and provide both **quantitative metrics** and **human-understandable reasoning** for each evaluation.  

Originally inspired by early work on *Clari_Fi (Rhino)*, ClarityX rebuilds the system from the ground up with a modular architecture, synthetic dataset generation, and an interactive Streamlit dashboard.

---

## 🚀 Features

| Category | Description |
|-----------|-------------|
| 🧮 **Clarity & Contrast Scoring** | Computes perceptual clarity, edge sharpness, and luminance contrast (Lc) |
| 📈 **Automated Batch Analysis** | Processes hundreds of images and generates a structured CSV with scores |
| 📊 **Interactive Dashboard** | Streamlit-powered dashboard with visual metrics, filters, and galleries |
| 📤 **Upload & Analyze** | Upload single or bulk images and instantly receive live analysis |
| 💬 **Explainable Results** | Provides clear reasoning on why an image “fails” or “passes” quality thresholds |
| 🧰 **Modular Codebase** | Components split across `clarityx/` modules for clarity, contrast, and reporting |

---

## 🏗️ Folder Structure

```
ClarityX/
├── app.py                     # Streamlit dashboard
├── main.py                    # Batch analysis entry point
├── clarityx/
│   ├── __init__.py
│   ├── clarity.py             # Clarity analysis logic
│   ├── contrast.py            # Contrast analysis logic
│   ├── report.py              # Batch processing and CSV export
│   └── utils.py               # Common helper functions
├── dataset/
│   └── raw/synthetic/         # Synthetic training/validation images
├── clarityx_results.csv       # Auto-generated after analysis
└── README.md
```

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/xxender13/ClarityX.git
   cd ClarityX
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(If you don’t have one yet, use `pip install streamlit opencv-python pillow pandas numpy`)*

---

## 🧪 Usage

### 🔹 Batch Processing
Run the full dataset analysis:
```bash
python main.py --input dataset/raw/synthetic
```

This generates a CSV file `clarityx_results.csv` with columns:
```
file, contrast_Lc, contrast_status, clarity_score, clarity_status, overall_status
```

---

### 🔹 Live Streamlit Dashboard
Launch the interactive interface:
```bash
streamlit run app.py
```

Features include:
- Dataset analytics with filters and visual metrics  
- Bulk or single image uploads  
- Real-time scoring and explanations  
- Image previews with pass/fail reasoning  

---

## 📊 Example Output

| File | Contrast Lc | Clarity Score | Overall | Reason |
|------|--------------|---------------|----------|---------|
| sample_001.jpg | 21.4 | 6.9 | ❌ Fail | Low contrast & clarity |
| sample_034.jpg | 31.1 | 61.7 | ✅ Pass | High edge density |
| sample_107.jpg | 42.5 | 63.6 | ✅ Pass | Sharp and well-lit |
| sample_400.jpg | 7.4 | 67.4 | ❌ Fail | Blur detected |

---

## 🧩 Next Steps

- [ ] Add visual heatmaps for failed regions  
- [ ] Integrate deep perceptual image quality metrics (LPIPS / NIQE)  
- [ ] Deploy Streamlit app online  
- [ ] Add API mode for external integration  

---

## 👤 Author

**Harshil Sharma**  
Researcher & AI Engineer  
[GitHub: xxender13](https://github.com/xxender13)  
Saint Louis University | PRiME Center | HKP Project  

---

## 🧾 License
Currently private and under development.  
All rights reserved © 2025, Harshil Sharma.

---

> *"ClarityX brings measurable intelligence to visual perception — bridging computer vision and human understanding."*
