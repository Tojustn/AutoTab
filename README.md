# 🎸 AutoTab

AutoTab is a web application that automatically extracts guitar tablature from videos. Just upload a video, define where the tab appears, and AutoTab will generate a clean set of tabs from the selected frames.

## 🚀 Features

- 🎥 Upload guitar videos
- ⏱️ Choose between regular time intervals or specific timestamps for frame selection
- ✂️ Crop specific regions where tablature appears
- 🧠 Detect and display guitar tabs automatically using a trained model
- ⚡ Fast and privacy-friendly — no login required
- 🐳 Easy to run with Docker:  
  Simply run `docker compose up`

## 🛠️ Tech Stack

- **Frontend:** React, TypeScript, Tailwind CSS
- **Backend:** Flask (Python)
- **Model Inference:** YOLO / Custom Tab Detection Model
- **Video Processing:** OpenCV (`cv2`)

## 🧪 Upcoming Features

- 📥 Download generated tabs in `.txt` or Guitar Pro format
- ☁️ Deployable demo version with public URL

---

Let me know if you'd like help adding usage instructions, screenshots, badges (e.g. GitHub stars or Docker build), or a license section!
****
