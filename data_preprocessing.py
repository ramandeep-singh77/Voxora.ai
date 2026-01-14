"""
Signity.AI - Data Preprocessing Module
Extracts hand landmarks from images and prepares training data
"""

import cv2
import mediapipe as mp
import numpy as np
import os
from tqdm import tqdm
import pickle
from config import *

class DataPreprocessor:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = None  # Initialize on demand
        
    def extract_landmarks_safe(self, image_path):
        """Extract hand landmarks from an image with proper resource management"""
        image = cv2.imread(image_path)
        if image is None:
            return None
        
        # Create a new MediaPipe instance for each image to avoid handle issues
        hands = None
        try:
            hands = self.mp_hands.Hands(
                static_image_mode=True,
                max_num_hands=1,
                min_detection_confidence=0.5
            )
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = hands.process(image_rgb)
            
            if results.multi_hand_landmarks:
                landmarks = []
                for hand_landmarks in results.multi_hand_landmarks:
                    for landmark in hand_landmarks.landmark:
                        landmarks.extend([landmark.x, landmark.y, landmark.z])
                return np.array(landmarks)
            return None
        finally:
            # Always close the hands instance
            if hands is not None:
                hands.close()
                del hands
    
    def process_dataset(self, dataset_path, max_samples_per_class=3000):
        """Process entire dataset and extract landmarks"""
        sequences = []
        labels = []
        
        print("🔄 Processing ASL Dataset...")
        print("⚠️  Using safe mode: Creating new MediaPipe instance per image")
        print("   This is slower but prevents Windows handle errors")
        
        for class_idx, class_name in enumerate(CLASSES):
            class_path = os.path.join(dataset_path, class_name)
            
            if not os.path.exists(class_path):
                print(f"⚠️  Warning: {class_name} folder not found")
                continue
            
            image_files = [f for f in os.listdir(class_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
            image_files = image_files[:max_samples_per_class]
            
            print(f"\n📂 Processing class '{class_name}' ({len(image_files)} images)...")
            
            # Process each image with its own MediaPipe instance
            for img_file in tqdm(image_files, desc=f"  {class_name}"):
                img_path = os.path.join(class_path, img_file)
                landmarks = self.extract_landmarks_safe(img_path)
                
                if landmarks is not None:
                    sequences.append(landmarks)
                    labels.append(class_idx)
        
        sequences = np.array(sequences)
        labels = np.array(labels)
        
        print(f"\n✅ Processed {len(sequences)} samples across {len(CLASSES)} classes")
        return sequences, labels
    
    def save_processed_data(self, sequences, labels, filename_prefix='data'):
        """Save processed data to disk"""
        sequences_path = os.path.join(DATA_DIR, f'{filename_prefix}_sequences.npy')
        labels_path = os.path.join(DATA_DIR, f'{filename_prefix}_labels.npy')
        
        np.save(sequences_path, sequences)
        np.save(labels_path, labels)
        
        print(f"💾 Saved to {sequences_path} and {labels_path}")
        
    def load_processed_data(self, filename_prefix='data'):
        """Load processed data from disk"""
        sequences_path = os.path.join(DATA_DIR, f'{filename_prefix}_sequences.npy')
        labels_path = os.path.join(DATA_DIR, f'{filename_prefix}_labels.npy')
        
        if os.path.exists(sequences_path) and os.path.exists(labels_path):
            sequences = np.load(sequences_path)
            labels = np.load(labels_path)
            print(f"📂 Loaded {len(sequences)} samples from disk")
            return sequences, labels
        return None, None

def main():
    """Main preprocessing pipeline"""
    preprocessor = DataPreprocessor()
    
    # Check if data already processed
    sequences, labels = preprocessor.load_processed_data('train')
    
    if sequences is None:
        print("🚀 Starting data preprocessing...")
        sequences, labels = preprocessor.process_dataset(TRAIN_DIR)
        preprocessor.save_processed_data(sequences, labels, 'train')
    else:
        print("✅ Using existing processed data")
    
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total samples: {len(sequences)}")
    print(f"   Feature shape: {sequences.shape}")
    print(f"   Classes: {NUM_CLASSES}")
    print(f"   Samples per class (avg): {len(sequences) // NUM_CLASSES}")

if __name__ == "__main__":
    main()
