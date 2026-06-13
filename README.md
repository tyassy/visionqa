# VisionQA

VisionQA adalah aplikasi pendeteksi bug UI berbasis AI yang membantu membandingkan desain yang diharapkan (Figma/Mockup) dengan tampilan aktual aplikasi.

Aplikasi ini memanfaatkan Computer Vision untuk mendeteksi perbedaan visual dan Generative AI (Gemini) untuk menghasilkan ringkasan temuan secara otomatis.

## Fitur

* Membandingkan desain yang diharapkan dengan screenshot aplikasi
* Mendeteksi perbedaan visual menggunakan SSIM (Structural Similarity Index)
* Menandai area yang berbeda secara otomatis
* Menghasilkan ringkasan hasil analisis menggunakan Gemini AI
* Menampilkan analisis cadangan (fallback) jika layanan AI tidak tersedia
* Antarmuka web sederhana menggunakan Streamlit

## Cara Kerja

1. Upload gambar desain yang diharapkan (Expected Design).
2. Upload screenshot aplikasi aktual (Actual Screenshot).
3. VisionQA membandingkan kedua gambar menggunakan Computer Vision.
4. Area yang berbeda akan ditandai secara otomatis.
5. Gemini AI menghasilkan ringkasan hasil analisis dalam bahasa alami.

## Teknologi yang Digunakan

* Python
* Streamlit
* OpenCV
* SSIM (Structural Similarity Index)
* NumPy
* Google Gemini API

## Contoh Temuan

VisionQA dapat membantu mengidentifikasi perbedaan visual seperti:

* Perubahan teks atau angka
* Perubahan nilai statistik
* Perubahan komponen UI
* Perubahan tampilan grafik atau elemen visual

## Menjalankan Aplikasi

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tujuan Proyek

Proyek ini dibuat sebagai prototype AI Assistant untuk membantu proses validasi tampilan antarmuka (UI) dengan menggabungkan Computer Vision dan Large Language Model (LLM).

VisionQA bertujuan membantu QA Engineer mengidentifikasi perbedaan visual secara lebih cepat dan efisien dibandingkan pemeriksaan manual.
