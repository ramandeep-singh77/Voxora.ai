# 🤟 Voxora.AI

**Real-time Sign Language Recognition & Translation System**

Transform ASL signs into text and speech instantly using AI and computer vision.

## 🎬 Demo Video

**🎥 [Watch Voxora.AI in Action!](https://youtu.be/cvyST-QWqhw)**

See the complete AI model recognizing sign language in real-time with 96-99% accuracy, automatic sentence formation, and GPT-4 powered corrections.

---

## 🚀 Quick Start (Super Simple!)

### Option 1: Auto-Install Batch File (Recommended!)
1. **Download**: Click "Code" → "Download ZIP" 
2. **Extract**: Unzip the downloaded file
3. **Run**: Double-click `INSTALL_AND_RUN.bat`
4. **Wait**: Installs packages and starts automatically (first time: 5-10 minutes)
5. **Ready**: Browser opens at http://localhost:3000

### Option 2: Simple Batch (If Packages Installed)
1. **Install**: `pip install -r requirements.txt` (one time)
2. **Run**: Double-click `RUN.bat`
3. **Ready**: Browser opens automatically

### Option 3: Python Scripts
```bash
git clone https://github.com/ramandeep-singh77/Voxora.ai.git
cd Voxora.ai
python start_simple.py  # or python run.py
```

**That's it! No complex setup needed.** 🎉

### ✅ What Happens Automatically
- **First Time**: Installs missing Python packages (5-10 minutes)
- **Every Time**: Kills conflicting processes, starts Flask + React, opens browser
- **Result**: Ready to use at http://localhost:3000

---

## ✨ Features

- ✅ **Real-time Recognition** - Instant ASL to text conversion
- ✅ **Web Interface** - Beautiful, responsive UI  
- ✅ **Sentence Formation** - Intelligent word building
- ✅ **AI Correction** - GPT-powered grammar correction
- ✅ **High Accuracy** - 96-99% recognition rate
- ✅ **28 Signs** - A-Z letters + space + delete

---

## 🎮 How to Use

1. **Start App**: Run `python run.py` or double-click `RUN.bat`
2. **Allow Camera**: Grant camera permissions when prompted
3. **Position Hand**: Show your hand clearly to the camera
4. **Make Signs**: Hold ASL signs for 1 second each
5. **Form Words**: Letters automatically build words
6. **Add Spaces**: Click "Add Space" to complete words
7. **Get Corrections**: Click "Correct & Show" for AI grammar correction

---

## 📋 Requirements

- **Python 3.8+** - [Download Python](https://python.org/downloads)
- **Node.js 16+** - [Download Node.js](https://nodejs.org)
- **Webcam** - Required for sign recognition

*Dependencies install automatically when you run the app!*

---

## 💻 Technology

- **Frontend**: React 19 + Vite
- **Backend**: Flask + Python
- **AI**: TensorFlow + CNN Model
- **Vision**: OpenCV + MediaPipe
- **Correction**: OpenAI GPT-4

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Accuracy | 96-99% |
| FPS | 25-30 |
| Latency | <100ms |
| Signs | 28 classes |

---

## 🏗️ Project Structure

```
Voxora.ai/
├── 🚀 INSTALL_AND_RUN.bat             # Auto-install and run (RECOMMENDED)
├── 🚀 start_simple.py                 # Simple Python launcher
├── 🚀 run.py                          # Advanced Python launcher 
├── 🚀 RUN.bat                         # Windows batch launcher
├── 🌐 web_app.py                      # Flask backend
├── 👋 hand_detector.py                # Hand detection
├── 🧠 models/signity_model.h5         # Trained AI model
├── 🎨 ASL-Hand-sign-language-translator--main/  # React UI
└── 📦 requirements.txt                # Dependencies
```

---

## 🔧 Troubleshooting

### Camera Not Working
- Allow camera permissions in browser
- Close other apps using camera
- Try refreshing the page

### Dependencies Error
```bash
pip install -r requirements.txt
cd ASL-Hand-sign-language-translator--main
npm install
```

### Port Already in Use
- Close other applications using ports 3000 or 5000
- Or restart your computer

---

## 🎯 For Developers

### Manual Start
```bash
# Terminal 1: Start Flask API
python web_app.py

# Terminal 2: Start React UI  
cd ASL-Hand-sign-language-translator--main
npm run dev
```

### Train Custom Model
```bash
python create_custom_dataset.py  # Collect data
python train_custom_model.py     # Train model
```

---

## 📝 License

MIT License - Feel free to use and modify!

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Support for more sign languages
- Mobile app version
- Offline mode
- Multi-hand support

---

## 🙏 Acknowledgments

- MediaPipe for hand tracking
- TensorFlow team
- OpenAI for GPT-4
- ASL community

---

**🤟 Made with ❤️ for the deaf and hard-of-hearing community**

*Empowering communication through AI*