# URANUS - Chess Book Digitization System
## Architecture (Uranus Master Engine v5.0)

### 🛠️ Core Technologies:
- **OCR Engine:** Marker (AI-driven Markdown conversion)
- **Vision Model:** Gemini Flash Vision (for chess move translation and verification)
- **Document Layout:** Python-Docx & Pandoc v3.1.11
- **Image Processing:** OpenCV & Contours v6 (chessboard extraction)

### ⚙️ 3-Phase Process:
1. **Extraction:** Automated board cropping and raw OCR.
2. **Refinement:** AI-assisted translation to professional Vietnamese chess terminology.
3. **Packaging:** Automated Word (.docx) generation with professional formatting.

### 📲 Integration:
- **Telegram Bridge:** Uranus Mirror Bridge for remote monitoring.
- **Search:** Brave Search API integration for terminology verification.

---
*Memory cleaned on 2026-02-28. System core preserved.*
