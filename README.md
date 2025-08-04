# 🎸 AutoTab

AutoTab is a web application that automatically extracts guitar tablature from videos. Just upload a video, define where the tab appears, and AutoTab will generate a clean set of tabs from the selected frames.

## 🚀 Features

- Upload guitar videos
- Choose between regular time intervals or specific timestamps for frame selection
- Crop specific regions where tablature appears
- Detect and display guitar tabs automatically using a trained model
- Fast and privacy-friendly — no login required
- Dockerized

## 🛠️ Tech Stack

- **Frontend:** React, TypeScript, Tailwind CSS
- **Backend:** Flask (Python)
- **Model Inference:** YOLO (Built on Pytorch)
- **Video Processing:** OpenCV (`cv2`)

## 🧪 Upcoming Features

- 📥 Download generated tabs in `.txt` or Guitar Pro format
- ☁️ Deployable demo version with public URL

---
