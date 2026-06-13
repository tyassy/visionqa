import streamlit as st
from PIL import Image
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim

st.set_page_config(page_title="VisionQA", layout="wide")

st.title("VisionQA")
user_question = st.text_input(
    "Ask VisionQA",
    placeholder="What bugs were found?"
)
st.write("Upload expected design dan actual screenshot untuk mendeteksi perbedaan UI yang obvious.")

expected_file = st.file_uploader("Upload Expected Image / Figma Design", type=["png", "jpg", "jpeg"])
actual_file = st.file_uploader("Upload Actual Screenshot", type=["png", "jpg", "jpeg"])

bug_count = 0
similarity_percent = 100

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

    threshold = cv2.threshold(diff, 180, 255, cv2.THRESH_BINARY_INV)[1]

    contours, _ = cv2.findContours(
        threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    result = actual_np.copy()
    bug_count = 0

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 300:
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
    st.write(f"Similarity score: **{similarity_percent}%**")

    if bug_count == 0 or similarity_percent > 98:
        st.success("No obvious UI bug detected.")

        st.subheader("VisionQA Analysis")

        st.write("""
        ✅ UI appears consistent with the expected design.

        Findings:
        - No major visual differences detected
        - Layout appears unchanged
        - No missing components detected

        Recommendation:
        Proceed with testing.
        """)

    else:
        st.error(f"Potential UI bug detected. Found {bug_count} obvious difference area(s).")

        st.subheader("VisionQA Analysis")

        st.write(f"""
        ⚠️ Potential UI issues found.

        Findings:
        - {bug_count} visual difference area(s) detected
        - Similarity score below expected threshold
        - Possible missing component, text change, or color mismatch

        Recommendation:
        Review highlighted areas and compare against the original design.
        """)

if user_question:

    if not expected_file or not actual_file:
        st.warning("Please upload both expected and actual images first.")

    else:
        if bug_count == 0:
            answer = """
        No major UI bugs were detected.

        The uploaded screenshot closely matches the expected design.
        """
        else:
            answer = f"""
        VisionQA detected {bug_count} potential UI issue(s).

        The highlighted regions indicate areas where the screenshot differs from the expected design.

        Please review these areas for missing elements, text changes, or styling inconsistencies.
        """

        st.subheader("VisionQA Assistant")
        st.write(answer)