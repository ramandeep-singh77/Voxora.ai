# 🚀 Voxora.AI Installation Guide

Complete step-by-step installation instructions for Voxora.AI.

## 📋 Prerequisites

- **Python 3.8+** - [Download Python](https://python.org/downloads)
- **Node.js 16+** - [Download Node.js](https://nodejs.org)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Webcam** - Required for sign language recognition

## 🎯 Quick Installation (Recommended)

### Step 1: Clone Repository
```bash
git clone https://github.com/ramandeep-singh77/Voxora.ai.git
cd Voxora.ai
```

### Step 2: Run Setup
```bash
# Automatic setup (downloads model + installs everything)
python setup.py
```

### Step 3: Start Application
```bash
# Windows
quick_start.bat

# Linux/Mac
./start.sh
```

### Step 4: Open Browser
Navigate to: **http://localhost:3000**

---

## 🔧 Manual Installation

If automatic setup fails, follow these manual steps:

### Step 1: Download Model
```bash
# Download the trained model (45MB)
python download_model.py
```

**Alternative**: Download manually from [Releases](https://github.com/ramandeep-singh77/Voxora.ai/releases) and place in `models/signity_model.h5`

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install Node.js Dependencies
```bash
cd ASL-Hand-sign-language-translator--main
npm install
cd ..
```

### Step 4: Start Services
```bash
# Terminal 1: Start Flask API
python web_app.py

# Terminal 2: Start React UI
cd ASL-Hand-sign-language-translator--main
npm run dev
```

---

## 🔍 Verify Installation

Run the setup checker:
```bash
python check_setup.py
```

This will verify all files and dependencies are correctly installed.

---

## 🐛 Troubleshooting

### Model Missing Error
```
❌ ERROR: Model file not found!
```

**Solution:**
```bash
python download_model.py
```

### Python Dependencies Error
```
ModuleNotFoundError: No module named 'tensorflow'
```

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Node.js Dependencies Error
```
npm ERR! Cannot resolve dependency
```

**Solution:**
```bash
cd ASL-Hand-sign-language-translator--main
npm install --force
```

### Camera Not Working
- Allow camera permissions in browser
- Close other apps using the camera
- Try refreshing the page
- Use Chrome/Edge for better compatibility

### Port Already in Use
```
Address already in use: Port 5000
```

**Solution:**
```bash
# Kill process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Performance Issues
- Ensure good lighting for hand detection
- Close unnecessary applications
- Use a dedicated webcam if possible
- Check CPU usage during operation

---

## 📁 File Structure After Installation

```
Voxora.ai/
├── ✅ models/signity_model.h5          # Downloaded model (45MB)
├── ✅ web_app.py                       # Flask backend
├── ✅ hand_detector.py                 # Hand detection
├── ✅ ASL-Hand-sign-language-translator--main/
│   ├── ✅ node_modules/                # Node dependencies
│   └── ✅ src/App.jsx                  # React UI
├── ✅ requirements.txt                 # Python deps
└── ✅ start.bat / start.sh             # Start scripts
```

---

## 🎮 Usage Instructions

1. **Start Application**: Run `quick_start.bat` or `python web_app.py`
2. **Open Browser**: Go to http://localhost:3000
3. **Allow Camera**: Grant camera permissions when prompted
4. **Position Hand**: Show your hand clearly to the camera
5. **Make Signs**: Hold ASL signs for 1 second each
6. **Form Words**: Letters automatically form words
7. **Add Spaces**: Click "Add Space" to complete words
8. **Get Corrections**: Click "Correct & Show" for AI grammar correction

---

## 🔄 Updates

To update Voxora.AI:

```bash
git pull origin main
python setup.py  # Re-run setup if needed
```

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ramandeep-singh77/Voxora.ai/issues)
- **Documentation**: [README.md](README.md)
- **Setup Check**: `python check_setup.py`

---

## 🎯 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8 | 3.9+ |
| Node.js | 16.0 | 18.0+ |
| RAM | 4GB | 8GB+ |
| Storage | 2GB | 5GB+ |
| Camera | 720p | 1080p |
| OS | Windows 10, macOS 10.15, Ubuntu 18.04 | Latest versions |

---

**🤟 Ready to start signing!**