"""
Signity.AI - Hand Detection Module
Real-time hand detection and landmark extraction using MediaPipe
"""

import cv2
import mediapipe as mp
import numpy as np
from config import *

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize hands on first use to avoid handle issues
        self.hands = None
        self._frame_count = 0
        self._reinit_interval = 100  # Reinitialize every 100 frames
        
    def detect_hand(self, frame):
        """Detect hand in frame and return landmarks"""
        # Initialize or reinitialize hands periodically to avoid handle buildup
        if self.hands is None or self._frame_count >= self._reinit_interval:
            if self.hands is not None:
                self.hands.close()
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
            self._frame_count = 0
        
        self._frame_count += 1
        
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame
        results = self.hands.process(frame_rgb)
        
        landmarks = None
        hand_present = False
        
        if results.multi_hand_landmarks:
            hand_present = True
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Extract landmark coordinates
            landmarks = []
            for landmark in hand_landmarks.landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
            landmarks = np.array(landmarks)
            
            # Draw landmarks on frame
            self.mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style()
            )
        
        return frame, landmarks, hand_present
    
    def extract_hand_region(self, frame, landmarks_raw):
        """Extract and isolate hand region with black background"""
        if landmarks_raw is None:
            return frame
        
        h, w, _ = frame.shape
        
        # Get bounding box from landmarks
        x_coords = [landmarks_raw[i] for i in range(0, len(landmarks_raw), 3)]
        y_coords = [landmarks_raw[i] for i in range(1, len(landmarks_raw), 3)]
        
        x_min = int(min(x_coords) * w) - 20
        x_max = int(max(x_coords) * w) + 20
        y_min = int(min(y_coords) * h) - 20
        y_max = int(max(y_coords) * h) + 20
        
        # Ensure bounds are within frame
        x_min = max(0, x_min)
        x_max = min(w, x_max)
        y_min = max(0, y_min)
        y_max = min(h, y_max)
        
        # Create black background
        black_frame = np.zeros_like(frame)
        
        # Copy hand region to black background
        black_frame[y_min:y_max, x_min:x_max] = frame[y_min:y_max, x_min:x_max]
        
        return black_frame
    
    def close(self):
        """Release resources"""
        self.hands.close()
