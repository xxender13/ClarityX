import streamlit as st
import pandas as pd
import os
import tempfile
from PIL import Image
import cv2
import numpy as np

from clarityx.contrast import analyze_image_contrast
from clarityx.clarity import clarity_score

st.set_page_config(page_title="ClarityX Dashboard", layout="wide")
st.title("🧠 ClarityX Visual Intelligence Dashboard")

# =========================================================
# SECTION 1 — Load Results from Dataset
# =========================================================
st.header("📊 Dataset Results Dashboard")

csv_path = "clarityx_results.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.success(f"Loaded {len(df)} analyzed images from dataset.")
else:
    st.warning("No clarityx_results.csv found. Run main.py to generate one.")
    df = pd.DataFrame()

if not df.empty:
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        contrast_filter = st.selectbox("Contrast status", ["All", "pass", "fail"])
    with col2:
        clarity_filter = st.selectbox("Clarity status", ["All", "pass", "fail"])
    with col3:
        overall_filter = st.selectbox("Overall status", ["All", "pass", "fail"])

    filtered = df.copy()
    if contrast_filter != "All":
        filtered = filtered[filtered["contrast_status"] == contrast_filter]
    if clarity_filter != "All":
        filtered = filtered[filtered["clarity_status"] == clarity_filter]
    if overall_filter != "All":
        filtered = filtered[filtered["overall_status"] == overall_filter]

    st.write(f"**{len(filtered)} images** match filters.")

    # Metrics
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Average Contrast (Lc)", f"{filtered['contrast_Lc'].mean():.2f}")
    col_b.metric("Average Clarity Score", f"{filtered['clarity_score'].mean():.2f}")
    col_c.metric("Overall Pass Rate", f"{(filtered['overall_status'] == 'pass').mean() * 100:.1f}%")

    # Distributions
    st.subheader("Score Distributions")
    if not filtered.empty:
        st.bar_chart(filtered[["contrast_Lc", "clarity_score"]])

    # Image Gallery
    st.subheader("🖼️ Image Gallery")
    img_folder = "dataset/raw/synthetic"
    for _, row in filtered.head(40).iterrows():
        img_path = os.path.join(img_folder, os.path.basename(row["file"]))
        cols = st.columns([1, 2])
        with cols[0]:
            if os.path.exists(img_path):
                st.image(Image.open(img_path).resize((200, 200)))
            else:
                st.text("Image not found")
        with cols[1]:
            st.write(f"**File:** {os.path.basename(row['file'])}")
            st.write(f"Contrast Lc: {row['contrast_Lc']}")
            st.write(f"Clarity Score: {row['clarity_score']}")
            st.write(f"Overall: **{row['overall_status'].upper()}**")
        st.divider()

# =========================================================
# SECTION 2 — Upload & Analyze New Images
# =========================================================
st.header("📤 Upload & Analyze Images")

uploaded_files = st.file_uploader(
    "Upload one or more images (JPG, PNG, etc.)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

def explain_failure(contrast_result, clarity_result):
    reasons = []
    if contrast_result["status"] == "fail":
        reasons.append(f"Low contrast (Lc={contrast_result['Lc']})")
    if clarity_result["status"] == "fail":
        reasons.append(f"Low clarity (score={clarity_result['clarity_score']})")
    if not reasons:
        return "Pass — image is visually clear and readable."
    return "; ".join(reasons)

if uploaded_files:
    st.info(f"Analyzing {len(uploaded_files)} uploaded file(s)...")

    results = []
    for file in uploaded_files:
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
        image = Image.open(file)
        image.save(temp_path)

        contrast_res = analyze_image_contrast(temp_path)
        clarity_res = clarity_score(temp_path)

        overall = (
            "pass"
            if contrast_res["status"] == "pass" and clarity_res["status"] == "pass"
            else "fail"
        )
        reason = explain_failure(contrast_res, clarity_res)

        results.append({
            "file": file.name,
            "contrast_Lc": contrast_res["Lc"],
            "contrast_status": contrast_res["status"],
            "clarity_score": clarity_res["clarity_score"],
            "clarity_status": clarity_res["status"],
            "overall_status": overall,
            "reason": reason
        })

    result_df = pd.DataFrame(results)

    # Summary metrics
    st.subheader("Results Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Contrast (Lc)", f"{result_df['contrast_Lc'].mean():.2f}")
    col2.metric("Avg Clarity Score", f"{result_df['clarity_score'].mean():.2f}")
    col3.metric("Pass Rate", f"{(result_df['overall_status'] == 'pass').mean() * 100:.1f}%")

    # Table of results
    st.dataframe(result_df[["file", "contrast_Lc", "clarity_score", "overall_status", "reason"]])

    # Image previews
    st.subheader("Visual Review")
    for _, row in result_df.iterrows():
        cols = st.columns([1, 2])
        with cols[0]:
            st.image(Image.open(uploaded_files[_]).resize((200, 200)))
        with cols[1]:
            st.write(f"**{row['file']}** — **{row['overall_status'].upper()}**")
            st.write(row["reason"])
        st.divider()
