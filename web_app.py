"""
Voxora.AI - Web Interface
Real-time Sign Language Recognition System
Flask web app with camera streaming and sentence formation
"""

from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import cv2
import numpy as np
from tensorflow import keras
import os
import json
import time
from collections import deque
from hand_detector import HandDetector
import threading
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global variables
camera = None
hand_detector = None
model = None
class_mapping = None
current_letter = None
current_word = ""
sentence = ""
prediction_buffer = deque(maxlen=10)  # Reduced for faster response
last_letter_time = 0
letter_hold_time = 1.0  # Reduced from 1.5 to 1.0 seconds
confidence_threshold = 0.85  # Slightly lower for faster recognition

# OpenAI client
try:
    openai_client = OpenAI(
        api_key="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",
        base_url="https://openrouter.ai/api/v1"
    )
except Exception as e:
    print(f"⚠️  OpenAI client warning: {e}")
    openai_client = None

def load_model():
    """Load the trained model"""
    global model, class_mapping
    
    model_path = os.path.join('models', 'signity_model.h5')
    model = keras.models.load_model(model_path)
    print(f"✅ Model loaded: {model_path}")
    
    # Load class mapping
    mapping_path = os.path.join('processed_data', 'class_mapping.json')
    if os.path.exists(mapping_path):
        with open(mapping_path, 'r') as f:
            mapping = json.load(f)
        class_mapping = mapping['model_to_class']
    else:
        # Default mapping
        classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                  'del', 'nothing', 'space']
        class_mapping = {str(i): classes[i] for i in range(len(classes))}

def predict_sign(landmarks):
    """Predict sign from landmarks"""
    if landmarks is None:
        return 'nothing', 0.0
    
    landmarks_input = landmarks.reshape(1, -1)
    predictions = model.predict(landmarks_input, verbose=0)[0]
    class_idx = np.argmax(predictions)
    confidence = predictions[class_idx]
    
    class_name = class_mapping.get(str(class_idx), f"Unknown_{class_idx}")
    
    return class_name, confidence

def get_stable_prediction(landmarks):
    """Get stabilized prediction - OPTIMIZED"""
    global prediction_buffer
    
    if landmarks is None:
        prediction_buffer.clear()
        return 'nothing', 1.0
    
    predicted_class, confidence = predict_sign(landmarks)
    
    if confidence >= confidence_threshold:
        prediction_buffer.append(predicted_class)
    
    # Faster stabilization - need only 5 frames
    if len(prediction_buffer) >= 5:
        most_common = max(set(prediction_buffer), key=prediction_buffer.count)
        return most_common, confidence
    
    return predicted_class, confidence

def process_letter(letter):
    """Process detected letter and build words/sentences"""
    global current_letter, last_letter_time, current_word, sentence
    
    current_time = time.time()
    
    if letter == 'nothing':
        return
    
    if letter == 'space':
        if current_word:
            sentence += current_word + " "
            current_word = ""
        current_letter = None
        return
    
    if letter == 'del':
        if current_word:
            current_word = current_word[:-1]
        current_letter = None
        return
    
    # Regular letter
    if letter != current_letter:
        current_letter = letter
        last_letter_time = current_time
    else:
        if current_time - last_letter_time >= letter_hold_time:
            current_word += letter
            current_letter = None

def correct_sentence_with_gpt(text):
    """Correct sentence using GPT"""
    if openai_client is None:
        # Basic correction without GPT
        return text.capitalize()
    
    try:
        response = openai_client.chat.completions.create(
            model="openai/gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that corrects spelling and grammar in sentences formed from sign language. Return ONLY the corrected sentence, nothing else."
                },
                {
                    "role": "user",
                    "content": f"Correct this sentence: {text}"
                }
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"GPT Error: {e}")
        return text.capitalize()

def generate_frames():
    """Generate frames for video streaming - OPTIMIZED"""
    global camera, hand_detector
    
    camera = cv2.VideoCapture(0)
    # Reduce resolution for faster processing
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_FPS, 30)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    hand_detector = HandDetector()
    
    # JPEG encoding parameters for faster compression
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
    
    frame_count = 0
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        frame_count += 1
        frame = cv2.flip(frame, 1)
        
        # Process every frame for smooth video
        frame_with_hand, landmarks, hand_present = hand_detector.detect_hand(frame)
        
        # Get prediction (fast)
        predicted_letter, confidence = get_stable_prediction(landmarks)
        
        # Process letter
        if predicted_letter and confidence >= confidence_threshold:
            process_letter(predicted_letter)
        
        # Draw UI on frame (simplified for speed)
        h, w = frame_with_hand.shape[:2]
        
        # Simple dark rectangle (faster than overlay)
        cv2.rectangle(frame_with_hand, (0, 0), (w, 100), (0, 0, 0), -1)
        
        # Current prediction
        if predicted_letter:
            color = (0, 255, 0) if confidence >= confidence_threshold else (0, 165, 255)
            cv2.putText(frame_with_hand, f"{predicted_letter} {confidence*100:.0f}%", 
                       (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        # Current word (smaller text)
        cv2.putText(frame_with_hand, f"Word: {current_word[:20]}", 
                   (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Hand status indicator (smaller)
        if hand_present:
            cv2.circle(frame_with_hand, (w - 30, 30), 20, (0, 255, 0), -1)
        else:
            cv2.circle(frame_with_hand, (w - 30, 30), 20, (0, 0, 255), -1)
        
        # Fast JPEG encoding
        ret, buffer = cv2.imencode('.jpg', frame_with_hand, encode_param)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """API status endpoint"""
    return jsonify({
        'status': 'running',
        'name': 'Voxora.AI API',
        'version': '1.0',
        'endpoints': {
            'video_feed': '/video_feed',
            'get_text': '/get_text',
            'add_space': '/add_space',
            'delete_letter': '/delete_letter',
            'correct': '/correct',
            'reset': '/reset'
        }
    })

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_text')
def get_text():
    """Get current word and sentence"""
    return jsonify({
        'word': current_word,
        'sentence': sentence
    })

@app.route('/reset', methods=['POST'])
def reset():
    """Reset word and sentence"""
    global current_word, sentence, current_letter
    current_word = ""
    sentence = ""
    current_letter = None
    return jsonify({'status': 'success'})

@app.route('/correct', methods=['POST'])
def correct():
    """Correct and return sentence"""
    global sentence, current_word
    
    full_text = sentence + current_word
    if full_text.strip():
        corrected = correct_sentence_with_gpt(full_text)
        return jsonify({
            'original': full_text,
            'corrected': corrected
        })
    return jsonify({'error': 'No text to correct'})

@app.route('/add_space', methods=['POST'])
def add_space():
    """Add space (complete word)"""
    global current_word, sentence
    if current_word:
        sentence += current_word + " "
        current_word = ""
    return jsonify({'status': 'success'})

@app.route('/delete_letter', methods=['POST'])
def delete_letter():
    """Delete last letter"""
    global current_word
    if current_word:
        current_word = current_word[:-1]
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    try:
        print("\n" + "="*70)
        print("  VOXORA.AI - WEB INTERFACE")
        print("="*70)
        print("\n📂 Loading model...")
        load_model()
        print("✅ Model loaded")
        print("\n🌐 Starting web server...")
        print("   Open your browser and go to: http://localhost:5000")
        print("\n⚠️  Press Ctrl+C to stop the server")
        print("="*70 + "\n")
        
        app.run(debug=True, threaded=True, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
