# 🤟 Voxora.AI

**Real-time Sign Language Recognition & Translation System**

Transform ASL signs into text and speech instantly using advanced AI and computer vision.

---

## 🎯 Overview

Voxora.AI is an intelligent sign language recognition system that bridges communication gaps by converting American Sign Language (ASL) gestures into text and speech in real-time.

### ✨ Key Features

- ✅ **Real-time Recognition** - Instant ASL to text conversion
- ✅ **Web Interface** - Beautiful, responsive UI
- ✅ **Sentence Formation** - Intelligent word building
- ✅ **AI Correction** - GPT-powered grammar correction
- ✅ **Custom Training** - Train on your own gestures
- ✅ **High Accuracy** - 96-99% recognition rate

---

## 🚀 Quick Start

> **⚠️ IMPORTANT**: The trained model file is required but not included in the repository due to size (45MB). Use the setup scripts below to download it automatically.

### Option 1: Automatic Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/ramandeep-singh77/Voxora.ai.git
cd Voxora.ai

# One-click setup (downloads model + installs dependencies)
python setup.py

# Start application
quick_start.bat  # Windows
# or ./start.sh   # Linux/Mac
```

### Option 2: Manual Setup

See detailed instructions: **[INSTALLATION.md](INSTALLATION.md)**

### Open Browser

Navigate to: **http://localhost:3000**

### ⚠️ Model Required

The trained model (`signity_model.h5`) is required to run the application. It's automatically downloaded by the setup scripts above, or you can:

1. **Download manually**: Go to [Releases](https://github.com/ramandeep-singh77/Voxora.ai/releases) → Download `signity_model.h5`
2. **Place in**: `models/signity_model.h5`
3. **Verify setup**: Run `python check_setup.py`

### Usage

1. Allow camera access when prompted
2. Show ASL signs (hold for 1 second)
3. Letters form words automatically
4. Click "Add Space" to complete words
5. Click "Correct & Show" for AI correction

---

## 💻 Technology Stack

- **Frontend**: React 19, Vite 7
- **Backend**: Flask, Python
- **ML**: TensorFlow, Keras
- **CV**: OpenCV, MediaPipe
- **AI**: OpenAI GPT-4
- **Styling**: Modern CSS3 with animations

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Accuracy | 96-99% |
| FPS | 25-30 |
| Latency | <100ms |
| Signs | 28 (A-Z, space, del) |

---

## 🏗️ Architecture

```
Camera → Hand Detection → Landmark Extraction → CNN → Prediction → Text → GPT Correction
```

### Model

- **Type**: CNN (6 Conv1D + 3 Dense layers)
- **Input**: 63 hand landmark features
- **Output**: 28 classes
- **Training**: Custom dataset (14,000 samples)

---

## 📁 Project Structure

```
voxora-ai/
├── 🚀 Main Application
│   ├── web_app.py                      # Flask backend API
│   ├── hand_detector.py                # Hand detection (MediaPipe)
│   ├── config.py                       # Configuration settings
│   └── requirements.txt                # Python dependencies
│
├── 🎨 User Interface
│   └── ASL-Hand-sign-language-translator--main/  # React UI
│       ├── src/
│       │   ├── App.jsx                 # Main React component
│       │   ├── App.css                 # Styles
│       │   ├── index.css               # Global styles
│       │   └── main.jsx                # Entry point
│       ├── package.json                # Node dependencies
│       └── vite.config.js              # Vite configuration
│
├── 🧠 Models & Data
│   ├── models/
│   │   └── signity_model.h5            # Trained model (96-99% accuracy) [DOWNLOAD REQUIRED]
│   ├── my_custom_dataset/              # Custom training data (28K samples)
│   ├── processed_data/                 # Processed features
│   └── confusion_correction/           # Confusion fix classifiers
│
├── 🛠️ Training Tools
│   ├── create_custom_dataset.py        # Data collection tool
│   ├── train_custom_model.py           # Model training script
│   ├── data_preprocessing.py           # Data preprocessing
│   └── model_training.py               # Training utilities
│
└── 🎬 Quick Start
    ├── setup.py                        # One-click setup script
    ├── download_model.py               # Model downloader
    ├── check_setup.py                  # Setup verification
    ├── quick_start.bat                 # Windows quick start
    ├── start.bat                       # Start application
    └── INSTALLATION.md                 # Detailed setup guide
```

---

## 🎓 Training Custom Model

### 1. Collect Dataset (60 min)

```bash
python create_custom_dataset.py
```

- 500 samples per letter
- 14,000 total samples
- Auto-capture every 0.2s

### 2. Train Model (1-3 hours)

```bash
python train_custom_model.py
```

- Advanced CNN architecture
- 3x data augmentation
- 96-99% accuracy

---

## 🔧 Configuration

Edit `config.py`:

```python
CONFIDENCE_THRESHOLD = 0.85  # Recognition confidence
LETTER_HOLD_TIME = 1.0       # Hold duration
WINDOW_WIDTH = 640           # Camera resolution
WINDOW_HEIGHT = 480
```

---

## 🎨 Web Interface

### Features

- Live video streaming with hand tracking
- Real-time text display
- Visual confidence indicators
- Smooth animations and transitions
- Responsive design
- Modern gradient UI

### Controls

- **Add Space** - Complete current word
- **Delete Letter** - Remove last letter
- **Correct & Show** - AI-powered correction
- **Reset All** - Clear everything

---

## 🔧 Troubleshooting

### Model Missing Error

If you get "Model not found" error:

```bash
# Download the model
python download_model.py

# Or manually download from:
# https://github.com/ramandeep-singh77/Voxora.ai/releases
# Place in: models/signity_model.h5
```

### Camera Not Working

- Allow camera permissions in browser
- Check if camera is being used by another app
- Try refreshing the page

### Dependencies Issues

```bash
# Update pip and try again
python -m pip install --upgrade pip
pip install -r requirements.txt

# For Node.js issues
cd ASL-Hand-sign-language-translator--main
npm install --force
```

### Performance Issues

- Close other applications using camera
- Use Chrome/Edge for better performance
- Ensure good lighting for hand detection

---

## 📈 Future Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Multi-language support
- [ ] Speech-to-sign translation
- [ ] Cloud deployment
- [ ] API for developers

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Support for more sign languages
- Offline mode
- Multi-hand support
- Gesture recording

---

## 📝 License

MIT License

---

## 👥 Team

Built for [Hackathon Name]

**Made with 🤟 by [Your Team]**

*Empowering communication through AI*

---

## 📞 Contact

- **Email**: your.email@example.com
- **GitHub**: github.com/yourusername
- **Demo**: voxora-ai-demo.com

---

## 🙏 Acknowledgments

- MediaPipe for hand tracking
- TensorFlow team
- OpenAI for GPT-4
- ASL dataset contributors
