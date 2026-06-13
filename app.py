import os
from google import genai
import streamlit as st
from PIL import Image
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim

st.set_page_config(page_title="VisionQA", layout="wide")

st.title("VisionQA")

st.write("👋 Halo, butuh bantuanku untuk cari UI bug?")

choice = st.radio(
    "Pilih jawaban:",
    ["Belum pilih", "Yes", "No"],
    horizontal=True
)

if choice == "No":
    st.info("Baik, silahkan datang lagi jika perlu bantuan untuk cari UI Bug.")
    st.stop()

if choice == "Belum pilih":
    st.stop()

st.write("Silahkan upload expected design dan actual screenshot.")

expected_file = st.file_uploader("Upload Expected Image / Figma Design", type=["png", "jpg", "jpeg"])
actual_file = st.file_uploader("Upload Actual Screenshot", type=["png", "jpg", "jpeg"])

bug_count = 0
similarity_percent = 100

def generate_ai_analysis(bug_count, similarity_percent):
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are VisionQA, an AI assistant for QA testers.

    Visual comparison result:
    - Similarity score: {similarity_percent}%
    - Detected obvious UI difference areas: {bug_count}

    Create a simple QA finding summary in Indonesian.

    Use this exact format:

    If differences are detected, explain them generally.

    Example:

    VisionQA menemukan beberapa perbedaan visual.

    Jenis perubahan yang kemungkinan terdeteksi:
    • Perubahan teks atau angka
    • Perubahan nilai statistik
    • Perubahan komponen UI

    Silahkan cek kembali area yang ditandai untuk memastikan kesesuaian dengan desain yang diharapkan.

    Do not invent specific bugs.
    Do not mention release recommendation.
    Do not mention similarity score.

    Rules:
    - If there is no bug, say: Tidak ada UI bug obvious yang terdeteksi.
    - Do not mention release recommendation.
    - Do not mention similarity score.
    - Keep it short.
    - Maximum 5 findings.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

if expected_file and actual_file:
    expected = Image.open(expected_file).convert("RGB")
    actual = Image.open(actual_file).convert("RGB")

    expected_np = np.array(expected)
    actual_np = np.array(actual)

    actual_np = cv2.resize(actual_np, (expected_np.shape[1], expected_np.shape[0]))

    gray_expected = cv2.cvtColor(expected_np, cv2.COLOR_RGB2GRAY)
    gray_actual = cv2.cvtColor(actual_np, cv2.COLOR_RGB2GRAY)

    score, diff = ssim(gray_expected, gray_actual, full=True)
    diff = (diff * 255).astype("uint8")

    threshold = cv2.threshold(diff, 120, 255, cv2.THRESH_BINARY_INV)[1]

    contours, _ = cv2.findContours(
        threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    result = actual_np.copy()
    bug_count = 0

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 1500:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 3)
            bug_count += 1

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Expected")
        st.image(expected_np)

    with col2:
        st.subheader("Actual")
        st.image(actual_np)

    with col3:
        st.subheader("Detected Difference")
        st.image(result)

    st.subheader("Result")

    similarity_percent = round(score * 100, 2)
    st.caption("Analisis visual selesai.")

    st.subheader("VisionQA Analysis")

    with st.spinner("VisionQA sedang menganalisa dengan AI..."):
        try:
            ai_result = generate_ai_analysis(
                bug_count,
                similarity_percent
            )

            st.markdown(ai_result)

        except Exception:
            st.warning("AI sedang tidak tersedia, menampilkan hasil basic analysis.")

            if bug_count == 0 or similarity_percent > 98:
                st.write("""
                Tidak ada perbedaan visual yang signifikan terdeteksi.

                Tampilan aplikasi terlihat konsisten dengan desain yang diharapkan.
                """)

            else:
                st.markdown("""
                VisionQA menemukan beberapa perbedaan visual.

                **Jenis perubahan yang kemungkinan terdeteksi:**

                - Perubahan teks atau angka
                - Perubahan nilai statistik
                - Perubahan komponen UI
                - Perubahan tampilan grafik atau elemen visual

                Silahkan periksa kembali area yang ditandai untuk memastikan kesesuaian dengan desain yang diharapkan.
                """)