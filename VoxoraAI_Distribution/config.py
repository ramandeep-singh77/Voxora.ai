"""
Signity.AI - Configuration Module
Central configuration for the two-way sign language communication system
"""

import os

# ==================== PATHS ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'hackdata')
TRAIN_DIR = os.path.join(DATASET_DIR, 'asl_alphabet_train', 'asl_alphabet_train')
TEST_DIR = os.path.join(DATASET_DIR, 'asl_alphabet_test', 'asl_alphabet_test')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
DATA_DIR = os.path.join(BASE_DIR, 'processed_data')
SIGN_ANIMATIONS_DIR = os.path.join(BASE_DIR, 'sign_animations')

# Create directories if they don't exist
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SIGN_ANIMATIONS_DIR, exist_ok=True)

# ==================== MODEL PARAMETERS ====================
IMG_SIZE = (200, 200)
SEQUENCE_LENGTH = 30  # Number of frames to consider for temporal patterns
NUM_LANDMARKS = 21  # MediaPipe hand landmarks
LANDMARK_DIMS = 3  # x, y, z coordinates

# Class labels (A-Z + special gestures)
CLASSES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
           'del', 'space']
NUM_CLASSES = len(CLASSES)

# ==================== TRAINING PARAMETERS ====================
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.2
EARLY_STOPPING_PATIENCE = 10
REDUCE_LR_PATIENCE = 5

# ==================== REAL-TIME DETECTION ====================
CONFIDENCE_THRESHOLD = 0.90  # Increased to reduce confusion
STABILIZATION_FRAMES = 15  # More frames for better stability
FPS_TARGET = 30
LETTER_HOLD_TIME = 1.5  # Seconds to hold a letter before adding to word

# ==================== OPENAI API ====================
OPENAI_API_KEY = "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"
OPENAI_MODEL = "gpt-4"
GPT_SYSTEM_PROMPT = """You are a helpful assistant that corrects and forms grammatically correct sentences 
from sequences of letters detected from sign language. The input may have errors or missing letters. 
Your job is to interpret the intended meaning and return a clean, natural sentence. 
Keep responses concise and natural."""

# ==================== SPEECH SETTINGS ====================
TTS_ENGINE = "pyttsx3"  # Options: pyttsx3, gtts
TTS_RATE = 150  # Words per minute
TTS_VOLUME = 0.9

# ==================== UI SETTINGS ====================
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BG_COLOR = (0, 0, 0)  # Black background
TEXT_COLOR = (255, 255, 255)  # White text
ACCENT_COLOR = (0, 255, 0)  # Green for highlights
FONT_SCALE = 0.8
FONT_THICKNESS = 2

# ==================== PREPROCESSING ====================
AUGMENTATION_ENABLED = True
NORMALIZE_LANDMARKS = True
BACKGROUND_REMOVAL = True
